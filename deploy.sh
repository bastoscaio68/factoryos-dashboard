#!/bin/bash

################################################################################
# FactoryOS Dashboard - Deploy Script
# Deploy no Vercel com suporte a Serverless Functions
################################################################################

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configurações
PROJECT_NAME="factoryos-dashboard"
API_DIR="docs/projetos/PROJ-003-dashboard-factoryos/outputs/api"
OUTPUT_DIR="vercel-deploy"

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  FactoryOS Dashboard - Deploy Script (Vercel)${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""

# Função de log
log() {
    echo -e "${GREEN}[✓]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[!]${NC} $1"
}

error() {
    echo -e "${RED}[✗]${NC} $1"
    exit 1
}

# Verificar dependências
check_dependencies() {
    echo -e "${BLUE}▸ Verificando dependências...${NC}"
    
    if ! command -v node &> /dev/null; then
        error "Node.js não está instalado"
    fi
    log "Node.js: $(node --version)"
    
    if ! command -v vercel &> /dev/null; then
        warn "Vercel CLI não encontrado. Instalando..."
        npm install -g vercel
    fi
    log "Vercel CLI: $(vercel --version)"
}

# Preparar build
prepare_build() {
    echo ""
    echo -e "${BLUE}▸ Preparando build...${NC}"
    
    # Criar diretório de output
    mkdir -p "$OUTPUT_DIR"
    
    # Copiar API
    cp -r "$API_DIR"/* "$OUTPUT_DIR/"
    
    # Criar package.json se não existir
    if [ ! -f "$OUTPUT_DIR/package.json" ]; then
        cat > "$OUTPUT_DIR/package.json" << 'EOF'
{
  "name": "factoryos-dashboard-api",
  "version": "1.0.0",
  "description": "FactoryOS Dashboard API",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "node server.js"
  },
  "dependencies": {
    "marked": "^9.1.0",
    "yaml": "^2.3.0"
  }
}
EOF
        log "package.json criado"
    fi
    
    # Criar vercel.json para configuração de serverless
    cat > "$OUTPUT_DIR/vercel.json" << 'EOF'
{
  "version": 2,
  "framework": null,
  "builds": [
    {
      "src": "server.js",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/server.js"
    },
    {
      "src": "/(.*)",
      "dest": "/server.js"
    }
  ],
  "env": {
    "NODE_ENV": "production"
  },
  "regions": ["iad1"]
}
EOF
    log "vercel.json criado"
    
    log "Build preparado com sucesso"
}

# Instalar dependências
install_deps() {
    echo ""
    echo -e "${BLUE}▸ Instalando dependências...${NC}"
    cd "$OUTPUT_DIR"
    npm install --production
    cd - > /dev/null
    log "Dependências instaladas"
}

# Deploy
deploy() {
    echo ""
    echo -e "${BLUE}▸ Fazendo deploy no Vercel...${NC}"
    echo ""
    
    cd "$OUTPUT_DIR"
    
    if [ "$1" == "--prod" ] || [ "$1" == "-p" ]; then
        vercel --prod --yes
    else
        vercel --yes
    fi
    
    cd - > /dev/null
}

# Configurar custom domain (opcional)
setup_custom_domain() {
    if [ -n "$1" ]; then
        echo ""
        echo -e "${BLUE}▸ Configurando custom domain: $1${NC}"
        vercel domains add "$1" --yes || warn "Não foi possível adicionar o domínio"
        
        echo ""
        echo -e "${YELLOW}▸ Configure o DNS do domínio:$NC"
        echo "   CNAME ou ALIAS para cname.vercel-dns.com"
    fi
}

# Mostrar informações pós-deploy
post_deploy_info() {
    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  Deploy concluído com sucesso!${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${BLUE}Endpoints disponíveis:${NC}"
    echo "  • GET    /api/projetos       - Lista projetos"
    echo "  • GET    /api/projetos/:id   - Detalhes do projeto"
    echo "  • POST   /api/projetos       - Criar projeto"
    echo "  • PUT    /api/projetos/:id/status - Atualizar status"
    echo "  • POST   /api/projetos/:id/log - Adicionar log PDCA"
    echo "  • GET    /health             - Health check"
    echo ""
    echo -e "${YELLOW}Próximos passos:${NC}"
    echo "  1. Configure custom domain (se desejado)"
    echo "  2. Configure variáveis de ambiente no Vercel"
    echo "  3. Habilite WebSocket se necessário"
    echo ""
}

# Mostrar help
show_help() {
    cat << EOF
用法: ./deploy.sh [opções]

Opções:
  -h, --help           Mostrar esta ajuda
  -p, --prod           Deploy em produção
  --domain <domínio>   Configurar custom domain após deploy
  --skip-build         Pular preparação do build
  --only-build         Apenas preparar build (sem deploy)

Exemplos:
  ./deploy.sh                    # Deploy de preview
  ./deploy.sh --prod             # Deploy em produção
  ./deploy.sh --prod --domain api.factoryos.com.br
                              # Deploy + custom domain
EOF
}

# Main
main() {
    SKIP_BUILD=false
    ONLY_BUILD=false
    PRODUCTION=false
    CUSTOM_DOMAIN=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -p|--prod)
                PRODUCTION=true
                shift
                ;;
            --domain)
                CUSTOM_DOMAIN="$2"
                shift 2
                ;;
            --skip-build)
                SKIP_BUILD=true
                shift
                ;;
            --only-build)
                ONLY_BUILD=true
                shift
                ;;
            *)
                error "Opção desconhecida: $1"
                ;;
        esac
    done
    
    if [ "$ONLY_BUILD" == "true" ]; then
        check_dependencies
        prepare_build
        install_deps
        log "Build concluído. Execute ./deploy.sh para deploy."
        exit 0
    fi
    
    if [ "$SKIP_BUILD" == "false" ]; then
        check_dependencies
        prepare_build
        install_deps
    fi
    
    if [ "$PRODUCTION" == "true" ]; then
        deploy "--prod"
    else
        deploy
    fi
    
    if [ -n "$CUSTOM_DOMAIN" ]; then
        setup_custom_domain "$CUSTOM_DOMAIN"
    fi
    
    post_deploy_info
}

# Executar
main "$@"
