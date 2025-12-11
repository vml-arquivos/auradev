# Guia de Deployment - AuraClass

Este documento descreve como fazer o deployment do AuraClass em diferentes ambientes.

## Deployment Local

### Pré-requisitos

- Python 3.8+
- PostgreSQL 12+ (opcional)
- Git

### Passos

1. Clone o repositório
2. Crie um virtual environment
3. Instale as dependências
4. Configure variáveis de ambiente
5. Execute as migrações
6. Inicie o servidor

```bash
git clone https://github.com/vml-arquivos/auradev.git
cd auradev
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

## Deployment com Docker

### Pré-requisitos

- Docker
- Docker Compose

### Passos

```bash
# Build das imagens
docker-compose build

# Iniciar os serviços
docker-compose up -d

# Executar migrações
docker-compose exec web python manage.py migrate

# Criar superusuário
docker-compose exec web python manage.py createsuperuser

# Coletar arquivos estáticos
docker-compose exec web python manage.py collectstatic --noinput
```

O aplicativo estará disponível em `http://localhost:8000`

## Deployment em Produção

### Usando Gunicorn + Nginx

#### 1. Configurar Gunicorn

Crie um arquivo `gunicorn_config.py`:

```python
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 30
keepalive = 2
```

#### 2. Configurar Nginx

Crie um arquivo `/etc/nginx/sites-available/auraclass`:

```nginx
upstream auraclass {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name seu-dominio.com;
    client_max_body_size 10M;

    location / {
        proxy_pass http://auraclass;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/auraclass/staticfiles/;
    }

    location /media/ {
        alias /home/auraclass/media/;
    }
}
```

#### 3. Configurar Systemd Service

Crie um arquivo `/etc/systemd/system/auraclass.service`:

```ini
[Unit]
Description=AuraClass Django Application
After=network.target

[Service]
Type=notify
User=auraclass
WorkingDirectory=/home/auraclass/auradev
ExecStart=/home/auraclass/venv/bin/gunicorn \
    --config gunicorn_config.py \
    --chdir /home/auraclass/auradev \
    config.wsgi:application
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 4. Iniciar o Serviço

```bash
sudo systemctl daemon-reload
sudo systemctl start auraclass
sudo systemctl enable auraclass
```

### Variáveis de Ambiente para Produção

```env
DEBUG=False
SECRET_KEY=sua-chave-secreta-muito-segura
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
DATABASE_URL=postgresql://user:password@localhost:5432/auraclass
AURAMIND_API_KEY=sua-chave-api-auramind
N8N_API_KEY=sua-chave-api-n8n
EMAIL_HOST_PASSWORD=sua-senha-email
SENTRY_ENABLED=True
SENTRY_DSN=seu-dsn-sentry
```

### SSL/TLS com Let's Encrypt

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d seu-dominio.com
```

Atualize a configuração do Nginx para usar SSL:

```nginx
server {
    listen 443 ssl http2;
    server_name seu-dominio.com;
    
    ssl_certificate /etc/letsencrypt/live/seu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seu-dominio.com/privkey.pem;
    
    # ... resto da configuração
}

server {
    listen 80;
    server_name seu-dominio.com;
    return 301 https://$server_name$request_uri;
}
```

## Deployment em Cloud Providers

### Heroku

1. Instale o Heroku CLI
2. Faça login: `heroku login`
3. Crie uma app: `heroku create seu-app-name`
4. Configure as variáveis de ambiente
5. Faça push: `git push heroku main`

### AWS EC2

1. Inicie uma instância EC2 (Ubuntu 20.04)
2. Instale as dependências
3. Clone o repositório
4. Configure o banco de dados RDS
5. Configure o Nginx e Gunicorn
6. Configure o SSL com ACM

### DigitalOcean App Platform

1. Conecte seu repositório GitHub
2. Configure as variáveis de ambiente
3. Configure o banco de dados PostgreSQL
4. Deploy automático

## Monitoramento

### Logs

```bash
# Ver logs do Gunicorn
sudo journalctl -u auraclass -f

# Ver logs do Nginx
sudo tail -f /var/log/nginx/error.log
```

### Métricas

Configure Sentry para monitoramento de erros:

```python
import sentry_sdk
sentry_sdk.init(dsn="seu-dsn-sentry")
```

### Backups

Configure backups automáticos do banco de dados:

```bash
# Backup manual
pg_dump -U user auraclass > backup.sql

# Restaurar
psql -U user auraclass < backup.sql
```

## Checklist de Deployment

- [ ] Variáveis de ambiente configuradas
- [ ] Banco de dados criado e migrado
- [ ] Arquivos estáticos coletados
- [ ] SSL/TLS configurado
- [ ] Email configurado
- [ ] Backups configurados
- [ ] Monitoramento ativado
- [ ] Logs configurados
- [ ] Firewall configurado
- [ ] CDN configurado (opcional)

## Troubleshooting

### Erro 502 Bad Gateway

Verifique se o Gunicorn está rodando:

```bash
sudo systemctl status auraclass
sudo journalctl -u auraclass -n 50
```

### Erro de Permissão

Verifique as permissões dos arquivos:

```bash
sudo chown -R auraclass:auraclass /home/auraclass/auradev
sudo chmod -R 755 /home/auraclass/auradev
```

### Erro de Banco de Dados

Verifique a conexão:

```bash
psql -U user -h localhost -d auraclass
```

## Suporte

Para dúvidas sobre deployment, abra uma issue ou entre em contato através de dev@auraclass.com
