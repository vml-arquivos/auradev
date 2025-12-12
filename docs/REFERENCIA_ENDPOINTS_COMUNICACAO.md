# Referência Rápida: Endpoints e Comunicação entre Serviços

## 1. Endpoints Django (Port 8000)

### 1.1 Autenticação

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|---|
| `POST` | `/api/v1/core/token/` | Obter JWT Token | ❌ Nenhuma |
| `POST` | `/api/v1/core/token/refresh/` | Renovar JWT Token | ✅ Token |

**Exemplo de Requisição**:

```bash
curl -X POST http://localhost:8000/api/v1/core/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "professor",
    "password": "senha123"
  }'
```

**Resposta**:

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 1.2 Planejamentos

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|---|
| `GET` | `/api/v1/pedagogico/planejamentos/` | Listar planejamentos | ✅ Token |
| `POST` | `/api/v1/pedagogico/planejamentos/` | Criar planejamento | ✅ Token |
| `GET` | `/api/v1/pedagogico/planejamentos/{id}/` | Obter planejamento | ✅ Token |
| `PUT` | `/api/v1/pedagogico/planejamentos/{id}/` | Atualizar planejamento | ✅ Token |
| `POST` | `/api/v1/pedagogico/planejamentos/{id}/approve/` | Aprovar planejamento | ✅ Token |
| `POST` | `/api/v1/pedagogico/planejamentos/{id}/reject/` | Rejeitar planejamento | ✅ Token |

**Exemplo: Criar Planejamento**:

```bash
curl -X POST http://localhost:8000/api/v1/pedagogico/planejamentos/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "turma": 1,
    "titulo": "Ciclo da Água",
    "introducao_geral": "Introdução ao ciclo da água",
    "status": "rascunho"
  }'
```

**Exemplo: Aprovar Planejamento**:

```bash
curl -X POST http://localhost:8000/api/v1/pedagogico/planejamentos/123/approve/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "observacoes_coordenador": "Excelente plano!"
  }'
```

### 1.3 Tarefas (Google Classroom Style)

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|---|
| `GET` | `/api/v1/pedagogico/tarefas/` | Listar tarefas | ✅ Token |
| `POST` | `/api/v1/pedagogico/tarefas/` | Criar tarefa | ✅ Token |
| `POST` | `/api/v1/pedagogico/tarefas/{id}/publicar/` | Publicar tarefa | ✅ Token |
| `POST` | `/api/v1/pedagogico/tarefas/{id}/fechar/` | Fechar tarefa | ✅ Token |
| `GET` | `/api/v1/pedagogico/submissoes-tarefas/` | Listar submissões | ✅ Token |
| `POST` | `/api/v1/pedagogico/submissoes-tarefas/{id}/avaliar/` | Avaliar submissão | ✅ Token |

**Exemplo: Criar Tarefa**:

```bash
curl -X POST http://localhost:8000/api/v1/pedagogico/tarefas/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "turma": 1,
    "titulo": "Exercício sobre Ciclo da Água",
    "descricao": "Responda as 5 questões sobre o ciclo da água",
    "data_entrega": "2025-12-20T23:59:59Z",
    "status": "rascunho"
  }'
```

### 1.4 Webhooks

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|---|
| `POST` | `/api/v1/pedagogico/webhooks/plano-pendente` | Receber notificação de plano pendente | ❌ Nenhuma |

## 2. Endpoints AuraMind (Port 8001)

### 2.1 Health & Status

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/health` | Verificar saúde do serviço |
| `GET` | `/api/v1/auramind/status/` | Status do agente AuraMind |
| `GET` | `/docs` | Documentação Swagger |
| `GET` | `/redoc` | Documentação ReDoc |

**Exemplo: Health Check**:

```bash
curl http://localhost:8001/health
```

**Resposta**:

```json
{
  "status": "healthy",
  "service": "AuraMind LLM Agent",
  "version": "1.0.0",
  "timestamp": "2025-12-12T15:30:00Z"
}
```

### 2.2 Sugestões de Planejamento

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/api/v1/auramind/sugestoes_planejamento/` | Gerar sugestão de planejamento |

