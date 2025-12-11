"""
Admin configuration for AuraMind app.
"""
from django.contrib import admin
from .models import SugestaoIa, AnaliseIa, LogIa


@admin.register(SugestaoIa)
class SugestaoIaAdmin(admin.ModelAdmin):
    list_display = ['professor', 'tipo', 'status', 'created_at']
    list_filter = ['tipo', 'status', 'created_at']
    search_fields = ['professor__first_name', 'titulo_sugestao']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(AnaliseIa)
class AnaliseIaAdmin(admin.ModelAdmin):
    list_display = ['professor', 'tipo_analise', 'status', 'score_aderencia']
    list_filter = ['tipo_analise', 'status']
    search_fields = ['professor__first_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(LogIa)
class LogIaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo', 'sucesso', 'created_at']
    list_filter = ['tipo', 'sucesso', 'created_at']
    search_fields = ['usuario__first_name']
    readonly_fields = ['created_at']
