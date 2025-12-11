"""
Models for Administrativo app.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import User


class Matricula(models.Model):
    """
    Model for Student Enrollment.
    """
    STATUS_CHOICES = [
        ('ativa', _('Ativa')),
        ('trancada', _('Trancada')),
        ('cancelada', _('Cancelada')),
        ('concluida', _('Concluída')),
    ]
    
    aluno = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='matriculas',
        verbose_name=_('Aluno')
    )
    numero_matricula = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Número de Matrícula')
    )
    data_matricula = models.DateField(
        auto_now_add=True,
        verbose_name=_('Data de Matrícula')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ativa',
        verbose_name=_('Status')
    )
    ano_letivo = models.IntegerField(verbose_name=_('Ano Letivo'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))
    
    class Meta:
        verbose_name = _('Matrícula')
        verbose_name_plural = _('Matrículas')
        ordering = ['-data_matricula']
    
    def __str__(self):
        return f"{self.aluno.get_full_name()} - {self.numero_matricula}"


class Funcionario(models.Model):
    """
    Model for Employee/Staff.
    """
    CARGO_CHOICES = [
        ('professor', _('Professor')),
        ('coordenador', _('Coordenador')),
        ('diretor', _('Diretor')),
        ('secretario', _('Secretário')),
        ('auxiliar', _('Auxiliar')),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='funcionario_profile',
        verbose_name=_('Usuário')
    )
    matricula_funcional = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Matrícula Funcional')
    )
    cargo = models.CharField(
        max_length=50,
        choices=CARGO_CHOICES,
        verbose_name=_('Cargo')
    )
    data_admissao = models.DateField(verbose_name=_('Data de Admissão'))
    salario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Salário')
    )
    departamento = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Departamento')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))
    
    class Meta:
        verbose_name = _('Funcionário')
        verbose_name_plural = _('Funcionários')
        ordering = ['user__first_name']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_cargo_display()}"


class Financeiro(models.Model):
    """
    Model for Financial Management.
    """
    TIPO_CHOICES = [
        ('mensalidade', _('Mensalidade')),
        ('taxa', _('Taxa')),
        ('uniforme', _('Uniforme')),
        ('material', _('Material')),
        ('outro', _('Outro')),
    ]
    
    STATUS_CHOICES = [
        ('pendente', _('Pendente')),
        ('pago', _('Pago')),
        ('atrasado', _('Atrasado')),
        ('cancelado', _('Cancelado')),
    ]
    
    aluno = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='financeiros',
        verbose_name=_('Aluno')
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name=_('Tipo')
    )
    descricao = models.CharField(max_length=255, verbose_name=_('Descrição'))
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Valor')
    )
    data_vencimento = models.DateField(verbose_name=_('Data de Vencimento'))
    data_pagamento = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Data de Pagamento')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name=_('Status')
    )
    observacoes = models.TextField(blank=True, verbose_name=_('Observações'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))
    
    class Meta:
        verbose_name = _('Financeiro')
        verbose_name_plural = _('Financeiros')
        ordering = ['-data_vencimento']
    
    def __str__(self):
        return f"{self.aluno.get_full_name()} - {self.get_tipo_display()}: R$ {self.valor}"


class Documento(models.Model):
    """
    Model for Document Management.
    """
    TIPO_CHOICES = [
        ('rg', _('RG')),
        ('cpf', _('CPF')),
        ('certidao', _('Certidão de Nascimento')),
        ('comprovante_endereco', _('Comprovante de Endereço')),
        ('outro', _('Outro')),
    ]
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='documentos',
        verbose_name=_('Usuário')
    )
    tipo = models.CharField(
        max_length=50,
        choices=TIPO_CHOICES,
        verbose_name=_('Tipo')
    )
    numero = models.CharField(max_length=50, verbose_name=_('Número'))
    arquivo = models.FileField(
        upload_to='documentos/',
        verbose_name=_('Arquivo')
    )
    data_expiracao = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Data de Expiração')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))
    
    class Meta:
        verbose_name = _('Documento')
        verbose_name_plural = _('Documentos')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.get_tipo_display()}"
