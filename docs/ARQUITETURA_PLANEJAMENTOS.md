# Arquitetura de Módulos: Planejamentos, Atividades e Materiais

## 1. Visão Geral

Esta arquitetura propõe a criação de um novo módulo (`planejamentos`) e a extensão do módulo existente (`pedagogico`) para incorporar funcionalidades inspiradas no **Rota Pedagógica** e no **Google Sala de Aula**. O objetivo é criar um ecossistema onde professores possam tanto consumir um banco de planos de aula prontos quanto criar e distribuir suas próprias tarefas e materiais.

## 2. Novo Módulo: `planejamentos`

Este novo aplicativo Django será o coração do repositório de conteúdo. Ele conterá os modelos para os planos de aula, atividades e materiais didáticos reutilizáveis.

### 2.1. Modelos de Dados

#### `PlanejamentoTemplate`

Armazena os planos de aula mestres, alinhados à BNCC, que podem ser copiados e personalizados pelos professores.

```python
# apps/planejamentos/models.py

class PlanejamentoTemplate(models.Model):
    """ Modelo para templates de planos de aula (estilo Rota Pedagógica) """
    titulo = models.CharField(max_length=255, verbose_name=_("Título do Plano"))
    nivel_ensino = models.CharField(max_length=50, choices=NIVEL_ENSINO_CHOICES, verbose_name=_("Nível de Ensino"))
    habilidades_bncc = models.JSONField(default=list, verbose_name=_("Habilidades BNCC"))
    campos_experiencia = models.JSONField(default=list, verbose_name=_("Campos de Experiência"))
    objetivos_aprendizagem = models.TextField(verbose_name=_("Objetivos de Aprendizagem"))
    atividade_dirigida = models.TextField(blank=True, verbose_name=_("Atividade Dirigida"))
    desenvolvimento = models.TextField(verbose_name=_("Desenvolvimento da Aula"))
    avaliacao = models.TextField(verbose_name=_("Metodologia de Avaliação"))
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="planos_criados")
    editavel = models.BooleanField(default=True, verbose_name=_("Permite Edição"))
    publico = models.BooleanField(default=True, verbose_name=_("Público"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo
```

#### `AtividadeTemplate`

Um banco de atividades reutilizáveis que podem ser anexadas a planejamentos ou tarefas.

```python
# apps/planejamentos/models.py

class AtividadeTemplate(models.Model):
    """ Banco de templates de atividades reutilizáveis """
    TIPO_CHOICES = [("exercicio", _("Exercício")), ("projeto", _("Projeto")), ("quiz", _("Quiz"))]
    DIFICULDADE_CHOICES = [("facil", _("Fácil")), ("medio", _("Médio")), ("dificil", _("Difícil"))]

    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    habilidades_bncc = models.JSONField(default=list)
    dificuldade = models.CharField(max_length=10, choices=DIFICULDADE_CHOICES, default="medio")
    tempo_estimado_min = models.PositiveIntegerField(default=30)
    arquivo = models.FileField(upload_to="atividades_templates/", blank=True, null=True)
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
```

#### `MaterialDidatico`

Para os materiais bônus, como kits de decoração, atividades para impressão e silabários.

```python
# apps/planejamentos/models.py

class MaterialDidatico(models.Model):
    """ Materiais didáticos de bônus (kits, etc.) """
    TIPO_CHOICES = [("decoracao", _("Decoração")), ("silabario", _("Silabário")), ("atividade_extra", _("Atividade Extra"))]

    titulo = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    arquivo = models.FileField(upload_to="materiais_didaticos/")
    nivel_ensino = models.CharField(max_length=50, choices=NIVEL_ENSINO_CHOICES)
    tema = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
```

## 3. Extensão do Módulo: `pedagogico`

Para incorporar a gestão de sala de aula (estilo Google Classroom), estenderemos o módulo `pedagogico` com modelos para tarefas e submissões.

### 3.1. Novos Modelos de Dados

