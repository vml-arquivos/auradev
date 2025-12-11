"""
Models for Pedagogico app.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import User
from apps.administrativo.models import Escola # NOVO: Importar Escola


class Turma(models.Model):
    """
    Model for Class/Grade.
    """
    # NOVO CAMPO: Liga a Turma a uma Escola
    escola = models.ForeignKey(
        Escola,
        on_delete=models.CASCADE,
        related_name='turmas',
        verbose_name=_('Escola'),
        default=1 # Requer valor padrão temporário para migração. Deve ser revisado manualmente.
    )
    
    nome = models.CharField(max_length=100, verbose_name=_('Nome'))
    nivel_ensino = models.CharField(
        max_length=50,
        choices=[
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
        ],
        verbose_name=_('Nível de Ensino')
    )
    professor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='turmas',
        verbose_name=_('Professor')
    )
    ano_letivo = models.IntegerField(verbose_name=_('Ano Letivo'))
    semestre = models.IntegerField(
        choices=[(1, '1º Semestre'), (2, '2º Semestre')],
        verbose_name=_('Semestre')
    )
    descricao = models.TextField(blank=True, verbose_name=_('Descrição'))
    ativa = models.BooleanField(default=True, verbose_name=_('Ativa'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))
    
    class Meta:
        verbose_name = _('Turma')
        verbose_name_plural = _('Turmas')
        ordering = ['nivel_ensino', 'nome']
        # UNIQUE_TOGETHER ATUALIZADO para incluir a Escola
        unique_together = ['escola', 'nome', 'ano_letivo', 'semestre'] 
    
    def __str__(self):
        return f"{self.nome} - {self.ano_letivo}"


class Aluno(models.Model):
    """
    Model for Student.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='aluno_profile',
        verbose_name=_('Usuário')
    )
    matricula = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Matrícula')
    )
    turmas = models.ManyToManyField(
        Turma,
        related_name='alunos',
        verbose_name=_('Turmas')
    )
    data_nascimento = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Data de Nascimento')
    )
    responsavel_nome = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Nome do Responsável')
    )
    responsavel_email = models.EmailField(
        blank=True,
        verbose_name=_('Email do Responsável')
    )
    responsavel_telefone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Telefone do Responsável')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))
    
    class Meta:
        verbose_name = _('Aluno')
        verbose_name_plural = _('Alunos')
        ordering = ['user__first_name']
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.matricula})"


class PlanejamentoAnual(models.Model):
    """
    Model for Annual Planning.
    """
    STATUS_CHOICES = [
        ('rascunho', _('Rascunho')),
        ('pendente', _('Pendente')),
        ('aprovado', _('Aprovado')),
        ('rejeitado', _('Rejeitado')),
        ('em_execucao', _('Em Execução')),
        ('concluido', _('Concluído')),
    ]
    
    professor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='planejamentos',
        verbose_name=_('Professor')
    )
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name='planejamentos',
        verbose_name=_('Turma')
    )
    titulo = models.CharField(max_length=255, verbose_name=_('Título'))
    introducao_geral = models.TextField(verbose_name=_('Introdução Geral'))
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='rascunho',
        verbose_name=_('Status')
    )
    observacoes_coordenador = models.TextField(
        blank=True,
        verbose_name=_('Observações do Coordenador')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))
    
    class Meta:
        verbose_name = _('Planejamento Anual')
        verbose_name_plural = _('Planejamentos Anuais')
        ordering = ['-created_at']
        unique_together = ['professor', 'turma']
    
    def __str__(self):
        return f"{self.professor.get_full_name()} - {self.turma.nome} ({self.get_status_display()})"


class UnidadeTematica(models.Model):
    """
    Model for Thematic Unit.
    """
    planejamento = models.ForeignKey(
        PlanejamentoAnual,
        on_delete=models.CASCADE,
        related_name='unidades_tematicas',
        verbose_name=_('Planejamento')
    )
    titulo = models.CharField(max_length=255, verbose_name=_('Título'))
    descricao = models.TextField(verbose_name=_('Descrição'))
    habilidades_bncc = models.JSONField(
        default=list,
        verbose_name=_('Habilidades BNCC')
    )
    duracao_semanas = models.IntegerField(verbose_name=_('Duração em Semanas'))
    ordem = models.IntegerField(verbose_name=_('Ordem'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))
    
    class Meta:
        verbose_name = _('Unidade Temática')
        verbose_name_plural = _('Unidades Temáticas')
        ordering = ['planejamento', 'ordem']
        unique_together = ['planejamento', 'ordem']
    
    def __str__(self):
        return f"{self.planejamento.turma.nome} - {self.titulo}"


