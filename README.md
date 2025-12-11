# AuraClass - Sistema Integrado de Gestão Educacional

AuraClass é um Sistema Integrado de Gestão Educacional (LMS/ERP) que combina funcionalidades de gerenciamento pedagógico, administrativo e integração com inteligência artificial.

## Características

- **Módulo Pedagógico**: Gerenciamento de cursos, aulas, avaliações e planejamento anual
- **Módulo Administrativo**: Gestão de alunos, professores, matrículas e RH
- **Módulo IA (AuraMind)**: Agente de inteligência artificial para sugestões pedagógicas
- **Automação (n8n)**: Workflows automatizados para reduzir esforço administrativo
- **API REST**: Endpoints completos para integração com frontend e terceiros

## Tecnologias

- **Backend**: Django 4.2.7 + Django REST Framework
- **Database**: PostgreSQL (SQLite para desenvolvimento)
- **IA**: OpenAI API + AuraMind Agent
- **Automação**: n8n
- **Autenticação**: JWT (djangorestframework-simplejwt)
- **Documentação**: Swagger/OpenAPI (drf-spectacular)

## Instalação

### Pré-requisitos

- Python 3.8+
- PostgreSQL 12+ (opcional, SQLite para desenvolvimento)
- Git

### Passos

1. **Clone o repositório**

```bash
git clone https://github.com/vml-arquivos/auradev.git
cd auradev
```

2. **Crie um virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

4. **Configure variáveis de ambiente**

```bash
cp .env.example .env
# Edite .env com suas configurações
```

5. **Execute as migrações**

```bash
python manage.py migrate
```

6. **Crie um superusuário**

```bash
python manage.py createsuperuser
```

7. **Execute o servidor de desenvolvimento**

```bash
python manage.py runserver
```

O servidor estará disponível em `http://localhost:8000`

## Estrutura do Projeto

```
auraclass_dev/
├── apps/
│   ├── core/                 # Aplicação core (usuários, notificações)
│   ├── pedagogico/           # Módulo pedagógico (turmas, planejamento)
│   ├── administrativo/       # Módulo administrativo (matrículas, RH)
│   └── auramind/             # Integração IA (sugestões, análises)
├── config/                   # Configuração do projeto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── README.md
```

## Endpoints Principais

### Autenticação

- `POST /api/v1/token/` - Obter token JWT
- `POST /api/v1/token/refresh/` - Renovar token

### Usuários

- `GET /api/v1/core/users/` - Listar usuários
- `POST /api/v1/core/users/` - Criar usuário
- `GET /api/v1/core/users/me/` - Perfil do usuário atual

### Pedagógico

- `GET /api/v1/pedagogico/turmas/` - Listar turmas
- `GET /api/v1/pedagogico/planejamentos/` - Listar planejamentos
- `POST /api/v1/pedagogico/planejamentos/` - Criar planejamento
- `POST /api/v1/pedagogico/planejamentos/{id}/submit/` - Submeter para aprovação

### Administrativo

- `GET /api/v1/administrativo/matriculas/` - Listar matrículas
- `GET /api/v1/administrativo/funcionarios/` - Listar funcionários
- `GET /api/v1/administrativo/financeiro/` - Listar registros financeiros

### AuraMind

- `POST /api/v1/auramind/api/sugestoes_planejamento/` - Gerar sugestão pedagógica
- `POST /api/v1/auramind/api/analise_plano/` - Analisar plano

## Documentação da API

A documentação interativa da API está disponível em:

- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/schema/`

## Configuração de Produção

### Usando Gunicorn

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Usando Docker

```bash
docker build -t auraclass:latest .
docker run -p 8000:8000 auraclass:latest
```

### Variáveis de Ambiente para Produção

```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=seu-dominio.com
DATABASE_URL=postgresql://user:password@host:5432/auraclass
AURAMIND_API_KEY=your-production-key
```

## Testes

### Executar testes

```bash
pytest
```

### Com cobertura

```bash
pytest --cov=apps --cov-report=html
```

## Contribuindo

1. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
2. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
3. Push para a branch (`git push origin feature/AmazingFeature`)
4. Abra um Pull Request

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para detalhes.

## Suporte

Para suporte, abra uma issue no repositório ou entre em contato através de dev@auraclass.com

## Roadmap

- [ ] Frontend React/Vue
- [ ] Integração com Google Classroom
- [ ] Aplicativo Mobile
- [ ] Relatórios avançados
- [ ] Gamificação
- [ ] Integração com mais plataformas LMS

## Autores

- **AuraDev IA** - Desenvolvimento inicial

## Agradecimentos

- Django community
- Django REST Framework
- OpenAI
- n8n
