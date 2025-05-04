from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from src.core.models import Profile, FSP
from django import forms

class CustomRegisterForm(UserCreationForm):
    username = forms.CharField(label="Логин", max_length=150, required=True)
    first_name = forms.CharField(label="Имя пользователя", max_length=150, required=True)
    last_name = forms.CharField(label="Фамилия", max_length=150, required=True)
    email = forms.EmailField(label="Email", required=True)
    fsp = forms.ModelChoiceField(label="ФСП", queryset=FSP.objects.all(), required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'fsp')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class RegisterUser(FormView):
    template_name = 'core/login/register.html'
    form_class = CustomRegisterForm
    success_url = reverse_lazy('/app/login')

    def form_valid(self, form):
        user = form.save()
        # Create a Profile for the new user with all the provided information
        Profile.objects.create(
            user=user,
            name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email'],
            fsp=form.cleaned_data['fsp'],
        )
        return redirect(self.success_url)