class RegistroDeAula(models.Model):
    """
    Model for Class Record.
    """
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name='registros_aula',
        verbose_name=_('Turma')
    )
    professor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='registros_aula',
        verbose_name=_('Professor')
    )
    data = models.DateField(verbose_name=_('Data'))
    titulo = models.CharField(max_length=255, verbose_name=_('Título'))
    conteudo = models.TextField(verbose_name=_('Conteúdo'))
    habilidades_trabalhadas = models.JSONField(
        default=list,
        verbose_name=_('Habilidades Trabalhadas')
    )
    presenca = models.JSONField(
        default=dict,
        verbose_name=_('Presença')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))
    
    class Meta:
        verbose_name = _('Registro de Aula')
        verbose_name_plural = _('Registros de Aula')
        ordering = ['-data']
        unique_together = ['turma', 'professor', 'data']
    
    def __str__(self):
        return f"{self.turma.nome} - {self.data}"


class Avaliacao(models.Model):
    """
    Model for Assessment/Evaluation.
    """
    TIPO_CHOICES = [
        ('diagnostica', _('Diagnóstica')),
        ('formativa', _('Formativa')),
        ('somativa', _('Somativa')),
    ]
    
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name='avaliacoes',
        verbose_name=_('Turma')
    )
    professor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='avaliacoes',
        verbose_name=_('Professor')
    )
    titulo = models.CharField(max_length=255, verbose_name=_('Título'))
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name=_('Tipo')
    )
    descricao = models.TextField(verbose_name=_('Descrição'))
    data = models.DateField(verbose_name=_('Data'))
    valor_maximo = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10,
        verbose_name=_('Valor Máximo')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))
    
    class Meta:
        verbose_name = _('Avaliação')
        verbose_name_plural = _('Avaliações')
        ordering = ['-data']
    
    def __str__(self):
        return f"{self.turma.nome} - {self.titulo}"


class NotaAluno(models.Model):
    """
    Model for Student Grade.
    """
    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE,
        related_name='notas',
        verbose_name=_('Aluno')
    )
    avaliacao = models.ForeignKey(
        Avaliacao,
        on_delete=models.CASCADE,
        related_name='notas',
        verbose_name=_('Avaliação')
    )
    valor = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_('Valor')
    )
    observacoes = models.TextField(blank=True, verbose_name=_('Observações'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))
    
    class Meta:
        verbose_name = _('Nota do Aluno')
        verbose_name_plural = _('Notas dos Alunos')
        unique_together = ['aluno', 'avaliacao']
    
    def __str__(self):
        return f"{self.aluno.user.get_full_name()} - {self.avaliacao.titulo}: {self.valor}"


class Tarefa(models.Model):
    """
    Model for Tasks/Assignments (estilo Google Classroom).
    Representa uma atividade ou trabalho atribuído a uma turma.
    """
    STATUS_CHOICES = [
        ('rascunho', _('Rascunho')),
        ('publicada', _('Publicada')),
        ('fechada', _('Fechada')),
    ]
    
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name='tarefas',
        verbose_name=_('Turma')
    )
    titulo = models.CharField(max_length=255, verbose_name=_('Título'))
    descricao = models.TextField(verbose_name=_('Descrição'))
    professor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tarefas_criadas',
        verbose_name=_('Professor')
    )
    data_entrega = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Data de Entrega')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='rascunho',
        verbose_name=_('Status')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))
    
    class Meta:
        verbose_name = _('Tarefa')
        verbose_name_plural = _('Tarefas')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.titulo} - {self.turma.nome}"


class SubmissaoTarefa(models.Model):
    """
    Model for Task Submissions.
    Registra a entrega de uma tarefa por um aluno.
    """
    STATUS_CHOICES = [
        ('pendente', _('Pendente')),
        ('entregue', _('Entregue')),
        ('avaliada', _('Avaliada')),
    ]
    
    tarefa = models.ForeignKey(
        Tarefa,
        on_delete=models.CASCADE,
        related_name='submissoes',
        verbose_name=_('Tarefa')
    )
    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE,
        related_name='submissoes_tarefas',
        verbose_name=_('Aluno')
    )
    arquivo_enviado = models.FileField(
        upload_to='submissoes_tarefas/',
        blank=True,
        null=True,
        verbose_name=_('Arquivo Enviado')
    )
    texto_enviado = models.TextField(
        blank=True,
        verbose_name=_('Texto Enviado')
    )
    data_submissao = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Data de Submissão')
    )
    nota = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Nota')
    )
    feedback_professor = models.TextField(
        blank=True,
        verbose_name=_('Feedback do Professor')
    )
    data_avaliacao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Data de Avaliação')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name=_('Status')
    )
    
    class Meta:
        verbose_name = _('Submissão de Tarefa')
        verbose_name_plural = _('Submissões de Tarefas')
        unique_together = ['tarefa', 'aluno']
        ordering = ['-data_submissao']
    
    def __str__(self):
        return f"Submissão de {self.aluno.user.get_full_name()} para {self.tarefa.titulo}"
