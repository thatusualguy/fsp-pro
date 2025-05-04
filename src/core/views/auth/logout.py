from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy


class LogoutUser(LogoutView):
    next_page = reverse_lazy('/app/about')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)