from django import forms
from django.forms import ModelForm, TextInput
from django.utils import timezone

from .models import Presentation


class PresentationForm(ModelForm):
    is_auto = forms.BooleanField(label='Is Auto', required=False)

    class Meta:
        model = Presentation

        fields = ['notes', 'rating', 'group']
        widgets = {
            "notes": TextInput(attrs={'class': 'textareaForm', 'placeholder': 'Примітка'}),
            "rating": TextInput(attrs={'class': 'textareaForm', 'placeholder': 'Оцінка'}),
            "group": TextInput(attrs={'class': 'textareaForm', 'placeholder': 'Вміст'}),
        }



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance'] is not None:
            self.fields['is_auto'].initial = kwargs['instance'].is_auto


    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.time = timezone.now()
        if 'is_auto' in self.cleaned_data:
            instance.is_auto = self.cleaned_data['is_auto']
        if commit:
            instance.save()
        return instance


class PresentationEditForm(ModelForm):
    is_auto = forms.BooleanField(label='Is Auto', required=False)
    is_auto_link = forms.BooleanField(label='Is Auto Link', required=False)
    class Meta:
        model = Presentation
        fields = ['title', 'notes', 'link', 'rating', 'group']
        widgets = {
            "title": TextInput(attrs={'class': 'textareaForm', 'placeholder': 'Назва презентації'}),
            "notes": TextInput(attrs={'class': 'textareaForm', 'placeholder': 'Примітка'}),
            "link": TextInput(attrs={'class': 'textareaForm', 'placeholder': 'Посилання на презентацію'}),
            "rating": TextInput(attrs={'class': 'textareaForm', 'placeholder': 'Оцінка'}),
            "group": TextInput(attrs={'class': 'textareaForm', 'placeholder': 'Вміст'})
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance'] is not None:
            self.fields['is_auto'].initial = kwargs['instance'].is_auto
        if 'instance' in kwargs and kwargs['instance'] is not None:
            self.fields['is_auto_link'].initial = kwargs['instance'].is_auto

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.time = timezone.now()
        if 'is_auto' in self.cleaned_data:
            instance.is_auto = self.cleaned_data['is_auto']
        if 'is_auto_link' in self.cleaned_data:
            instance.is_auto = self.cleaned_data['is_auto_link']
        if commit:
            instance.save()
        return instance

