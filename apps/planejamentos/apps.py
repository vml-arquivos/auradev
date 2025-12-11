"""
App configuration for Planejamentos app.
"""
from django.apps import AppConfig


class PlanejamentosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.planejamentos'
    verbose_name = 'Planejamentos'
