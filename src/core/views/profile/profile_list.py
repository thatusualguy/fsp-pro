from django.views.generic import ListView

from src.core.models import Profile


class ProfilesListView(ListView):
    model = Profile
    paginate_by = 50
    template_name = "core/profile/profile_list.html"

