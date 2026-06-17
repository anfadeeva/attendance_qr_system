# attendance_app/forms.py
from django import forms
from .models import Session, Subject

from django.contrib.auth.models import User
from .models import Profile

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['subject', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs.update({'class': 'form-control'})
        # Опционально: показывать только предметы, которые ведёт текущий преподаватель
        # self.fields['subject'].queryset = Subject.objects.filter(...)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

from django import forms
from .models import Group, Subject

class ReportForm(forms.Form):
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label="Группа",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        label="Предмет",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_from = forms.DateField(
        label="С",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_to = forms.DateField(
        label="По",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
   

    
from django.contrib.auth.forms import PasswordChangeForm

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class StudentGroupForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['group']
        widgets = {'group': forms.Select(attrs={'class': 'form-control'})}