"""Serializers for Administrativo app."""
from rest_framework import serializers
from .models import Escola, Matricula, Funcionario, Financeiro, Documento


class EscolaSerializer(serializers.ModelSerializer):
    """Serializer for Escola model."""
    class Meta:
        model = Escola
        fields = [
            'id', 'nome', 'cnpj', 'endereco', 'diretor',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MatriculaSerializer(serializers.ModelSerializer):
    """Serializer for Matricula model."""
    class Meta:
        model = Matricula
        fields = [
            'id', 'escola', 'aluno', 'numero_matricula', 'data_matricula',
            'status', 'ano_letivo', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'data_matricula', 'created_at', 'updated_at']


class FuncionarioSerializer(serializers.ModelSerializer):
    """Serializer for Funcionario model."""
    class Meta:
        model = Funcionario
        fields = [
            'id', 'escola', 'user', 'matricula_funcional', 'cargo',
            'data_admissao', 'salario', 'departamento',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FinanceiroSerializer(serializers.ModelSerializer):
    """Serializer for Financeiro model."""
    class Meta:
        model = Financeiro
        fields = [
            'id', 'aluno', 'tipo', 'descricao', 'valor',
            'data_vencimento', 'data_pagamento', 'status',
            'observacoes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DocumentoSerializer(serializers.ModelSerializer):
    """Serializer for Documento model."""
    class Meta:
        model = Documento
        fields = [
            'id', 'usuario', 'tipo', 'numero', 'arquivo',
            'data_expiracao', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
