# Configuração de Automação com n8n

## Visão Geral

O n8n é uma plataforma de automação que permite criar workflows para automatizar tarefas no AuraClass, como aprovação de planos pedagógicos, notificações e integração com sistemas externos.

## Instalação

### Usando Docker

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### Usando npm

```bash
npm install -g n8n
n8n start
```

O n8n estará disponível em `http://localhost:5678`

## Configuração Inicial

1. Acesse `http://localhost:5678`
2. Configure o usuário e senha
3. Configure as credenciais necessárias

## Workflow: Aprovação de Plano Pedagógico

Este workflow automatiza o processo de aprovação de planos pedagógicos.

### Nodes Necessários

1. **Webhook Trigger**: Recebe notificação do Django
2. **HTTP Request**: Recupera dados do plano
3. **AuraMind LLM**: Análise preliminar
4. **Send Email**: Notifica coordenador
5. **Wait for Webhook**: Aguarda decisão
6. **HTTP Request**: Atualiza status
7. **Send Email/Slack**: Notifica professor

### Configuração do Webhook Trigger

```
POST /webhook/auraclass/plano-pendente
```

Payload esperado:

```json
{
  "plano_id": 105,
  "professor_id": 42,
  "status": "PEN"
}
```

### Configuração do HTTP Request (Recuperar Dados)

```
GET https://api.auraclass.com/api/v1/pedagogico/planejamentos/{{ $json.plano_id }}/

Headers:
Authorization: Bearer {{ $env.DJANGO_API_TOKEN }}
```

### Configuração do AuraMind LLM

```
POST https://api.auraclass.com/api/v1/auramind/api/analise_plano/

Body:
{
  "plano_id": {{ $json.id }},
  "nivel_ensino": "{{ $json.nivel_ensino }}",
  "introducao_geral": "{{ $json.introducao_geral }}",
  "unidades_tematicas": {{ $json.unidades_tematicas }}
}
```

### Configuração do Send Email

```
To: {{ $json.coordenador_email }}
Subject: [Aprovação Pendente] Plano de {{ $json.professor_nome }}

Body (HTML):
<h2>Novo Plano Pendente de Aprovação</h2>
<p>Professor: {{ $json.professor_nome }}</p>
<p>Turma: {{ $json.turma_nome }}</p>

<h3>Análise da IA</h3>
<h4>Pontos Fortes:</h4>
<ul>
{{ $json.analise.pontos_fortes.map(p => '<li>' + p + '</li>').join('') }}
</ul>

<h4>Pontos a Revisar:</h4>
<ul>
{{ $json.analise.pontos_a_revisar.map(p => '<li>' + p + '</li>').join('') }}
</ul>

<p>
  <a href="https://n8n.auraclass.com/webhook/approve/{{ $json.plano_id }}">Aprovar</a>
  <a href="https://n8n.auraclass.com/webhook/reject/{{ $json.plano_id }}">Rejeitar</a>
</p>
```

### Configuração do Wait for Webhook

Crie dois webhooks:

- Aprovação: `POST /webhook/approve/{plano_id}`
- Rejeição: `POST /webhook/reject/{plano_id}`

Timeout: 7 dias

### Configuração do HTTP Request (Atualizar Status)

```
PUT https://api.auraclass.com/api/v1/pedagogico/planejamentos/{{ $json.plano_id }}/

Body:
{
  "status": "{{ $json.acao === 'aprovar' ? 'APR' : 'REC' }}",
  "observacoes_coordenador": "{{ $json.observacoes }}"
}
```

### Configuração do Send Email/Slack (Notificação Final)

Notifique o professor sobre a decisão:

```
To: {{ $json.professor_email }}
Subject: [{{ $json.acao === 'aprovar' ? 'APROVADO' : 'REJEITADO' }}] Seu Plano Anual
```

## Variáveis de Ambiente

Configure as seguintes variáveis no n8n:

```
DJANGO_API_TOKEN=seu_token_jwt
DJANGO_API_URL=https://api.auraclass.com
AURAMIND_API_TOKEN=sua_chave_auramind
AURAMIND_API_URL=https://api.auraclass.com/api/v1/auramind/
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
```

## Testando o Workflow

1. Acesse a aba "Execução"
2. Clique em "Testar Webhook"
3. Envie um payload de teste
4. Verifique se o workflow foi executado corretamente

## Monitoramento

### Logs

Acesse a aba "Execução" para ver o histórico de execuções.

### Alertas

Configure alertas para falhas:

1. Vá para "Configurações"
2. Configure notificações por email ou Slack

## Troubleshooting

### Webhook não dispara

Verifique se a URL do webhook está correta e se o firewall permite conexões.

### Erro de autenticação

Verifique se os tokens estão configurados corretamente nas credenciais.

### Timeout

Aumente o timeout se a API está lenta.

## Workflows Adicionais

### Notificação de Falta

Automatize notificações quando um aluno falta:

```
Trigger: Registro de presença atualizado
Action: Enviar email para responsável
```

### Relatório Semanal

Gere relatórios automaticamente:

```
Trigger: Toda segunda-feira às 8:00
Action: Gerar relatório e enviar por email
```

### Sincronização de Dados

Sincronize dados com sistemas externos:

```
Trigger: Dados atualizados no AuraClass
Action: Enviar para Google Sheets ou outro sistema
```

## Backup e Recuperação

### Backup

```bash
# Exportar workflow
n8n export:workflow --id=1 > workflow.json
```

### Restaurar

```bash
# Importar workflow
n8n import:workflow < workflow.json
```

## Suporte

Para dúvidas sobre n8n, consulte a [documentação oficial](https://docs.n8n.io/).

Para problemas específicos do AuraClass, abra uma issue no repositório.
