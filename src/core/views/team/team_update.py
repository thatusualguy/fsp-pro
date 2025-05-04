@login_required
def send_team_to_moderation(request, team_id):
    if request.method == 'POST':
        team = get_object_or_404(Team, id=team_id)
        # Ensure only team leader can send for moderation
        if request.user.profile == team.leader:
            team.moderation_status = ModerationEnum.PENDING
            team.save()
        else:
            raise PermissionDenied
    return redirect('core:team_details', pk=team.id)


class TeamUpdateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['title', 'invitees']

    invitees = forms.ModelMultipleChoiceField(
        queryset=Profile.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Пригласить участников"
    )

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.fields['invitees'].queryset = Profile.objects.all()


class TeamUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'core/team_form.html'
    model = Team
    form_class = TeamUpdateForm

    def dispatch(self, request, *args, **kwargs):
        team: Team = self.get_object()
        # Get current user's profile
        profile = get_object_or_404(Profile, user=self.request.user)

        # Check if current user is the team leader
        if team.leader != profile:
            raise PermissionDenied("You do not have permission to update this team.")

        return super().dispatch(request, *args, **kwargs)
