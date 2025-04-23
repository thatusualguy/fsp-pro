from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('/')

    def form_valid(self, form):
        user = authenticate(username="john", password="secret")
        if user is not None:
            # A backend authenticated the credentials
            ...
        else:
            # No backend authenticated the credentials
            ...
        return super().form_valid(form)
