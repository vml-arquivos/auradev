"""
Core models for AuraClass.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    """
    ROLE_CHOICES = [
        ('admin', _('Administrador')),
        ('coordenador', _('Coordenador')),
        ('professor', _('Professor')),
        ('aluno', _('Aluno')),
        ('responsavel', _('Responsável')),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='aluno',
        verbose_name=_('Papel')
    )
    bio = models.TextField(blank=True, verbose_name=_('Biografia'))
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name=_('Avatar')
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Telefone')
    )
    is_active = models.BooleanField(default=True, verbose_name=_('Ativo'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))
    
    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"


class AuditLog(models.Model):
    """
    Model to track all changes in the system.
    """
    ACTION_CHOICES = [
        ('create', _('Criação')),
        ('update', _('Atualização')),
        ('delete', _('Exclusão')),
        ('view', _('Visualização')),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs',
        verbose_name=_('Usuário')
    )
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        verbose_name=_('Ação')
    )
    model_name = models.CharField(
        max_length=100,
        verbose_name=_('Nome do Modelo')
    )
    object_id = models.IntegerField(verbose_name=_('ID do Objeto'))
    changes = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('Mudanças')
    )
    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name=_('Endereço IP')
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_('Timestamp'))
    
    class Meta:
        verbose_name = _('Log de Auditoria')
        verbose_name_plural = _('Logs de Auditoria')
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['model_name', 'object_id']),
        ]
    
    def __str__(self):
        return f"{self.user} - {self.get_action_display()} - {self.model_name}"


class Notification(models.Model):
    """
    Model for system notifications.
    """
    PRIORITY_CHOICES = [
        ('low', _('Baixa')),
        ('medium', _('Média')),
        ('high', _('Alta')),
        ('urgent', _('Urgente')),
    ]
    
    STATUS_CHOICES = [
        ('unread', _('Não Lida')),
        ('read', _('Lida')),
        ('archived', _('Arquivada')),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('Usuário')
    )
    title = models.CharField(max_length=255, verbose_name=_('Título'))
    message = models.TextField(verbose_name=_('Mensagem'))
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name=_('Prioridade')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='unread',
        verbose_name=_('Status')
    )
    link = models.URLField(blank=True, verbose_name=_('Link'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    read_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Lido em'))
    
    class Meta:
        verbose_name = _('Notificação')
        verbose_name_plural = _('Notificações')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'status']),
        ]
    
    def __str__(self):
        return f"{self.user} - {self.title}"
