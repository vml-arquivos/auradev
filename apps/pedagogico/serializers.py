"""
Serializers for Pedagogico app.
"""
from rest_framework import serializers
from .models import (
    Turma, Aluno, PlanejamentoAnual, UnidadeTematica,
    RegistroDeAula, Avaliacao, NotaAluno
)


class TurmaSerializer(serializers.ModelSerializer):
    """Serializer for Turma model."""
    class Meta:
        model = Turma
        fields = [
            'id', 'nome', 'nivel_ensino', 'professor', 'ano_letivo',
            'semestre', 'descricao', 'ativa', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AlunoSerializer(serializers.ModelSerializer):
    """Serializer for Aluno model."""
    class Meta:
        model = Aluno
        fields = [
            'id', 'user', 'matricula', 'turmas', 'data_nascimento',
            'responsavel_nome', 'responsavel_email', 'responsavel_telefone',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UnidadeTematicaSerializer(serializers.ModelSerializer):
    """Serializer for UnidadeTematica model."""
    class Meta:
        model = UnidadeTematica
        fields = [
            'id', 'planejamento', 'titulo', 'descricao', 'habilidades_bncc',
            'duracao_semanas', 'ordem', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PlanejamentoAnualSerializer(serializers.ModelSerializer):
    """Serializer for PlanejamentoAnual model."""
    unidades_tematicas = UnidadeTematicaSerializer(many=True, read_only=True)
    
    class Meta:
        model = PlanejamentoAnual
        fields = [
            'id', 'professor', 'turma', 'titulo', 'introducao_geral',
            'status', 'observacoes_coordenador', 'unidades_tematicas',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RegistroDeAulaSerializer(serializers.ModelSerializer):
    """Serializer for RegistroDeAula model."""
    class Meta:
        model = RegistroDeAula
        fields = [
            'id', 'turma', 'professor', 'data', 'titulo', 'conteudo',
            'habilidades_trabalhadas', 'presenca', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AvaliacaoSerializer(serializers.ModelSerializer):
    """Serializer for Avaliacao model."""
    class Meta:
        model = Avaliacao
        fields = [
            'id', 'turma', 'professor', 'titulo', 'tipo', 'descricao',
            'data', 'valor_maximo', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class NotaAlunoSerializer(serializers.ModelSerializer):
    """Serializer for NotaAluno model."""
    class Meta:
        model = NotaAluno
        fields = [
            'id', 'aluno', 'avaliacao', 'valor', 'observacoes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
