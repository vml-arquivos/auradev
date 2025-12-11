"""
Views for AuraMind app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import SugestaoIa, AnaliseIa, LogIa
from .serializers import SugestaoIaSerializer, AnaliseIaSerializer, LogIaSerializer
from .services import AuraMindService


class SugestaoIaViewSet(viewsets.ModelViewSet):
    """ViewSet for SugestaoIa model."""
    queryset = SugestaoIa.objects.all()
    serializer_class = SugestaoIaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tipo', 'status']


class AnaliseIaViewSet(viewsets.ModelViewSet):
    """ViewSet for AnaliseIa model."""
    queryset = AnaliseIa.objects.all()
    serializer_class = AnaliseIaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tipo_analise', 'status']


class LogIaViewSet(viewsets.ModelViewSet):
    """ViewSet for LogIa model."""
    queryset = LogIa.objects.all()
    serializer_class = LogIaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tipo', 'sucesso']


class AuraMindAPIViewSet(viewsets.ViewSet):
    """ViewSet for AuraMind API interactions."""
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def sugestoes_planejamento(self, request):
        """
        Generate pedagogical suggestion.
        """
        try:
            service = AuraMindService()
            plano_data = request.data
            
            resultado = service.gerar_sugestao_planejamento(
                professor=request.user,
                plano_data=plano_data
            )
            
            return Response(resultado, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def analise_plano(self, request):
        """
        Analyze planning.
        """
        try:
            service = AuraMindService()
            plano_data = request.data
            
            resultado = service.analisar_plano(
                professor=request.user,
                plano_data=plano_data
            )
            
            return Response(resultado, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