**Requisição**:

```bash
curl -X POST http://localhost:8001/api/v1/auramind/sugestoes_planejamento/ \
  -H "Content-Type: application/json" \
  -d '{
    "nivel_ensino": "4ef",
    "tema": "Ciclo da Água",
    "habilidades_bncc": ["EF04CI02", "EF04CI03"],
    "duracao_semanas": 4,
    "contexto_turma": "Turma com 25 alunos, boa participação"
  }'
```

**Resposta**:

```json
{
  "titulo": "Planejamento: Ciclo da Água (4ef)",
  "introducao": "Este planejamento foi gerado pela IA AuraMind...",
  "unidades_tematicas": [
    {
      "titulo": "Unidade 1: Introdução ao Ciclo da Água",
      "semanas": 1,
      "habilidades": ["EF04CI02"],
      "descricao": "Apresentação e contextualização do tema"
    }
  ],
  "atividades_sugeridas": [...],
  "recursos_necessarios": [...],
  "avaliacoes_propostas": [...],
  "score_aderencia_bncc": 0.92,
  "observacoes": "Planejamento gerado automaticamente..."
}
```

### 2.3 Análise de Plano

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/api/v1/auramind/analise_plano/` | Analisar plano pedagógico |

**Requisição**:

```bash
curl -X POST http://localhost:8001/api/v1/auramind/analise_plano/ \
  -H "Content-Type: application/json" \
  -d '{
    "plano_id": 123,
    "titulo": "Ciclo da Água - 4º Ano",
    "nivel_ensino": "4ef",
    "habilidades_bncc": ["EF04CI02", "EF04CI03"],
    "objetivos_aprendizagem": "Compreender o ciclo da água e suas fases",
    "atividade_dirigida": "Observação de imagens do ciclo da água",
    "desenvolvimento": "Explicação teórica com slides e vídeos",
    "avaliacao": "Quiz e projeto prático"
  }'
```

**Resposta**:

```json
{
  "plano_id": 123,
  "score_geral": 0.88,
  "aderencia_bncc": 0.95,
  "qualidade_pedagogica": 0.85,
  "pontos_fortes": [
    {
      "aspecto": "Alinhamento BNCC",
      "descricao": "O plano está bem alinhado com as habilidades BNCC",
      "impacto": "alto"
    }
  ],
  "pontos_revisar": [
    {
      "aspecto": "Tempo de Aula",
      "descricao": "Considere ajustar o tempo estimado",
      "impacto": "médio"
    }
  ],
  "sugestoes_melhoria": [
    "Adicione mais atividades de diferenciação",
    "Inclua estratégias de engajamento"
  ],
  "recomendacao_final": "APROVADO COM OBSERVAÇÕES",
  "timestamp": "2025-12-12T15:30:00Z"
}
```

## 3. Endpoints n8n (Port 5678)

### 3.1 Interface Web

| URL | Descrição |
|-----|-----------|
| `http://localhost:5678` | Interface web do n8n |
| `http://localhost:5678/api/v1/workflows` | API de workflows |

**Credenciais Padrão**:
- Usuário: `admin`
- Senha: `admin`

### 3.2 Webhooks

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/webhook/auraclass/plano-pendente` | Webhook disparado pelo Django |
| `GET` | `/webhook/auraclass/acao-plano` | Webhook para ação do coordenador |

**Exemplo: Disparar Webhook de Teste**:

```bash
curl -X POST http://localhost:5678/webhook/auraclass/plano-pendente \
  -H "Content-Type: application/json" \
  -d '{
    "plano_id": 123,
    "professor_id": 45,
    "status": "pendente"
  }'
