# Guia de Contribuição - AuraClass

Obrigado por considerar contribuir para o AuraClass! Este documento fornece diretrizes e instruções para contribuir com o projeto.

## Código de Conduta

Este projeto adota um código de conduta inclusivo. Todos os contribuidores são esperados a manter um ambiente respeitoso e profissional.

## Como Contribuir

### Relatando Bugs

Antes de criar um relatório de bug, verifique a lista de issues, pois você pode descobrir que o bug já foi relatado. Ao criar um relatório de bug, inclua o máximo de detalhes possível:

- Use um título descritivo
- Descreva os passos exatos para reproduzir o problema
- Forneça exemplos específicos para demonstrar os passos
- Descreva o comportamento observado e o que você esperava ver
- Inclua screenshots ou gifs animados se possível
- Mencione sua versão do Python, Django e sistema operacional

### Sugerindo Melhorias

Sugestões de melhorias são sempre bem-vindas. Ao criar uma sugestão de melhoria, inclua:

- Um título descritivo
- Uma descrição detalhada da melhoria sugerida
- Exemplos de como a melhoria seria usada
- Uma explicação do porquê essa melhoria seria útil

### Pull Requests

- Preencha o modelo de pull request fornecido
- Siga o guia de estilo Python (PEP 8)
- Inclua testes apropriados
- Atualize a documentação conforme necessário
- Termine todos os arquivos com uma nova linha

## Guia de Estilo

### Python

Seguimos o PEP 8 com algumas exceções:

- Comprimento máximo de linha: 100 caracteres
- Use type hints quando possível
- Docstrings em formato Google

```python
def exemplo_funcao(parametro: str) -> str:
    """
    Descrição breve da função.
    
    Args:
        parametro: Descrição do parâmetro
    
    Returns:
        Descrição do retorno
    """
    return parametro
```

### Commits

Seguimos a convenção de Conventional Commits:

```
<tipo>(<escopo>): <descrição>

<corpo>

<rodapé>
```

Tipos válidos: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`

Exemplos:

```
feat(pedagogico): Adicionar endpoint de planejamento anual
fix(auramind): Corrigir timeout na chamada da API
docs(readme): Atualizar instruções de instalação
```

### Branches

- `main`: Código pronto para produção
- `develop`: Código em desenvolvimento
- `feature/*`: Novas funcionalidades
- `fix/*`: Correções de bugs
- `docs/*`: Atualizações de documentação

## Processo de Desenvolvimento

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'feat(escopo): Add AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Executando Testes Localmente

```bash
# Instalar dependências de desenvolvimento
pip install -r requirements.txt

# Executar testes
pytest

# Executar testes com cobertura
pytest --cov=apps --cov-report=html

# Verificar formatação
black --check .
flake8 .
isort --check-only .
```

## Configurar Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

Isso executará verificações automaticamente antes de cada commit.

## Documentação

- Documente novas funcionalidades com docstrings
- Atualize o README.md se necessário
- Adicione exemplos de uso para novas APIs

## Perguntas?

Sinta-se à vontade para abrir uma issue com a tag `question` ou entre em contato através de dev@auraclass.com

Obrigado por contribuir!
