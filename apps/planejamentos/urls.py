"""
URLs for Planejamentos app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PlanejamentoTemplateViewSet, AtividadeTemplateViewSet,
    MaterialDidaticoViewSet, ColeçaoPlanejamentosViewSet
)

router = DefaultRouter()
router.register(r'templates', PlanejamentoTemplateViewSet, basename='planejamento-template')
router.register(r'atividades', AtividadeTemplateViewSet, basename='atividade-template')
router.register(r'materiais', MaterialDidaticoViewSet, basename='material-didatico')
router.register(r'colecoes', ColeçaoPlanejamentosViewSet, basename='colecao-planejamentos')

urlpatterns = [
    path('', include(router.urls)),
]
