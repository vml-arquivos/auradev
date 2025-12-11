# Changelog - AuraClass

Todas as mudanças significativas neste projeto serão documentadas neste arquivo.

## [Versão 0.2.0] - 2025-12-11

### Adicionado

- **Modelo Escola**: Novo modelo para suportar gestão multi-escola
  - Campos: nome, CNPJ, endereço, diretor
  - Relacionamentos com Turma, Matricula e Funcionario
  
- **Integração n8n**: Webhook para automação de aprovação de planejamentos
  - Função `send_n8n_webhook()` em views.py do módulo Pedagógico
  - Disparo automático ao submeter planejamento anual
  - Configuração via variável de ambiente `N8N_WEBHOOK_URL`

- **Serializers para Administrativo**: Adicionado EscolaSerializer
  - Suporte completo para CRUD de escolas via API

- **ViewSets para Administrativo**: Adicionado EscolaViewSet
  - Endpoints REST para gerenciamento de escolas
  - Filtros por nome e CNPJ

### Modificado

- **Modelo Turma**: Adicionado campo `escola` (ForeignKey)
  - Constraint unique_together atualizado para incluir escola
  - Cada turma agora está vinculada a uma escola específica

- **Modelo Matricula**: Adicionado campo `escola` (ForeignKey)
  - Cada matrícula agora está vinculada a uma escola específica

- **Modelo Funcionario**: Adicionado campo `escola` (ForeignKey)
  - Cada funcionário agora está vinculado a uma escola específica

- **Views Pedagógico**: Integração com webhook n8n
  - Ação `submit()` agora dispara webhook para n8n
  - Logging de sucesso/falha na chamada do webhook

- **Admin Administrativo**: Adicionado EscolaAdmin
  - Interface de administração para gerenciamento de escolas

- **URLs Administrativo**: Adicionado rota para EscolaViewSet
  - Endpoint: `/api/v1/administrativo/escolas/`

### Configuração

- **N8N_WEBHOOK_URL**: Nova variável de ambiente
  - Padrão: `http://localhost:5678/webhook/`
  - Configurável via `.env`

### Documentação

- Atualizado `docs/N8N_SETUP.md` com instruções de configuração
- Adicionados comentários em código para marcar alterações com `# NOVO`

## [Versão 0.1.0] - 2025-12-11

### Adicionado

- Estrutura inicial do projeto Django
- Módulo Core com modelos User, AuditLog e Notification
- Módulo Pedagógico com modelos de turmas, planejamentos e avaliações
- Módulo Administrativo com modelos de matrículas e funcionários
- Módulo AuraMind com integração de IA
- APIs REST completas com autenticação JWT
- Documentação Swagger/OpenAPI
- Testes unitários para Core e Pedagógico
- Configuração Docker com docker-compose
- Documentação de deployment e setup

### Estrutura de Commits

```
063a714 - feat(arch): Implement multi-school (Escola model) and n8n webhook trigger
202a13b - chore(migrations): Add initial migration files for all apps
55127a6 - docs(api,deployment,n8n): Add comprehensive documentation
7f3bec2 - test(core,pedagogico): Add unit tests for core and pedagogico apps
12138c5 - feat(base): Initial commit - Setup Django core, models, API prototype
```

## Próximas Etapas

- [ ] Gerar e aplicar migrações do banco de dados
- [ ] Implementar frontend React/Vue
- [ ] Adicionar mais testes (Administrativo, Pedagógico, AuraMind)
- [ ] Integração com Google Classroom
- [ ] Aplicativo mobile
- [ ] Relatórios avançados
- [ ] Gamificação

## Notas de Implementação

### Multi-Escola

A implementação de multi-escola foi realizada através de:

1. Novo modelo `Escola` no módulo Administrativo
2. ForeignKey `escola` adicionada aos modelos:
   - Turma
   - Matricula
   - Funcionario

3. Constraint `unique_together` atualizado em Turma para incluir escola:
   ```python
   unique_together = ['escola', 'nome', 'ano_letivo', 'semestre']
   ```

### Integração n8n

A integração com n8n foi implementada através de:

1. Função `send_n8n_webhook()` em `apps/pedagogico/views.py`
2. Disparo automático ao submeter planejamento anual
3. Payload contém: plano_id, professor_id, status
4. Webhook URL configurável via variável de ambiente

### Migrações Pendentes

Após estas alterações, execute:

```bash
python manage.py makemigrations administrativo
python manage.py makemigrations pedagogico
python manage.py migrate
```

## Contribuindo

Veja `CONTRIBUTING.md` para diretrizes de contribuição.

## Licença

MIT License - veja `LICENSE` para detalhes.
