from django.apps import AppConfig


class RcAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rc_backend.rc_app'


def ready(self):
    # noinspection PyUnresolvedReferences
    from . import signals
