# FactoryOS Dashboard - API Gateway Configuration

## Visão Geral

Este documento descreve como configurar o gateway OpenClaw para expor a API do FactoryOS Dashboard.

## Configuração do Gateway OpenClaw

### 1. Verificar Status do Gateway

```bash
openclaw gateway status
```

### 2. Configurar rotas para a API

Crie um arquivo de configuração em `~/.openclaw/gateway/routes.json`:

```json
{
  "routes": [
    {
      "path": "/api",
      "target": "http://localhost:3000",
      "methods": ["GET", "POST", "PUT", "DELETE"],
      "stripPrefix": false,
      "headers": {
        "Access-Control-Allow-Origin": "*",
        "X-Forwarded-For": "factoryos-api"
      }
    },
    {
      "path": "/dashboard",
      "target": "http://localhost:3000",
      "methods": ["GET"]
    }
  ],
  "port": 8080,
  "host": "0.0.0.0",
  "ssl": {
    "enabled": false,
    "cert": "",
    "key": ""
  },
  "logging": {
    "level": "info",
    "format": "json"
  },
  "cors": {
    "enabled": true,
    "origins": ["*"],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "headers": ["Content-Type", "Authorization", "X-Requested-With"]
  }
}
```

### 3. Iniciar o Gateway com a API

```bash
# Iniciar a API primeiro
node docs/projetos/PROJ-003-dashboard-factoryos/outputs/api/server.js &

# Ou usar o gateway diretamente
openclaw gateway start --config ~/.openclaw/gateway/routes.json
```

### 4. Configurar como Serviço systemd (Linux)

Crie `/etc/systemd/system/factoryos-api.service`:

```ini
[Unit]
Description=FactoryOS Dashboard API
After=network.target

[Service]
Type=simple
User=team
WorkingDirectory=/home/team/.openclaw/workspace-scope_parser
ExecStart=/usr/bin/node docs/projetos/PROJ-003-dashboard-factoryos/outputs/api/server.js
Restart=always
RestartSec=10
Environment=NODE_ENV=production
Environment=PORT=3000

[Install]
WantedBy=multi-user.target
```

Ativar e iniciar:

```bash
sudo systemctl daemon-reload
sudo systemctl enable factoryos-api
sudo systemctl start factoryos-api
sudo systemctl status factoryos-api
```

### 5. Configurar Nginx como Proxy Reverso (Produção)

Crie `/etc/nginx/sites-available/factoryos`:

```nginx
server {
    listen 80;
    server_name api.factoryos.com.br;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # CORS headers
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Content-Type, Authorization' always;
    }
    
    # WebSocket support
    location /ws {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
}
```

Ativar:

```bash
sudo ln -s /etc/nginx/sites-available/factoryos /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 6. Configurar SSL com Let's Encrypt

```bash
sudo certbot --nginx -d api.factoryos.com.br
```

### 7. Variáveis de Ambiente Recomendadas

```bash
# .env
NODE_ENV=production
PORT=3000
BASE_PATH=/home/team/.openclaw/workspace-scope_parser
CORS_ORIGINS=https://factoryos.com.br,https://dashboard.factoryos.com.br
LOG_LEVEL=info
```

## Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/projetos` | Lista todos os projetos |
| GET | `/api/projetos/:id` | Detalhes de um projeto |
| POST | `/api/projetos` | Criar novo projeto |
| PUT | `/api/projetos/:id/status` | Atualizar status |
| POST | `/api/projetos/:id/log` | Adicionar log PDCA |
| GET | `/health` | Health check |

## Testes

### Testar endpoints locais

```bash
# Health check
curl http://localhost:3000/health

# Listar projetos
curl http://localhost:3000/api/projetos

# Criar projeto
curl -X POST http://localhost:3000/api/projetos \
  -H "Content-Type: application/json" \
  -d '{"id":"PROJ-004","titulo":"Novo Projeto","descricao":"Descrição"}'
```

### Testar via gateway

```bash
curl http://localhost:8080/api/projetos
```

## Monitoramento

### Logs

```bash
# Ver logs da API
journalctl -u factoryos-api -f

# Ou verificar output do processo
pm2 logs factoryos-api
```

### Health Check Automático

Crie um cron job para verificar a saúde da API:

```bash
# /etc/cron.d/factoryos-healthcheck
*/5 * * * * curl -s http://localhost:3000/health || systemctl restart factoryos-api
```

## Troubleshooting

### Gateway não inicia

```bash
# Verificar portas em uso
netstat -tlnp | grep -E '(:3000|:8080)'

# Verificar logs do gateway
openclaw gateway logs
```

### CORS errors

Verifique se os headers CORS estão configurados corretamente no gateway ou no servidor.

### API não responde

```bash
# Verificar se a API está rodando
curl http://localhost:3000/health

# Verificar portas
lsof -i :3000
```

## Links Úteis

- [Documentação OpenClaw Gateway](../docs/openclaw-gateway.md)
- [Vercel Serverless Functions](https://vercel.com/docs/serverless-functions)
- [Node.js HTTP Server](https://nodejs.org/api/http.html)
