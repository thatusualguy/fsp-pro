from django.contrib import admin

from rc_backend.rc_app.models import Competition
from rc_backend.rc_app.models import CompetitionResult
from rc_backend.rc_app.models import FSP
from rc_backend.rc_app.models import FSPCompetition
from rc_backend.rc_app.models import InviteCompetition
from rc_backend.rc_app.models import Profile
from rc_backend.rc_app.models import Team


# Register your models here.

class CompetitionResultAdmin(admin.ModelAdmin):
    pass


class CompetitionAdmin(admin.ModelAdmin):
    pass


class ProfileAdmin(admin.ModelAdmin):
    pass


class TeamAdmin(admin.ModelAdmin):
    pass


class FSPAdmin(admin.ModelAdmin):
    pass


class FSPCompetitionAdmin(admin.ModelAdmin):
    pass


class InviteCompetitionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(CompetitionResult, CompetitionResultAdmin)
admin.site.register(FSP, FSPAdmin)
admin.site.register(FSPCompetition, FSPCompetitionAdmin)
admin.site.register(InviteCompetition, InviteCompetitionAdmin)