#### `Tarefa`

Representa uma atividade ou trabalho atribuído a uma turma.

```python
# apps/pedagogico/models.py

class Tarefa(models.Model):
    """ Modelo para tarefas e atividades atribuídas a uma turma """
    STATUS_CHOICES = [("rascunho", _("Rascunho")), ("publicada", _("Publicada")), ("fechada", _("Fechada"))]

    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="tarefas")
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tarefas_criadas")
    data_entrega = models.DateTimeField(null=True, blank=True)
    planejamento_base = models.ForeignKey(PlanejamentoTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    atividades_anexas = models.ManyToManyField(AtividadeTemplate, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="rascunho")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} - {self.turma.nome}"
```

#### `SubmissaoTarefa`

Registra a entrega de uma tarefa por um aluno.

```python
# apps/pedagogico/models.py

class SubmissaoTarefa(models.Model):
    """ Registro da submissão de uma tarefa por um aluno """
    STATUS_CHOICES = [("pendente", _("Pendente")), ("entregue", _("Entregue")), ("avaliada", _("Avaliada"))]

    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name="submissoes")
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissoes")
    arquivo_enviado = models.FileField(upload_to="submissoes_tarefas/", blank=True, null=True)
    texto_enviado = models.TextField(blank=True)
    data_submissao = models.DateTimeField(auto_now_add=True)
    nota = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback_professor = models.TextField(blank=True)
    data_avaliacao = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pendente")

    class Meta:
        unique_together = ["tarefa", "aluno"]

    def __str__(self):
        return f"Submissão de {self.aluno.get_full_name()} para {self.tarefa.titulo}"
```

## 4. APIs REST e Endpoints

Novos endpoints serão criados para gerenciar os novos modelos.

| Módulo | Endpoint | Ações |
|---|---|---|
| `planejamentos` | `/api/v1/planejamentos/templates/` | CRUD para `PlanejamentoTemplate` |
| `planejamentos` | `/api/v1/planejamentos/atividades/` | CRUD para `AtividadeTemplate` |
| `planejamentos` | `/api/v1/planejamentos/materiais/` | CRUD para `MaterialDidatico` |
| `pedagogico` | `/api/v1/pedagogico/tarefas/` | CRUD para `Tarefa` |
| `pedagogico` | `/api/v1/pedagogico/tarefas/{id}/submissoes/` | CRUD para `SubmissaoTarefa` |

## 5. Integração com AuraMind (IA)

O módulo `auramind` será estendido para interagir com os novos modelos.

- **Sugestão de Atividades**: Ao criar uma `Tarefa`, o professor poderá solicitar sugestões de `AtividadeTemplate` baseadas nas habilidades BNCC da turma.
- **Geração de Planos**: O AuraMind poderá gerar um `PlanejamentoTemplate` completo a partir de um prompt simples (ex: "Crie um plano de 2 semanas sobre o ciclo da água para o 4º ano EF").
- **Análise de Submissões**: A IA poderá fazer uma pré-análise de textos enviados pelos alunos em `SubmissaoTarefa`, identificando pontos-chave e possíveis plágios.

## 6. Automações com n8n

- **Distribuição de Materiais**: Um workflow no n8n poderá ser acionado para distribuir `MaterialDidatico` para turmas específicas no início do ano letivo.
- **Notificações de Tarefas**: Ao publicar uma `Tarefa`, um webhook notificará os alunos e responsáveis via email ou WhatsApp.
- **Lembretes de Prazo**: Um workflow agendado verificará tarefas com prazo próximo e enviará lembretes.

## 7. Próximos Passos

1.  **Criar o app `planejamentos`**.
2.  **Implementar os modelos** definidos neste documento.
3.  **Gerar e aplicar as migrações** do banco de dados.
4.  **Criar os Serializers e ViewSets** para os novos modelos.
5.  **Registrar as novas rotas** de API.
6.  **Fazer o commit** das alterações no repositório.
