"""
URLs for Administrativo app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EscolaViewSet, MatriculaViewSet, FuncionarioViewSet,
    FinanceiroViewSet, DocumentoViewSet
)

router = DefaultRouter()
router.register(r'escolas', EscolaViewSet, basename='escola')
router.register(r'matriculas', MatriculaViewSet, basename='matricula')
router.register(r'funcionarios', FuncionarioViewSet, basename='funcionario')
router.register(r'financeiro', FinanceiroViewSet, basename='financeiro')
router.register(r'documentos', DocumentoViewSet, basename='documento')

urlpatterns = [
    path('', include(router.urls)),
]
