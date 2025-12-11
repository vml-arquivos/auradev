"""
Models for AuraMind app - IA Integration.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import User


class SugestaoIa(models.Model):
    """
    Model to store AI suggestions.
    """
    TIPO_CHOICES = [
        ('atividade', _('Atividade')),
        ('recurso_didatico', _('Recurso Didático')),
        ('ideia_avaliacao', _('Ideia de Avaliação')),
    ]
    
    STATUS_CHOICES = [
        ('processando', _('Processando')),
        ('concluida', _('Concluída')),
        ('erro', _('Erro')),
    ]
    
    professor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sugestoes_ia',
        verbose_name=_('Professor')
    )
    plano_id = models.IntegerField(verbose_name=_('ID do Plano'))
    habilidade_foco = models.CharField(
        max_length=20,
        verbose_name=_('Habilidade BNCC')
    )
    nivel_ensino = models.CharField(
        max_length=50,
        verbose_name=_('Nível de Ensino')
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name=_('Tipo de Sugestão')
    )
    contexto_previo = models.TextField(
        verbose_name=_('Contexto Prévio')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='processando',
        verbose_name=_('Status')
    )
    titulo_sugestao = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Título da Sugestão')
    )
    conteudo_sugestao = models.TextField(
        blank=True,
        verbose_name=_('Conteúdo da Sugestão')
    )
    habilidades_sugeridas = models.JSONField(
        default=list,
        verbose_name=_('Habilidades Sugeridas')
    )
    custo_token = models.IntegerField(
        default=0,
        verbose_name=_('Custo em Tokens')
    )
    tempo_processamento_ms = models.IntegerField(
        default=0,
        verbose_name=_('Tempo de Processamento (ms)')
    )
    modelo_ia = models.CharField(
        max_length=50,
        default='AuraMind-v3',
        verbose_name=_('Modelo de IA')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))
    
    class Meta:
        verbose_name = _('Sugestão de IA')
        verbose_name_plural = _('Sugestões de IA')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['professor', '-created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.professor.get_full_name()} - {self.get_tipo_display()}"


class AnaliseIa(models.Model):
    """
    Model to store IA analysis results.
    """
    STATUS_CHOICES = [
        ('pendente', _('Pendente')),
        ('concluida', _('Concluída')),
        ('erro', _('Erro')),
    ]
    
    professor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='analises_ia',
        verbose_name=_('Professor')
    )
    plano_id = models.IntegerField(verbose_name=_('ID do Plano'))
    tipo_analise = models.CharField(
        max_length=100,
        verbose_name=_('Tipo de Análise')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name=_('Status')
    )
    pontos_fortes = models.JSONField(
        default=list,
        verbose_name=_('Pontos Fortes')
    )
    pontos_a_revisar = models.JSONField(
        default=list,
        verbose_name=_('Pontos a Revisar')
    )
    recomendacoes = models.TextField(
        blank=True,
        verbose_name=_('Recomendações')
    )
    score_aderencia = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name=_('Score de Aderência')
    )
    custo_token = models.IntegerField(
        default=0,
        verbose_name=_('Custo em Tokens')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))
    
    class Meta:
        verbose_name = _('Análise de IA')
        verbose_name_plural = _('Análises de IA')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.professor.get_full_name()} - {self.tipo_analise}"


class LogIa(models.Model):
    """
    Model to log all IA interactions.
    """
    TIPO_CHOICES = [
        ('sugestao', _('Sugestão')),
        ('analise', _('Análise')),
        ('erro', _('Erro')),
    ]
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='logs_ia',
        verbose_name=_('Usuário')
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name=_('Tipo')
    )
    entrada = models.JSONField(
        verbose_name=_('Entrada')
    )
    saida = models.JSONField(
        default=dict,
        verbose_name=_('Saída')
    )
    custo_token = models.IntegerField(
        default=0,
        verbose_name=_('Custo em Tokens')
    )
    tempo_resposta_ms = models.IntegerField(
        default=0,
        verbose_name=_('Tempo de Resposta (ms)')
    )
    sucesso = models.BooleanField(
        default=True,
        verbose_name=_('Sucesso')
    )
    mensagem_erro = models.TextField(
        blank=True,
        verbose_name=_('Mensagem de Erro')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    
    class Meta:
        verbose_name = _('Log de IA')
        verbose_name_plural = _('Logs de IA')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['usuario', '-created_at']),
            models.Index(fields=['tipo', 'sucesso']),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.created_at}"
