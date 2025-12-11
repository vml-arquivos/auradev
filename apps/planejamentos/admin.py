"""
Admin configuration for Planejamentos app.
"""
from django.contrib import admin
from .models import PlanejamentoTemplate, AtividadeTemplate, MaterialDidatico, ColeçaoPlanejamentos


@admin.register(PlanejamentoTemplate)
class PlanejamentoTemplateAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'nivel_ensino', 'autor', 'publico', 'created_at']
    list_filter = ['nivel_ensino', 'publico', 'created_at']
    search_fields = ['titulo', 'objetivos_aprendizagem']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'nivel_ensino', 'tema', 'autor')
        }),
        ('BNCC', {
            'fields': ('habilidades_bncc', 'campos_experiencia', 'objetivos_aprendizagem')
        }),
        ('Conteúdo da Aula', {
            'fields': ('atividade_dirigida', 'desenvolvimento', 'atividades_impressao', 'avaliacao')
        }),
        ('Configurações', {
            'fields': ('editavel', 'publico')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AtividadeTemplate)
class AtividadeTemplateAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'nivel_ensino', 'dificuldade', 'tempo_estimado_min', 'publico']
    list_filter = ['tipo', 'nivel_ensino', 'dificuldade', 'publico']
    search_fields = ['titulo', 'descricao']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'tipo', 'nivel_ensino')
        }),
        ('Detalhes Pedagógicos', {
            'fields': ('habilidades_bncc', 'dificuldade', 'tempo_estimado_min')
        }),
        ('Arquivo', {
            'fields': ('arquivo',)
        }),
        ('Configurações', {
            'fields': ('autor', 'publico')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MaterialDidatico)
class MaterialDidaticoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'nivel_ensino', 'tema', 'publico']
    list_filter = ['tipo', 'nivel_ensino', 'publico']
    search_fields = ['titulo', 'descricao']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'tipo', 'descricao', 'nivel_ensino', 'tema')
        }),
        ('Arquivo', {
            'fields': ('arquivo',)
        }),
        ('Configurações', {
            'fields': ('autor', 'publico')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ColeçaoPlanejamentos)
class ColeçaoPlanejamentosAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'nivel_ensino', 'criador', 'publico']
    list_filter = ['nivel_ensino', 'publico']
    search_fields = ['titulo', 'descricao']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['planejamentos']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'nivel_ensino', 'criador')
        }),
        ('Planejamentos', {
            'fields': ('planejamentos',)
        }),
        ('Configurações', {
            'fields': ('publico',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
