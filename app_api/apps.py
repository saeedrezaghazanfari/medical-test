from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_api'
    verbose_name = _('ماژول api')