```

## 4. Fluxo de Comunicação Completo

### 4.1 Submissão de Plano (Professor)

```
1. Professor acessa interface web
2. Clica em "Submeter Plano"
3. Envia POST para Django:
   POST /api/v1/pedagogico/planejamentos/123/submit/
   Authorization: Bearer {token}
```

### 4.2 Processamento no Django

```
4. Django recebe requisição
5. Valida dados
6. Salva plano com status = "pendente"
7. Dispara webhook para n8n:
   POST http://localhost:5678/webhook/auraclass/plano-pendente
   {plano_id, professor_id, status}
```

### 4.3 Automação no n8n

```
8. n8n recebe webhook (Node 1)
9. Busca plano no Django (Node 2):
   GET /api/v1/pedagogico/planejamentos/123/
   Authorization: Bearer {token}
10. Envia para análise no AuraMind (Node 3):
    POST /api/v1/auramind/analise_plano/
    {plano_id, titulo, nivel_ensino, ...}
11. Compõe email com resumo (Node 4)
12. Aguarda ação do coordenador (Node 5)
```

### 4.4 Aprovação (Coordenador)

```
13. Coordenador recebe email
14. Clica em "Aprovar"
15. Aciona webhook no n8n:
    GET /webhook/auraclass/acao-plano?plano_id=123&acao=aprovar
```

### 4.5 Finalização no Django

```
16. n8n atualiza status (Node 6):
    POST /api/v1/pedagogico/planejamentos/123/approve/
    Authorization: Bearer {token}
17. Django atualiza plano com status = "aprovado"
18. n8n envia email final (Node 7)
19. Professor recebe notificação
```

## 5. Autenticação e Segurança

### 5.1 JWT Token (Django)

Todos os endpoints do Django (exceto `/token/`) requerem autenticação JWT.

**Header**:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Obter Token**:
```bash
curl -X POST http://localhost:8000/api/v1/core/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "seu_usuario", "password": "sua_senha"}'
```

### 5.2 CORS (AuraMind)

O AuraMind permite CORS de qualquer origem (configurável em produção).

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 6. Variáveis de Ambiente

### 6.1 Django (`.env`)

```env
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@db:5432/auraclass
N8N_WEBHOOK_URL=http://n8n:5678/webhook/
AURAMIND_API_URL=http://auramind_agent:8001/api/v1/auramind/
```

### 6.2 n8n (`.env`)

```env
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=admin
N8N_HOST=localhost
N8N_PORT=5678
N8N_WEBHOOK_URL=http://web:8000/api/v1/pedagogico/webhooks/
```

## 7. Tratamento de Erros

### 7.1 Erros Django

| Status | Descrição |
|--------|-----------|
| `400` | Bad Request - Dados inválidos |
| `401` | Unauthorized - Token inválido |
| `403` | Forbidden - Sem permissão |
| `404` | Not Found - Recurso não existe |
| `500` | Internal Server Error |

### 7.2 Erros AuraMind

| Status | Descrição |
|--------|-----------|
| `400` | Bad Request - Payload inválido |
| `500` | Internal Server Error - Erro na análise |

### 7.3 Erros n8n

| Tipo | Descrição |
|------|-----------|
| `Webhook Error` | Webhook não foi acionado |
| `HTTP Error` | Falha na requisição HTTP |
| `Timeout` | Requisição expirou |

## 8. Monitoramento

### 8.1 Verificar Status dos Serviços

```bash
# Todos os serviços
docker-compose ps

# Logs do Django
docker-compose logs -f web

# Logs do AuraMind
docker-compose logs -f auramind_agent

# Logs do n8n
docker-compose logs -f n8n
```

### 8.2 Testar Conectividade

```bash
# Testar Django
curl http://localhost:8000/api/docs/

# Testar AuraMind
curl http://localhost:8001/health

# Testar n8n
curl http://localhost:5678
```

---

**Data**: 12 de Dezembro de 2025  
**Versão**: 1.0.0  
**Autor**: AuraDev IA
