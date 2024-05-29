import time
from functools import wraps

import dropbox
import requests
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from CourseProject import settings
from .forms import PresentationForm, PresentationEditForm
from .models import Presentation
import os
from gpttest import presentationAnalyze

context = {
    'page_obj': '',
    'form': '',
    'error': '',
    'success': '',
    'querystring': '',
    'typeOfContent': '',
}


def check_authorization(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            member = Presentation.objects.get(id=kwargs.get('id'))
        except Presentation.DoesNotExist:
            return redirect('home')

        if request.user.is_authenticated:
            if request.user.is_superuser or (
                    request.user.first_name == member.author.split()[0] and
                    request.user.last_name == member.author.split()[1]
            ) or request.user.is_staff:
                return view_func(request, *args, **kwargs)
        return redirect('home')

    return _wrapped_view


access_token = None
expires_at = 0
dbx = None


def get_access_token(refresh_token, app_key, app_secret):
    global access_token, expires_at, dbx

    url = 'https://api.dropboxapi.com/oauth2/token'
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': app_key,
        'client_secret': app_secret
    }
    response_data = requests.post(url, data=data).json()
    access_token = response_data.get('access_token')
    expires_at = time.time() + response_data.get('expires_in')
    dbx = dropbox.Dropbox(access_token)


get_access_token(settings.REFRESH_TOKEN, settings.APP_KEY, settings.APP_SECRET)
dbx = dropbox.Dropbox(access_token)

def chek_access_token():
    if expires_at - time.time() < 3600:
        print("get new token")
        get_access_token(settings.REFRESH_TOKEN, settings.APP_KEY, settings.APP_SECRET)
    if access_token and expires_at > time.time():
        print("do nothing")
        return None

def database(request):
    sort_by = request.GET.get('sort_by', '-time')
    pres = Presentation.objects.order_by(sort_by)

    paginator = Paginator(pres, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'typeOfContent': 'database',
        'sort_by': sort_by,
    }
    return render(request, 'maindb/database.html', context)

class PresentationView(DetailView):
    model = Presentation
    template_name = 'maindb/PresentationView.html'
    context_object_name = 'presentation'

def editPr(request, id):
    global context
    presentation = get_object_or_404(Presentation, id=id)
    initial_data = {
        "title": presentation.title,
        "notes": presentation.notes,
        "link": presentation.link,
        "rating": presentation.rating,
        "group": presentation.group,
    }
    if request.method == 'POST':
        form = PresentationEditForm(request.POST)
        is_auto = request.POST.get('is_auto')
        is_auto_link = request.POST.get('is_auto_link')
        print(form.errors)
        if form.is_valid() or is_auto:

            presentation.title = request.POST.get('title')
            presentation.notes = request.POST.get('notes')
            presentation.link = request.POST.get('link')
            presentation.rating = request.POST.get('rating')
            presentation.group = request.POST.get('group')

            if is_auto_link:
                chek_access_token()
                presentation.link = dbx.sharing_create_shared_link(path=f'/presentation/{presentation.title}').url

            if is_auto:
                path_pres = "pptx/" + presentation.title
                file_path = "/presentation/" + presentation.title
                with open(path_pres, "wb") as f:
                    metadata, res = dbx.files_download(file_path)
                    f.write(res.content)
                presentation.group = presentationAnalyze(path_pres)
                os.remove(path_pres)

            presentation.save()
            context.update({'success': 'Презентація успішно відредагована!'})
            initial_data.update(request.POST.dict())
        else:
            context.update({'error': 'Неправильно введені дані!'})

    form = PresentationEditForm(initial=initial_data)
    context.update({'form': form})

    return render(request, 'maindb/editPresentation.html', context)


@check_authorization
def link(request, id):
    member = Presentation.objects.get(id=id)
    if member.link == '':
        chek_access_token()
        member.link = dbx.sharing_create_shared_link(path=f'/presentation/{member.title}').url
        member.save()
    return redirect(member.link)


@check_authorization
def delete(request, id):
    member = Presentation.objects.get(id=id)
    chek_access_token()
    if exists_file_dropbox(f'/presentation/{member.title}'):
        dbx.files_delete_v2(f'/presentation/{member.title}')
    member.delete()
    return redirect('database')

def exists_file_dropbox(path):
    try:
        dbx.files_get_metadata(path)
        return True
    except:
        return False

def addPr(request):
    context = {}
    if request.method == 'POST':
        form = PresentationForm(request.POST, request.FILES)
        is_auto_generate_content = request.POST.get('is_auto') == 'on'
        print(is_auto_generate_content)

        if form.is_valid():
            presentation = form.save(commit=False)
            presentation.author = request.user.first_name + " " + request.user.last_name
            presentation.title = request.FILES['file'].name
            file = request.FILES.get('file')
            file_content = file.read()

            try:
                chek_access_token()
                dbx.files_upload(file_content, f'/presentation/{file.name}')
                link = dbx.sharing_create_shared_link(path=f'/presentation/{file.name}').url
                presentation.link = link
                presentation.save()
                context.update({'success': 'Презентація успішно додана!'})
            except Exception as e:
                context.update({'error': f'Помилка завантаження: {str(e)}'})

            if is_auto_generate_content:
                with open(os.path.join('pptx', file.name), 'wb+') as destination:
                    destination.write(file_content)
                group = presentationAnalyze('pptx/'+file.name)
                presentation.group = group
                presentation.save()
                os.remove('pptx/'+file.name)

        else:
            context.update({'error': 'Неправильно введені дані!', 'form': form})


    form = PresentationForm()
    context.update({'form': form})

    return render(request, 'maindb/addPresentation.html', context)

def get_querystring(request):
    params = request.GET.copy()
    if 'page' in params:
        del params['page']
    return params.urlencode()

def search_view(request):
    template_name = 'maindb/database.html'
    paginate_by = 10
    query_dict = {}
    for key, value in request.GET.items():
        if value and key != 'page' and key != 'search_type' and key != 'sort_by':
            query_dict[key] = value.lower()

    object_list = Presentation.objects.all()
    for key, value in query_dict.items():
        query = key + '__icontains'
        filter_kwargs = {query: value}
        object_list = object_list.filter(**filter_kwargs)

    sort_by = request.GET.get('sort_by', '-time')
    object_list = object_list.order_by(sort_by)

    paginator = Paginator(object_list, paginate_by)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'querystring': get_querystring(request),
        'typeOfContent': 'search',
        'sort_by': sort_by,
    }
    return render(request, template_name, context)