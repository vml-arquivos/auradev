"""
Serializers for Planejamentos app.
"""
from rest_framework import serializers
from .models import PlanejamentoTemplate, AtividadeTemplate, MaterialDidatico, ColeçaoPlanejamentos


class PlanejamentoTemplateSerializer(serializers.ModelSerializer):
    """Serializer for PlanejamentoTemplate model."""
    autor_nome = serializers.CharField(source='autor.get_full_name', read_only=True)
    
    class Meta:
        model = PlanejamentoTemplate
        fields = [
            'id', 'titulo', 'nivel_ensino', 'habilidades_bncc',
            'campos_experiencia', 'objetivos_aprendizagem',
            'atividade_dirigida', 'desenvolvimento', 'atividades_impressao',
            'avaliacao', 'autor', 'autor_nome', 'editavel', 'publico', 'tema',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AtividadeTemplateSerializer(serializers.ModelSerializer):
    """Serializer for AtividadeTemplate model."""
    autor_nome = serializers.CharField(source='autor.get_full_name', read_only=True)
    
    class Meta:
        model = AtividadeTemplate
        fields = [
            'id', 'titulo', 'descricao', 'tipo', 'habilidades_bncc',
            'nivel_ensino', 'dificuldade', 'tempo_estimado_min',
            'arquivo', 'autor', 'autor_nome', 'publico',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MaterialDidaticoSerializer(serializers.ModelSerializer):
    """Serializer for MaterialDidatico model."""
    autor_nome = serializers.CharField(source='autor.get_full_name', read_only=True)
    
    class Meta:
        model = MaterialDidatico
        fields = [
            'id', 'titulo', 'tipo', 'descricao', 'arquivo',
            'nivel_ensino', 'tema', 'autor', 'autor_nome', 'publico',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ColeçaoPlanejamentosSerializer(serializers.ModelSerializer):
    """Serializer for ColeçaoPlanejamentos model."""
    planejamentos = PlanejamentoTemplateSerializer(many=True, read_only=True)
    criador_nome = serializers.CharField(source='criador.get_full_name', read_only=True)
    
    class Meta:
        model = ColeçaoPlanejamentos
        fields = [
            'id', 'titulo', 'descricao', 'planejamentos',
            'nivel_ensino', 'criador', 'criador_nome', 'publico',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
