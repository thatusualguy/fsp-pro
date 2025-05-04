from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from src.core.models import Profile


class LoginUser(LoginView):
    template_name = 'core/login/login.html'
    form_class = AuthenticationForm
    # redirect_authenticated_user = True
    success_url = reverse_lazy('/app/profile/')
    next_page = reverse_lazy('core:profile')

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