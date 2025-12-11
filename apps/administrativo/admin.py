"""
Admin configuration for Administrativo app.
"""
from django.contrib import admin
from .models import Matricula, Funcionario, Financeiro, Documento


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'numero_matricula', 'status', 'ano_letivo']
    list_filter = ['status', 'ano_letivo']
    search_fields = ['aluno__first_name', 'numero_matricula']


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'cargo', 'data_admissao']
    list_filter = ['cargo']
    search_fields = ['user__first_name', 'matricula_funcional']


@admin.register(Financeiro)
class FinanceiroAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'tipo', 'valor', 'status', 'data_vencimento']
    list_filter = ['tipo', 'status', 'data_vencimento']
    search_fields = ['aluno__first_name']


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo', 'numero']
    list_filter = ['tipo']
    search_fields = ['usuario__first_name', 'numero']
