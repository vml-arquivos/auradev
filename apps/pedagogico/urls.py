"""
URLs for Pedagogico app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TurmaViewSet, AlunoViewSet, PlanejamentoAnualViewSet,
    UnidadeTematicaViewSet, RegistroDeAulaViewSet,
    AvaliacaoViewSet, NotaAlunoViewSet, TarefaViewSet, SubmissaoTarefaViewSet
)

router = DefaultRouter()
router.register(r'turmas', TurmaViewSet, basename='turma')
router.register(r'alunos', AlunoViewSet, basename='aluno')
router.register(r'planejamentos', PlanejamentoAnualViewSet, basename='planejamento')
router.register(r'unidades-tematicas', UnidadeTematicaViewSet, basename='unidade-tematica')
router.register(r'registros-aula', RegistroDeAulaViewSet, basename='registro-aula')
router.register(r'avaliacoes', AvaliacaoViewSet, basename='avaliacao')
router.register(r'notas', NotaAlunoViewSet, basename='nota')
router.register(r'tarefas', TarefaViewSet, basename='tarefa')
router.register(r'submissoes-tarefas', SubmissaoTarefaViewSet, basename='submissao-tarefa')

urlpatterns = [
    path('', include(router.urls)),
]
