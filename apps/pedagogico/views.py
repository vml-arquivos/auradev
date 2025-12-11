"""Views for Pedagogico app."""
import requests # NOVO
import logging # NOVO
from django.conf import settings # NOVO

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

logger = logging.getLogger(__name__) # NOVO


def send_n8n_webhook(plano_id, professor_id, status_novo):
    """Função auxiliar para disparar o webhook do n8n para aprovação de planos."""
    # O Webhook Trigger deve ser configurado no n8n conforme docs/N8N_SETUP.md
    webhook_url = settings.N8N_WEBHOOK_URL
    plano_pendente_webhook_url = f"{webhook_url}auraclass/plano-pendente" 
    
    payload = {
        "plano_id": plano_id,
        "professor_id": professor_id,
        "status": status_novo
    }
    
    headers = {
        'Content-Type': 'application/json',
        # Em produção, adicionar o N8N_API_KEY no header de autenticação, se necessário
    }
    
    try:
        response = requests.post(plano_pendente_webhook_url, json=payload, headers=headers, timeout=5)
        response.raise_for_status()
        logger.info(f"Webhook n8n disparado com sucesso para Plano {plano_id}.")
        return True
    except requests.RequestException as e:
        logger.error(f"Falha ao disparar webhook n8n para Plano {plano_id}: {e}")
        return False


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
        """Submit planejamento for approval and trigger n8n webhook."""
        planejamento = self.get_object()
        
        # Só muda e dispara se não estiver pendente (evita repetição)
        if planejamento.status != 'pendente':
            planejamento.status = 'pendente'
            planejamento.save()
            
            # Dispara o webhook n8n para iniciar o fluxo de aprovação
            send_n8n_webhook(
                plano_id=planejamento.id,
                professor_id=planejamento.professor.id,
                status_novo='pendente'
            )
        
        serializer = self.get_serializer(planejamento)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
