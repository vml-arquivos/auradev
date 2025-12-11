"""
URLs for AuraMind app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SugestaoIaViewSet, AnaliseIaViewSet, LogIaViewSet,
    AuraMindAPIViewSet
)

router = DefaultRouter()
router.register(r'sugestoes', SugestaoIaViewSet, basename='sugestao-ia')
router.register(r'analises', AnaliseIaViewSet, basename='analise-ia')
router.register(r'logs', LogIaViewSet, basename='log-ia')
router.register(r'api', AuraMindAPIViewSet, basename='auramind-api')

urlpatterns = [
    path('', include(router.urls)),
]
