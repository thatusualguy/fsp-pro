from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from rc_backend.rc_app.models import Profile, FSP


class LoginUser(LoginView):
    template_name = 'rc_app/login/login.html'
    form_class = AuthenticationForm
    # redirect_authenticated_user = True
    # success_url = reverse_lazy('/')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            # Check if the user has a Profile object connected
            if Profile.objects.filter(user=user).exists():
                # A backend authenticated the credentials and user has a Profile
                return super().form_valid(form)
            else:
                return redirect('admin')
        else:
            # No backend authenticated the credentials
            return self.form_invalid(form)


class RegisterUser(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Save the new user
        user = form.save()

        # Create a Profile for the new user
        Profile.objects.create(user=user, fsp=FSP.objects.first())

        # Redirect to login page
        return redirect(self.success_url)


class LogoutUser(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
