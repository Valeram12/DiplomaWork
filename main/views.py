from django.contrib import messages
from django.contrib.auth import login, authenticate, logout  # add this
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import F, Value, CharField
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import NewUserForm


def main(request):
    return render(request, 'main/main.html')

def help(request):
    return render(request, 'main/help.html')

def user_manage(request):
    if request.user.is_superuser:
        sort_by = request.GET.get('sort_by', 'username')
        users = User.objects.order_by(sort_by)
        paginator = Paginator(users, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'typeOfContent': 'user_manage',
            'sort_by': sort_by,
        }
        return render(request, 'main/userManage.html', context)
    else:
        return redirect('home')

def toggle_staff_status(request, user_id):
    if request.user.is_superuser:
        user_profile = User.objects.get(id=user_id)
        user_profile.is_staff = not user_profile.is_staff
        user_profile.save()
        return user_manage(request)
    else:
        return redirect('home')

def get_querystring(request):
    params = request.GET.copy()
    if 'page' in params:
        del params['page']
    return params.urlencode()

def search_view_users(request):
    template_name = 'main/userManage.html'
    paginate_by = 10
    query_dict = {}
    for key, value in request.GET.items():
        if value and key != 'page' and key != 'search_type' and key != 'sort_by':
            query_dict[key] = value.lower()

    object_list = User.objects.all()
    for key, value in query_dict.items():
        query = key + '__icontains'
        filter_kwargs = {query: value}
        object_list = object_list.filter(**filter_kwargs)

    sort_by = request.GET.get('sort_by', 'username')
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

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
        messages.error(request, "Невдала реєстрація. Перевірте правильність введеної інформації.")
    form = NewUserForm()
    return render(request=request, template_name="main/register.html", context={"register_form": form})

def login_request(request):
    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Неправильне ім'я користувача або пароль.")
        else:
            messages.error(request, "Неправильне ім'я користувача або пароль.")
    form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"login_form": form})

def logout_view(request):
    logout(request)