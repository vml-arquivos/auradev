# Documentação da API AuraMind

## Visão Geral

O AuraMind é um agente de inteligência artificial integrado ao AuraClass que fornece sugestões pedagógicas acionáveis aos professores. Esta documentação descreve como integrar e usar a API do AuraMind.

## Endpoint Principal

```
POST /api/v1/auramind/api/sugestoes_planejamento/
```

## Autenticação

Todas as requisições devem incluir um token JWT no header:

```
Authorization: Bearer {seu_token_jwt}
Content-Type: application/json
```

## Payload de Requisição

```json
{
  "plano_id": 105,
  "professor_id": 42,
  "nivel_ensino": "5º Ano EF",
  "habilidade_foco": "EF05LP01",
  "contexto_previo": "Trabalhamos com gêneros textuais narrativos...",
  "formato_desejado": "atividade",
  "parametros_adicionais": {
    "duracao_estimada_min": 45,
    "recursos_disponiveis": ["projetor", "computadores"]
  }
}
```

## Resposta de Sucesso

```json
{
  "status": "sucesso",
  "mensagem": "Sugestão pedagógica gerada com sucesso",
  "dados_sugeridos": {
    "titulo": "Explorando Textos Argumentativos",
    "sugestao_texto": "Crie um debate em sala sobre um tema atual...",
    "habilidades_sugeridas": ["EF05LP03", "EF05LP04"],
    "recursos_necessarios": ["projetor", "computadores"],
    "etapas_execucao": [
      "Apresentar o tema",
      "Dividir a turma em grupos",
      "Debate estruturado"
    ],
    "tempo_estimado_min": 50,
    "dificuldade": "média"
  },
  "metadata": {
    "modelo_ia": "AuraMind-v3",
    "custo_token": 1250,
    "timestamp": "2025-12-11T10:30:00Z"
  }
}
```

## Tipos de Sugestão

- `atividade`: Atividades pedagógicas
- `recurso_didatico`: Recursos e materiais didáticos
- `ideia_avaliacao`: Ideias para avaliações

## Níveis de Ensino Suportados

- Maternal
- Pré-Escolar
- 1º ao 9º Ano EF
- 1º ao 3º Ano EM

## Códigos BNCC

Utilize códigos BNCC válidos para o nível de ensino selecionado. Exemplos:

- EF05LP01 (5º Ano - Língua Portuguesa)
- EI02EO01 (Educação Infantil - Educação Emocional)

## Tratamento de Erros

### Erro 400 - Requisição Inválida

```json
{
  "status": "erro",
  "codigo_erro": "INVALID_HABILIDADE_BNCC",
  "detalhes": "Código BNCC inválido para o nível selecionado"
}
```

### Erro 401 - Não Autenticado

```json
{
  "status": "erro",
  "codigo_erro": "AUTENTICACAO_FALHOU",
  "detalhes": "Token JWT inválido ou expirado"
}
```

### Erro 500 - Erro Interno

```json
{
  "status": "erro",
  "codigo_erro": "ERRO_INTERNO_SERVIDOR",
  "detalhes": "Erro ao processar requisição"
}
```

## Exemplo de Uso com Python

```python
import requests
from django.conf import settings

class AuraMindClient:
    def __init__(self, token):
        self.base_url = settings.AURAMIND_API_URL
        self.token = token
    
    def gerar_sugestao(self, plano_data):
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            f'{self.base_url}sugestoes_planejamento/',
            json=plano_data,
            headers=headers,
            timeout=60
        )
        
        response.raise_for_status()
        return response.json()

# Uso
client = AuraMindClient(token='seu_token_aqui')
sugestao = client.gerar_sugestao({
    'plano_id': 105,
    'professor_id': 42,
    'nivel_ensino': '5º Ano EF',
    'habilidade_foco': 'EF05LP01',
    'contexto_previo': 'Conteúdo anterior...',
    'formato_desejado': 'atividade'
})
```

## Limites e Quotas

- Limite por usuário: 100 requisições por hora
- Timeout: 60 segundos
- Tamanho máximo de payload: 1MB

## Boas Práticas

1. Sempre valide o código BNCC antes de enviar
2. Implemente retry logic com backoff exponencial
3. Cache resultados para evitar requisições duplicadas
4. Monitore o custo de tokens para otimizar custos
5. Use tratamento de erro apropriado

## Suporte

Para dúvidas ou problemas, abra uma issue no repositório ou entre em contato através de dev@auraclass.com
