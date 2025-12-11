"""
App configuration for AuraMind app.
"""
from django.apps import AppConfig


class AuramindConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.auramind'
    verbose_name = 'AuraMind'
