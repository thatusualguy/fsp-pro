from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
import logging

from rc_backend.rc_app.models import Competition
from rc_backend.rc_app.models import CompetitionResult
from rc_backend.rc_app.models import FSP
from rc_backend.rc_app.models import InviteCompetition
from rc_backend.rc_app.models import Profile
from rc_backend.rc_app.models import Team
from rc_backend.rc_app.models import OnModerationStatus
from rc_backend.rc_app.models import Discipline


# Register your models here.

class CompetitionResultAdmin(admin.ModelAdmin):
    pass


class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'finish_date', 'place', 'on_moderation', 'competition_type', 'get_fsps')
    list_filter = ('fsps', 'on_moderation')
    search_fields = ("title", 'place')

    def get_fsps(self, obj):
        return "\n".join([str(fsp) for fsp in obj.fsps.all()])

    def response_change(self, request, obj):
        if "_send_to_moderation" in request.POST:
            if obj.on_moderation == OnModerationStatus.PENDING:
                self.message_user(request, "Соревнование уже на модерации!", messages.ERROR)
            elif obj.on_moderation == OnModerationStatus.APPROVED:
                self.message_user(request, "Соревнование уже принято!", messages.ERROR)
            else:
                obj.on_moderation = OnModerationStatus.PENDING
                obj.save()
                self.message_user(request, "Запись отправлена на модерацию!", messages.SUCCESS)
            return HttpResponseRedirect(".")  # Обновляем страницу
        return super().response_change(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='Федеральное ФСП').exists() or request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        return ('on_moderation', )



class ProfileAdmin(admin.ModelAdmin):
    pass


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'competition', 'leader', 'get_team_members', 'moderation_status')
    list_filter = ('competition',)
    search_fields = ("title", 'get_team_members', 'competition')


class FSPAdmin(admin.ModelAdmin):
    pass


class InviteCompetitionAdmin(admin.ModelAdmin):
    pass


class DisciplineAdmin(admin.ModelAdmin):
    pass


admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(CompetitionResult, CompetitionResultAdmin)
admin.site.register(FSP, FSPAdmin)
admin.site.register(InviteCompetition, InviteCompetitionAdmin)
admin.site.register(Discipline, DisciplineAdmin)