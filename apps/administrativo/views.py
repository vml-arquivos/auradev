"""
Views for Administrativo app.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Matricula, Funcionario, Financeiro, Documento
from .serializers import (
    MatriculaSerializer, FuncionarioSerializer,
    FinanceiroSerializer, DocumentoSerializer
)


class MatriculaViewSet(viewsets.ModelViewSet):
    """ViewSet for Matricula model."""
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status', 'ano_letivo']
    search_fields = ['aluno__first_name', 'numero_matricula']


class FuncionarioViewSet(viewsets.ModelViewSet):
    """ViewSet for Funcionario model."""
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['cargo']
    search_fields = ['user__first_name', 'matricula_funcional']


class FinanceiroViewSet(viewsets.ModelViewSet):
    """ViewSet for Financeiro model."""
    queryset = Financeiro.objects.all()
    serializer_class = FinanceiroSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['tipo', 'status']
    ordering_fields = ['-data_vencimento']


class DocumentoViewSet(viewsets.ModelViewSet):
    """ViewSet for Documento model."""
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['tipo']
    search_fields = ['numero']
