# Análise: Rota Pedagógica + Google Sala de Aula

## Visão Geral

Este documento analisa o modelo de negócio e funcionalidades do **Rota Pedagógica** (https://rotapedagogica.com.br/rotapedagogica) e como integrá-lo ao **AuraClass** com funcionalidades simplificadas do **Google Sala de Aula**, potencializados com **IA** e **automações**.

## 1. Análise do Rota Pedagógica

### 1.1 Proposta de Valor

O Rota Pedagógica oferece um repositório de **planejamentos prontos e editáveis** baseados na **BNCC**, permitindo que professores economizem tempo no planejamento de aulas.

**Principais características:**

- **1200+ Planos Diários** - Prontos para uso imediato
- **189 Planejamentos Semanais** - Estruturados por semana
- **Planejamentos Mensais e Anuais** - Visão ampla do ano letivo
- **Materiais Editáveis** - Formato Word para personalização
- **Alinhamento BNCC** - Todos os planos seguem diretrizes pedagógicas
- **Bônus Exclusivos** - 1000 atividades para impressão, kits temáticos, silabários
- **Acesso Vitalício** - Uma compra, acesso permanente
- **Suporte WhatsApp** - Atendimento direto para dúvidas

### 1.2 Estrutura de um Plano de Aula (Rota Pedagógica)

Cada plano contém:

| Elemento | Descrição |
|----------|-----------|
| **Identificação de Habilidades** | Quais habilidades serão desenvolvidas |
| **Campos de Experiências** | Áreas de aprendizagem (BNCC) |
| **Objetivos de Aprendizagem** | O que o aluno deve aprender |
| **Códigos BNCC** | Identificação alfanumérica BNCC |
| **Atividade Dirigida** | Atividade inicial/introdutória |
| **Desenvolvimento** | Conteúdo principal da aula |
| **Atividades para Impressão** | Materiais para distribuir aos alunos |
| **Avaliação** | Como avaliar o aprendizado |

### 1.3 Público-Alvo

- Professores de **Educação Infantil** (0-5 anos)
- Professores de **Ensino Fundamental** (1º ao 5º ano)
- Coordenadores pedagógicos
- Escolas que buscam padronizar planejamentos

### 1.4 Modelo de Negócio

- **Preço**: R$ 197 (ou 7x R$ 5,29)
- **Entrega**: Digital via email
- **Acesso**: Vitalício com atualizações semanais
- **Suporte**: WhatsApp vitalício

## 2. Análise do Google Sala de Aula

### 2.1 Funcionalidades Principais

O Google Sala de Aula é uma plataforma de **gestão de aprendizagem** que simplifica a criação, distribuição e avaliação de tarefas.

**Funcionalidades-chave:**

| Funcionalidade | Descrição |
|----------------|-----------|
| **Turmas** | Criar e gerenciar turmas virtuais |
| **Tarefas** | Atribuir trabalhos aos alunos |
| **Materiais** | Compartilhar recursos (documentos, vídeos, links) |
| **Anúncios** | Comunicar com alunos e responsáveis |
| **Avaliações** | Criar quizzes e testes |
| **Comentários** | Feedback em tempo real |
| **Integração Google** | Docs, Sheets, Slides, YouTube |
| **Relatórios** | Acompanhamento de progresso |

### 2.2 Fluxo de Uso (Simplificado)

```
1. Professor cria turma
2. Alunos se matriculam
3. Professor publica materiais/tarefas
4. Alunos acessam e completam tarefas
5. Professor avalia e fornece feedback
6. Alunos recebem notas e comentários
```

### 2.3 Simplicidade como Diferencial

- Interface intuitiva
- Sem configurações complexas
- Integração com Google Drive
- Acesso via web e mobile
- Gratuito para educadores

## 3. Integração Proposta: AuraClass

### 3.1 Conceito Híbrido

**AuraClass** combinará:

1. **Repositório de Planejamentos** (estilo Rota Pedagógica)
   - Banco de planejamentos BNCC
   - Atividades prontas e editáveis
   - Materiais para impressão

2. **Gestão de Sala de Aula** (estilo Google Sala de Aula)
   - Criar e gerenciar turmas
   - Distribuir tarefas e materiais
   - Acompanhar progresso dos alunos
   - Fornecer feedback

3. **Potencialização com IA** (AuraMind)
   - Sugestões de atividades baseadas em habilidades
   - Análise de planejamentos
   - Geração automática de atividades
   - Recomendações personalizadas

4. **Automações** (n8n)
   - Distribuição automática de materiais
   - Notificações para alunos e responsáveis
   - Geração de relatórios
   - Integração com sistemas externos

### 3.2 Diferenciais do AuraClass

| Aspecto | Rota Pedagógica | Google Sala | AuraClass |
|--------|-----------------|-------------|-----------|
| **Planejamentos BNCC** | ✅ Sim | ❌ Não | ✅ Sim |
| **Gestão de Turmas** | ❌ Não | ✅ Sim | ✅ Sim |
| **IA para Sugestões** | ❌ Não | ❌ Não | ✅ Sim |
| **Automações** | ❌ Não | ❌ Não | ✅ Sim |
| **Acesso Vitalício** | ✅ Sim | ✅ Sim | ✅ Sim |
| **Suporte** | ✅ WhatsApp | ✅ Comunidade | ✅ Integrado |
| **Editável** | ✅ Word | ✅ Google Docs | ✅ Integrado |
| **Gratuito** | ❌ Pago | ✅ Gratuito | 🔄 Freemium |

## 4. Arquitetura de Módulos Propostos

### 4.1 Novo Módulo: `planejamentos`

Responsável por gerenciar planejamentos BNCC, atividades e materiais.

**Modelos:**

```
PlanejamentoTemplate
├── titulo
├── nivel_ensino
├── habilidades_bncc[]
├── campos_experiencia[]
├── objetivos_aprendizagem[]
├── atividade_dirigida (texto)
├── desenvolvimento (texto)
├── atividades_impressao[] (arquivo)
├── avaliacao (texto)
├── autor
├── data_criacao
└── editavel (bool)

AtividadeTemplate
├── titulo
├── descricao
├── tipo (exercicio, projeto, quiz)
├── habilidades_bncc[]
├── dificuldade (facil, medio, dificil)
├── tempo_estimado_min
├── arquivo (PDF/Word)
├── criado_por
└── data_criacao

MaterialDidatico
├── titulo
├── tipo (decoracao, silabario, atividade_impressao)
├── arquivo
├── nivel_ensino
├── tema
├── data_criacao
└── criado_por
```

### 4.2 Extensão do Módulo: `pedagogico`

Adicionar funcionalidades de distribuição de tarefas e acompanhamento.

**Novos Modelos:**

```
Tarefa
├── titulo
├── descricao
├── turma (FK)
├── professor (FK)
├── data_entrega
├── planejamento_template (FK)
├── atividades[] (FK)
├── status (rascunho, publicada, fechada)
├── data_criacao
└── data_atualizacao

SubmissaoTarefa
├── tarefa (FK)
├── aluno (FK)
├── arquivo_enviado
├── data_submissao
├── nota
├── feedback_professor
├── data_avaliacao
└── status (pendente, entregue, avaliada)

AcompanhamentoAluno
├── aluno (FK)
├── turma (FK)
├── tarefas_completas (int)
├── tarefas_pendentes (int)
├── media_notas (decimal)
├── ultimo_acesso (datetime)
├── progresso_habilidades[] (JSON)
└── data_atualizacao
```

### 4.3 Extensão do Módulo: `auramind`

Potencializar com sugestões de atividades e análises.

**Novos Endpoints:**

```
POST /api/v1/auramind/sugerir_atividades/
├── nivel_ensino
├── habilidades_bncc[]
├── tipo_atividade
└── contexto_turma

POST /api/v1/auramind/analisar_planejamento/
├── planejamento_id
├── turma_id
└── feedback_detalhado (bool)

POST /api/v1/auramind/gerar_atividade/
├── habilidade_bncc
├── tipo (exercicio, projeto, quiz)
├── nivel_dificuldade
└── tema_opcional
```

## 5. Fluxo de Uso do AuraClass

### 5.1 Cenário 1: Professor Cria Aula com Planejamento Pronto

```
1. Professor acessa "Planejamentos"
2. Filtra por nível, habilidade BNCC, tema
3. Seleciona planejamento pronto
4. Personaliza (edita campos, adiciona atividades)
5. Cria tarefa na turma
6. Distribui para alunos
7. Acompanha submissões
8. Avalia e fornece feedback
```

### 5.2 Cenário 2: Professor Usa IA para Gerar Atividades

```
1. Professor acessa "Gerar com IA"
2. Seleciona habilidade BNCC e tipo de atividade
3. AuraMind gera 3 opções de atividades
4. Professor escolhe e personaliza
5. Distribui na turma
6. Acompanha respostas
7. IA analisa respostas e sugere intervenções
```

### 5.3 Cenário 3: Automação de Distribuição

```
1. Coordenador cria "Campanha de Distribuição"
2. Seleciona planejamentos e atividades
3. Configura datas e turmas
4. n8n automaticamente:
   - Cria tarefas nas turmas
   - Envia notificações aos professores
   - Acompanha conclusões
   - Gera relatórios
```

## 6. Integrações Propostas

### 6.1 Google Drive / Google Docs

- Armazenar planejamentos editáveis
- Sincronizar alterações em tempo real
- Facilitar compartilhamento

### 6.2 WhatsApp / Telegram

- Notificações de tarefas
- Lembretes de prazos
- Suporte via chatbot

### 6.3 Email

- Envio de planejamentos
- Notificações de submissões
- Relatórios periódicos

### 6.4 Google Classroom (opcional)

- Sincronização bidirecional
- Importar turmas
- Exportar tarefas

## 7. Roadmap de Implementação

### Fase 1: Estrutura Base (Semana 1-2)
- [ ] Criar módulo `planejamentos`
- [ ] Modelos de dados
- [ ] APIs REST básicas
- [ ] Admin interface

### Fase 2: Integração IA (Semana 3-4)
- [ ] Endpoints AuraMind para sugestões
- [ ] Geração de atividades
- [ ] Análise de planejamentos

### Fase 3: Automações n8n (Semana 5-6)
- [ ] Workflows de distribuição
- [ ] Notificações automáticas
- [ ] Geração de relatórios

### Fase 4: Frontend (Semana 7-8)
- [ ] Interface de planejamentos
- [ ] Editor de atividades
- [ ] Dashboard de acompanhamento

### Fase 5: Integrações Externas (Semana 9-10)
- [ ] Google Drive/Docs
- [ ] WhatsApp/Telegram
- [ ] Google Classroom

## 8. Benefícios para o Usuário

### Para Professores

- ⏱️ **Economia de Tempo**: Planejamentos prontos economizam 5-10 horas/semana
- 🎯 **Qualidade Pedagógica**: Alinhamento com BNCC garantido
- 🤖 **Inteligência Artificial**: Sugestões personalizadas de atividades
- 📊 **Acompanhamento**: Visualizar progresso dos alunos em tempo real
- 🔄 **Automações**: Distribuição automática de materiais

### Para Alunos

- 📚 **Acesso Fácil**: Interface intuitiva para acessar tarefas
- 📱 **Multiplataforma**: Web e mobile
- 🎮 **Engajamento**: Atividades variadas e personalizadas
- 📊 **Feedback Rápido**: Avaliações e comentários imediatos
- 🏆 **Progresso Visível**: Acompanhar próprio desempenho

### Para Escolas

- 📋 **Padronização**: Planejamentos consistentes entre professores
- 📈 **Relatórios**: Dados sobre aprendizado por turma/aluno
- 💰 **Economia**: Redução de custos com materiais impressos
- 🔒 **Segurança**: Dados centralizados e seguros
- 🌐 **Escalabilidade**: Funciona para 1 ou 1000 alunos

## 9. Conclusão

O **AuraClass** posicionado como a convergência de:

- **Rota Pedagógica** (planejamentos prontos BNCC)
- **Google Sala de Aula** (gestão simplificada)
- **IA** (AuraMind - sugestões inteligentes)
- **Automações** (n8n - eficiência operacional)

Oferece uma solução **completa, inteligente e automatizada** para educadores, diferenciando-se pela combinação única de funcionalidades que nenhum concorrente oferece isoladamente.
