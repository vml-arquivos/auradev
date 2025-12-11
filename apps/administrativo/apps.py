"""
App configuration for Administrativo app.
"""
from django.apps import AppConfig


class AdministrativoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.administrativo'
    verbose_name = 'Administrativo'
