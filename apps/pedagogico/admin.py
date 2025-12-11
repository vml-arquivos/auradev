"""
Admin configuration for Pedagogico app.
"""
from django.contrib import admin
from .models import (
    Turma, Aluno, PlanejamentoAnual, UnidadeTematica,
    RegistroDeAula, Avaliacao, NotaAluno, Tarefa, SubmissaoTarefa
)


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'nivel_ensino', 'professor', 'ano_letivo', 'ativa']
    list_filter = ['nivel_ensino', 'ano_letivo', 'ativa']
    search_fields = ['nome', 'professor__first_name']


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ['user', 'matricula']
    search_fields = ['user__first_name', 'user__last_name', 'matricula']


@admin.register(PlanejamentoAnual)
class PlanejamentoAnualAdmin(admin.ModelAdmin):
    list_display = ['professor', 'turma', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['professor__first_name', 'turma__nome']


@admin.register(UnidadeTematica)
class UnidadeTematicaAdmin(admin.ModelAdmin):
    list_display = ['planejamento', 'titulo', 'ordem']
    list_filter = ['planejamento']
    search_fields = ['titulo']


@admin.register(RegistroDeAula)
class RegistroDeAulaAdmin(admin.ModelAdmin):
    list_display = ['turma', 'professor', 'data']
    list_filter = ['data', 'turma']
    search_fields = ['titulo', 'professor__first_name']


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ['turma', 'titulo', 'tipo', 'data']
    list_filter = ['tipo', 'data']
    search_fields = ['titulo']


@admin.register(NotaAluno)
class NotaAlunoAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'avaliacao', 'valor']
    list_filter = ['avaliacao']
    search_fields = ['aluno__user__first_name']


@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'turma', 'professor', 'status', 'data_entrega']
    list_filter = ['status', 'data_entrega', 'turma']
    search_fields = ['titulo', 'descricao', 'professor__first_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SubmissaoTarefa)
class SubmissaoTarefaAdmin(admin.ModelAdmin):
    list_display = ['tarefa', 'aluno', 'status', 'nota', 'data_submissao']
    list_filter = ['status', 'data_submissao', 'tarefa']
    search_fields = ['aluno__user__first_name', 'tarefa__titulo']
    readonly_fields = ['data_submissao']
