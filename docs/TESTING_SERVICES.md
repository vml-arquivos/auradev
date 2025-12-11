# Guia de Teste e Validação dos Serviços

## 1. Iniciar os Serviços com Docker Compose

```bash
cd /home/ubuntu/auraclass_dev
docker-compose up -d
```

Isso iniciará os seguintes serviços:

| Serviço | Porta | URL | Status |
|---------|-------|-----|--------|
| **PostgreSQL (db)** | 5432 | `postgresql://localhost:5432/auraclass` | Banco de dados |
| **Django (web)** | 8000 | `http://localhost:8000` | API Principal |
| **AuraMind (auramind_agent)** | 8001 | `http://localhost:8001` | Micro-serviço IA |
| **n8n** | 5678 | `http://localhost:5678` | Automação |

## 2. Verificar Status de Cada Serviço

### 2.1 Verificar PostgreSQL

```bash
docker-compose logs db
```

Procure por: `database system is ready to accept connections`

### 2.2 Verificar Django

```bash
docker-compose logs web
```

Procure por: `Starting development server at http://0.0.0.0:8000/`

### 2.3 Verificar AuraMind

```bash
curl http://localhost:8001/health
```

Resposta esperada:

```json
{
  "status": "healthy",
  "service": "AuraMind LLM Agent",
  "version": "1.0.0",
  "timestamp": "2025-12-11T..."
}
```

### 2.4 Verificar n8n

Acesse: `http://localhost:5678`

Login padrão: `admin` / `admin`

## 3. Testar Endpoints da API

### 3.1 Testar Health Check do AuraMind

```bash
curl -X GET http://localhost:8001/health
```

### 3.2 Testar Endpoint de Sugestão de Planejamento

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

Resposta esperada:

```json
{
  "titulo": "Planejamento: Ciclo da Água (4ef)",
  "introducao": "Este planejamento foi gerado pela IA AuraMind...",
  "unidades_tematicas": [...],
  "atividades_sugeridas": [...],
  "recursos_necessarios": [...],
  "avaliacoes_propostas": [...],
  "score_aderencia_bncc": 0.92,
  "observacoes": "Planejamento gerado automaticamente..."
}
```

### 3.3 Testar Endpoint de Análise de Plano

```bash
curl -X POST http://localhost:8001/api/v1/auramind/analise_plano/ \
  -H "Content-Type: application/json" \
  -d '{
    "plano_id": 1,
    "titulo": "Ciclo da Água - 4º Ano",
    "nivel_ensino": "4ef",
    "habilidades_bncc": ["EF04CI02", "EF04CI03"],
    "objetivos_aprendizagem": "Compreender o ciclo da água...",
    "atividade_dirigida": "Observação de imagens do ciclo da água",
    "desenvolvimento": "Explicação teórica e prática com experimentos",
    "avaliacao": "Quiz e projeto prático"
  }'
```

Resposta esperada:

```json
{
  "plano_id": 1,
  "score_geral": 0.88,
  "aderencia_bncc": 0.95,
  "qualidade_pedagogica": 0.85,
  "pontos_fortes": [...],
  "pontos_revisar": [...],
  "sugestoes_melhoria": [...],
  "recomendacao_final": "APROVADO COM OBSERVAÇÕES...",
  "timestamp": "2025-12-11T..."
}
```

## 4. Testar API Django

### 4.1 Obter Token JWT

```bash
curl -X POST http://localhost:8000/api/v1/core/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "seu_usuario",
    "password": "sua_senha"
  }'
```

### 4.2 Listar Planejamentos

```bash
curl -X GET http://localhost:8000/api/v1/pedagogico/planejamentos/ \
  -H "Authorization: Bearer SEU_TOKEN"
```

### 4.3 Criar Planejamento

```bash
curl -X POST http://localhost:8000/api/v1/pedagogico/planejamentos/ \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "turma": 1,
    "titulo": "Ciclo da Água",
    "introducao_geral": "Introdução ao ciclo da água",
    "status": "rascunho"
  }'
```

## 5. Testar Webhook n8n

### 5.1 Disparar Webhook de Teste

```bash
curl -X POST http://localhost:5678/webhook/auraclass/plano-pendente \
  -H "Content-Type: application/json" \
  -d '{
    "plano_id": 1,
    "professor_id": 1,
    "status": "pendente"
  }'
```

Isso deve iniciar o workflow no n8n.

## 6. Verificar Logs

### 6.1 Logs do Django

```bash
docker-compose logs -f web
```

### 6.2 Logs do AuraMind

```bash
docker-compose logs -f auramind_agent
```

### 6.3 Logs do n8n

```bash
docker-compose logs -f n8n
```

## 7. Parar os Serviços

```bash
docker-compose down
```

Para remover volumes também:

```bash
docker-compose down -v
```

## 8. Troubleshooting

### Erro: "Connection refused"

Verifique se todos os serviços estão rodando:

```bash
docker-compose ps
```

### Erro: "Port already in use"

Mude a porta no `docker-compose.yml` ou libere a porta:

```bash
# Encontrar processo usando a porta
lsof -i :8001

# Matar processo
kill -9 PID
```

### Erro: "Database connection failed"

Aguarde alguns segundos para o PostgreSQL iniciar:

```bash
docker-compose logs db
```

### AuraMind não responde

Verifique se o serviço está rodando:

```bash
docker-compose logs auramind_agent
```

## 9. Checklist de Validação

- [ ] PostgreSQL está healthy
- [ ] Django está rodando na porta 8000
- [ ] AuraMind está respondendo na porta 8001
- [ ] n8n está acessível na porta 5678
- [ ] Endpoint `/health` do AuraMind retorna status "healthy"
- [ ] Endpoint de sugestão retorna resposta válida
- [ ] Endpoint de análise retorna resposta válida
- [ ] Webhook n8n dispara corretamente
- [ ] Logs não mostram erros críticos

## 10. Próximos Passos

Após validar todos os serviços:

1. Configurar credenciais no n8n
2. Importar workflow de aprovação de planos
3. Testar fluxo E2E completo
4. Configurar emails reais
5. Deploy em produção
