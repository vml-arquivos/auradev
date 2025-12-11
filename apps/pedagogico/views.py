"""
Views for Pedagogico app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import (
    Turma, Aluno, PlanejamentoAnual, UnidadeTematica,
    RegistroDeAula, Avaliacao, NotaAluno
)
from .serializers import (
    TurmaSerializer, AlunoSerializer, PlanejamentoAnualSerializer,
    UnidadeTematicaSerializer, RegistroDeAulaSerializer,
    AvaliacaoSerializer, NotaAlunoSerializer
)


class TurmaViewSet(viewsets.ModelViewSet):
    """ViewSet for Turma model."""
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nivel_ensino', 'ano_letivo', 'semestre', 'ativa']
    search_fields = ['nome', 'professor__first_name']
    ordering_fields = ['nome', 'ano_letivo']


class AlunoViewSet(viewsets.ModelViewSet):
    """ViewSet for Aluno model."""
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['user__first_name', 'user__last_name', 'matricula']


class PlanejamentoAnualViewSet(viewsets.ModelViewSet):
    """ViewSet for PlanejamentoAnual model."""
    queryset = PlanejamentoAnual.objects.all()
    serializer_class = PlanejamentoAnualSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'turma']
    ordering_fields = ['-created_at']
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit planejamento for approval."""
        planejamento = self.get_object()
        planejamento.status = 'pendente'
        planejamento.save()
        
        serializer = self.get_serializer(planejamento)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve planejamento."""
        planejamento = self.get_object()
        planejamento.status = 'aprovado'
        planejamento.save()
        
        serializer = self.get_serializer(planejamento)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject planejamento."""
        planejamento = self.get_object()
        planejamento.status = 'rejeitado'
        planejamento.observacoes_coordenador = request.data.get('observacoes', '')
        planejamento.save()
        
        serializer = self.get_serializer(planejamento)
        return Response(serializer.data)


class UnidadeTematicaViewSet(viewsets.ModelViewSet):
    """ViewSet for UnidadeTematica model."""
    queryset = UnidadeTematica.objects.all()
    serializer_class = UnidadeTematicaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['planejamento']


class RegistroDeAulaViewSet(viewsets.ModelViewSet):
    """ViewSet for RegistroDeAula model."""
    queryset = RegistroDeAula.objects.all()
    serializer_class = RegistroDeAulaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['turma', 'professor', 'data']
    ordering_fields = ['-data']


class AvaliacaoViewSet(viewsets.ModelViewSet):
    """ViewSet for Avaliacao model."""
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['turma', 'tipo']
    search_fields = ['titulo']


class NotaAlunoViewSet(viewsets.ModelViewSet):
    """ViewSet for NotaAluno model."""
    queryset = NotaAluno.objects.all()
    serializer_class = NotaAlunoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['aluno', 'avaliacao']
