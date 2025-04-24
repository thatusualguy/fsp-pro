from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect

from rc_backend.rc_app.models import Competition
from rc_backend.rc_app.models import CompetitionResult
from rc_backend.rc_app.models import FSP
from rc_backend.rc_app.models import InviteCompetition
from rc_backend.rc_app.models import Profile
from rc_backend.rc_app.models import Team
from rc_backend.rc_app.models import OnModerationStatus
from rc_backend.rc_app.models import Discipline

from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.
class CompetitionResultResourse(resources.ModelResource):
    class Meta:
        model = CompetitionResult


class CompetitionResultAdmin(ImportExportModelAdmin):
    list_display = ("team__competition__title", 'team', "place", "points")
    list_filter = ("team", "team__competition__title", "place", "points")
    search_fields = ("team", 'team__competition__title')
    resource_classes = [CompetitionResultResourse]


class CompetitionResourse(resources.ModelResource):
    class Meta:
        model = Competition

class CompetitionAdmin(ImportExportModelAdmin):
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
        # if request.user.groups.filter(name='Федеральное ФСП').exists() or request.user.is_superuser:
        return super().response_change(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='Федеральное ФСП').exists() or request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        return ('on_moderation', )

class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile

class ProfileAdmin(ImportExportModelAdmin):
    list_display = ("__str__", "email", "fsp")
    search_fields = ("__str__", "email")
    list_filter = ("fsp", )
    resource_classes = [ProfileResource]


class TeamResource(resources.ModelResource):
    class Meta:
        model = Team

class TeamAdmin(ImportExportModelAdmin):
    list_display = ('leader__fsp__region', 'title', 'competition', 'leader', 'get_team_members', 'moderation_status')
    list_filter = ('competition', 'moderation_status', "leader__fsp__region")
    search_fields = ("title", 'get_team_members', 'competition')
    resource_classes = [TeamResource]

class FSPResource(resources.ModelResource):
    class Meta:
        model = FSP


class FSPAdmin(ImportExportModelAdmin):
    list_display = ("region", "country", "head")
    search_fields = ("region", "country", "head")

class InviteCompetitionAdmin(admin.ModelAdmin):
    pass

class CompetitionModerationProxy(Competition):
    class Meta:
        proxy = True
        verbose_name = "Заявка на модерацию"
        verbose_name_plural = "Заявки на модерацию"

class ModerationCompetitionAdmin(admin.ModelAdmin):    
    list_display = ('title', 'start_date', 'finish_date', 'place', 'on_moderation', 'competition_type', 'get_fsps')
    list_filter = ('fsps', 'on_moderation')
    search_fields = ("title", 'place')
    actions = ["approve", "reject"]

    def get_fsps(self, obj):
        return "\n".join([str(fsp) for fsp in obj.fsps.all()])

    # Фильтруем queryset
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(on_moderation=OnModerationStatus.PENDING)

    def has_view_permission(self, request, obj=None):
        if request.user.groups.filter(name='Федеральное ФСП').exists() or request.user.is_superuser:
            return request.user.has_perm('rc_app.view_competition')
        return False

    # Кнопки действий
    def approve(self, request, queryset):
        queryset.update(on_moderation=OnModerationStatus.APPROVED)
    approve.short_description = "Одобрить выбранные заявки"

    def reject(self, request, queryset):
        queryset.update(on_moderation=OnModerationStatus.REJECTED)
    reject.short_description = "Отклонить выбранные заявки"


class DisciplineAdmin(admin.ModelAdmin):
    list_display = ("discipline", )


admin.site.register(Competition, CompetitionAdmin)
admin.site.register(CompetitionModerationProxy, ModerationCompetitionAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(CompetitionResult, CompetitionResultAdmin)
admin.site.register(FSP, FSPAdmin)
admin.site.register(InviteCompetition, InviteCompetitionAdmin)
admin.site.register(Discipline, DisciplineAdmin)