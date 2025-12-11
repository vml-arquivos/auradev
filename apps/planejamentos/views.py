"""
Views for Planejamentos app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import PlanejamentoTemplate, AtividadeTemplate, MaterialDidatico, ColeçaoPlanejamentos
from .serializers import (
    PlanejamentoTemplateSerializer, AtividadeTemplateSerializer,
    MaterialDidaticoSerializer, ColeçaoPlanejamentosSerializer
)


class PlanejamentoTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet for PlanejamentoTemplate model."""
    queryset = PlanejamentoTemplate.objects.filter(publico=True)
    serializer_class = PlanejamentoTemplateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nivel_ensino', 'publico', 'tema']
    search_fields = ['titulo', 'objetivos_aprendizagem']
    ordering_fields = ['-created_at', 'titulo']

    def get_queryset(self):
        """Retorna planejamentos públicos ou do próprio usuário."""
        if self.request.user.is_authenticated:
            return PlanejamentoTemplate.objects.filter(
                publico=True
            ) | PlanejamentoTemplate.objects.filter(
                autor=self.request.user
            )
        return PlanejamentoTemplate.objects.filter(publico=True)

    def perform_create(self, serializer):
        """Define o autor como o usuário logado."""
        serializer.save(autor=self.request.user)

    @action(detail=True, methods=['post'])
    def duplicar(self, request, pk=None):
        """Cria uma cópia do planejamento para o usuário."""
        original = self.get_object()
        novo_plano = PlanejamentoTemplate.objects.create(
            titulo=f"{original.titulo} (Cópia)",
            nivel_ensino=original.nivel_ensino,
            habilidades_bncc=original.habilidades_bncc,
            campos_experiencia=original.campos_experiencia,
            objetivos_aprendizagem=original.objetivos_aprendizagem,
            atividade_dirigida=original.atividade_dirigida,
            desenvolvimento=original.desenvolvimento,
            atividades_impressao=original.atividades_impressao,
            avaliacao=original.avaliacao,
            autor=request.user,
            editavel=True,
            publico=False,
            tema=original.tema,
        )
        serializer = self.get_serializer(novo_plano)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AtividadeTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet for AtividadeTemplate model."""
    queryset = AtividadeTemplate.objects.filter(publico=True)
    serializer_class = AtividadeTemplateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tipo', 'nivel_ensino', 'dificuldade', 'publico']
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['-created_at', 'tempo_estimado_min']

    def get_queryset(self):
        """Retorna atividades públicas ou do próprio usuário."""
        if self.request.user.is_authenticated:
            return AtividadeTemplate.objects.filter(
                publico=True
            ) | AtividadeTemplate.objects.filter(
                autor=self.request.user
            )
        return AtividadeTemplate.objects.filter(publico=True)

    def perform_create(self, serializer):
        """Define o autor como o usuário logado."""
        serializer.save(autor=self.request.user)


class MaterialDidaticoViewSet(viewsets.ModelViewSet):
    """ViewSet for MaterialDidatico model."""
    queryset = MaterialDidatico.objects.filter(publico=True)
    serializer_class = MaterialDidaticoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tipo', 'nivel_ensino', 'tema', 'publico']
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['-created_at']

    def get_queryset(self):
        """Retorna materiais públicos ou do próprio usuário."""
        if self.request.user.is_authenticated:
            return MaterialDidatico.objects.filter(
                publico=True
            ) | MaterialDidatico.objects.filter(
                autor=self.request.user
            )
        return MaterialDidatico.objects.filter(publico=True)

    def perform_create(self, serializer):
        """Define o autor como o usuário logado."""
        serializer.save(autor=self.request.user)


class ColeçaoPlanejamentosViewSet(viewsets.ModelViewSet):
    """ViewSet for ColeçaoPlanejamentos model."""
    queryset = ColeçaoPlanejamentos.objects.filter(publico=True)
    serializer_class = ColeçaoPlanejamentosSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nivel_ensino', 'publico']
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['-created_at', 'titulo']

    def get_queryset(self):
        """Retorna coleções públicas ou do próprio usuário."""
        if self.request.user.is_authenticated:
            return ColeçaoPlanejamentos.objects.filter(
                publico=True
            ) | ColeçaoPlanejamentos.objects.filter(
                criador=self.request.user
            )
        return ColeçaoPlanejamentos.objects.filter(publico=True)

    def perform_create(self, serializer):
        """Define o criador como o usuário logado."""
        serializer.save(criador=self.request.user)
