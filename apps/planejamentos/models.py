"""
Models for Planejamentos app - Templates de planos de aula, atividades e materiais didáticos.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import User


NIVEL_ENSINO_CHOICES = [
    ('maternal', _('Maternal')),
    ('pre', _('Pré-Escolar')),
    ('1ef', _('1º Ano EF')),
    ('2ef', _('2º Ano EF')),
    ('3ef', _('3º Ano EF')),
    ('4ef', _('4º Ano EF')),
    ('5ef', _('5º Ano EF')),
    ('6ef', _('6º Ano EF')),
    ('7ef', _('7º Ano EF')),
    ('8ef', _('8º Ano EF')),
    ('9ef', _('9º Ano EF')),
    ('1em', _('1º Ano EM')),
    ('2em', _('2º Ano EM')),
    ('3em', _('3º Ano EM')),
]


class PlanejamentoTemplate(models.Model):
    """
    Modelo para templates de planos de aula (estilo Rota Pedagógica).
    Armazena planos mestres alinhados à BNCC que podem ser copiados e personalizados.
    """
    titulo = models.CharField(
        max_length=255,
        verbose_name=_('Título do Plano')
    )
    nivel_ensino = models.CharField(
        max_length=50,
        choices=NIVEL_ENSINO_CHOICES,
        verbose_name=_('Nível de Ensino')
    )
    habilidades_bncc = models.JSONField(
        default=list,
        verbose_name=_('Habilidades BNCC'),
        help_text=_('Ex: ["EF05LP01", "EF05LP02"]')
    )
    campos_experiencia = models.JSONField(
        default=list,
        verbose_name=_('Campos de Experiência'),
        help_text=_('Campos de experiência BNCC para educação infantil')
    )
    objetivos_aprendizagem = models.TextField(
        verbose_name=_('Objetivos de Aprendizagem')
    )
    atividade_dirigida = models.TextField(
        blank=True,
        verbose_name=_('Atividade Dirigida'),
        help_text=_('Atividade inicial/introdutória')
    )
    desenvolvimento = models.TextField(
        verbose_name=_('Desenvolvimento da Aula'),
        help_text=_('Conteúdo principal da aula')
    )
    atividades_impressao = models.TextField(
        blank=True,
        verbose_name=_('Descrição de Atividades para Impressão')
    )
    avaliacao = models.TextField(
        verbose_name=_('Metodologia de Avaliação')
    )
    autor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='planos_criados',
        verbose_name=_('Autor')
    )
    editavel = models.BooleanField(
        default=True,
        verbose_name=_('Permite Edição')
    )
    publico = models.BooleanField(
        default=True,
        verbose_name=_('Público')
    )
    tema = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Tema')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))

    class Meta:
        verbose_name = _('Planejamento Template')
        verbose_name_plural = _('Planejamentos Templates')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['nivel_ensino', '-created_at']),
            models.Index(fields=['publico', '-created_at']),
        ]

    def __str__(self):
        return f"{self.titulo} ({self.get_nivel_ensino_display()})"


class AtividadeTemplate(models.Model):
    """
    Banco de templates de atividades reutilizáveis.
    Podem ser anexadas a planejamentos ou tarefas.
    """
    TIPO_CHOICES = [
        ('exercicio', _('Exercício')),
        ('projeto', _('Projeto')),
        ('quiz', _('Quiz')),
        ('discussao', _('Discussão')),
        ('criativo', _('Atividade Criativa')),
    ]
    DIFICULDADE_CHOICES = [
        ('facil', _('Fácil')),
        ('medio', _('Médio')),
        ('dificil', _('Difícil')),
    ]

    titulo = models.CharField(
        max_length=255,
        verbose_name=_('Título da Atividade')
    )
    descricao = models.TextField(
        verbose_name=_('Descrição')
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name=_('Tipo de Atividade')
    )
    habilidades_bncc = models.JSONField(
        default=list,
        verbose_name=_('Habilidades BNCC')
    )
    nivel_ensino = models.CharField(
        max_length=50,
        choices=NIVEL_ENSINO_CHOICES,
        verbose_name=_('Nível de Ensino')
    )
    dificuldade = models.CharField(
        max_length=10,
        choices=DIFICULDADE_CHOICES,
        default='medio',
        verbose_name=_('Nível de Dificuldade')
    )
    tempo_estimado_min = models.PositiveIntegerField(
        default=30,
        verbose_name=_('Tempo Estimado (minutos)')
    )
    arquivo = models.FileField(
        upload_to='atividades_templates/',
        blank=True,
        null=True,
        verbose_name=_('Arquivo da Atividade')
    )
    autor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='atividades_criadas',
        verbose_name=_('Autor')
    )
    publico = models.BooleanField(
        default=True,
        verbose_name=_('Público')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))

    class Meta:
        verbose_name = _('Atividade Template')
        verbose_name_plural = _('Atividades Templates')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tipo', 'nivel_ensino']),
            models.Index(fields=['publico', '-created_at']),
        ]

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"


class MaterialDidatico(models.Model):
    """
    Materiais didáticos de bônus (kits de decoração, silabários, atividades extras).
    Similar aos bônus oferecidos pelo Rota Pedagógica.
    """
    TIPO_CHOICES = [
        ('decoracao', _('Decoração de Sala')),
        ('silabario', _('Silabário')),
        ('atividade_extra', _('Atividade Extra')),
        ('kit_tematico', _('Kit Temático')),
        ('recurso_visual', _('Recurso Visual')),
    ]

    titulo = models.CharField(
        max_length=255,
        verbose_name=_('Título do Material')
    )
    tipo = models.CharField(
        max_length=50,
        choices=TIPO_CHOICES,
        verbose_name=_('Tipo de Material')
    )
    descricao = models.TextField(
        blank=True,
        verbose_name=_('Descrição')
    )
    arquivo = models.FileField(
        upload_to='materiais_didaticos/',
        verbose_name=_('Arquivo do Material')
    )
    nivel_ensino = models.CharField(
        max_length=50,
        choices=NIVEL_ENSINO_CHOICES,
        verbose_name=_('Nível de Ensino')
    )
    tema = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Tema')
    )
    autor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='materiais_criados',
        verbose_name=_('Autor')
    )
    publico = models.BooleanField(
        default=True,
        verbose_name=_('Público')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))

    class Meta:
        verbose_name = _('Material Didático')
        verbose_name_plural = _('Materiais Didáticos')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tipo', 'nivel_ensino']),
            models.Index(fields=['publico', '-created_at']),
        ]

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"


class ColeçaoPlanejamentos(models.Model):
    """
    Agrupa planejamentos relacionados (ex: "Planejamentos para Educação Infantil 2025").
    Facilita a navegação e descoberta de conteúdo.
    """
    titulo = models.CharField(
        max_length=255,
        verbose_name=_('Título da Coleção')
    )
    descricao = models.TextField(
        blank=True,
        verbose_name=_('Descrição')
    )
    planejamentos = models.ManyToManyField(
        PlanejamentoTemplate,
        related_name='colecoes',
        verbose_name=_('Planejamentos')
    )
    nivel_ensino = models.CharField(
        max_length=50,
        choices=NIVEL_ENSINO_CHOICES,
        verbose_name=_('Nível de Ensino')
    )
    criador = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='colecoes_criadas',
        verbose_name=_('Criador')
    )
    publico = models.BooleanField(
        default=True,
        verbose_name=_('Público')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))

    class Meta:
        verbose_name = _('Coleção de Planejamentos')
        verbose_name_plural = _('Coleções de Planejamentos')
        ordering = ['-created_at']

    def __str__(self):
        return self.titulo
