"""
Serializers for AuraMind app.
"""
from rest_framework import serializers
from .models import SugestaoIa, AnaliseIa, LogIa


class SugestaoIaSerializer(serializers.ModelSerializer):
    """Serializer for SugestaoIa model."""
    class Meta:
        model = SugestaoIa
        fields = [
            'id', 'professor', 'plano_id', 'habilidade_foco',
            'nivel_ensino', 'tipo', 'contexto_previo', 'status',
            'titulo_sugestao', 'conteudo_sugestao', 'habilidades_sugeridas',
            'custo_token', 'tempo_processamento_ms', 'modelo_ia',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AnaliseIaSerializer(serializers.ModelSerializer):
    """Serializer for AnaliseIa model."""
    class Meta:
        model = AnaliseIa
        fields = [
            'id', 'professor', 'plano_id', 'tipo_analise', 'status',
            'pontos_fortes', 'pontos_a_revisar', 'recomendacoes',
            'score_aderencia', 'custo_token', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LogIaSerializer(serializers.ModelSerializer):
    """Serializer for LogIa model."""
    class Meta:
        model = LogIa
        fields = [
            'id', 'usuario', 'tipo', 'entrada', 'saida',
            'custo_token', 'tempo_resposta_ms', 'sucesso',
            'mensagem_erro', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
