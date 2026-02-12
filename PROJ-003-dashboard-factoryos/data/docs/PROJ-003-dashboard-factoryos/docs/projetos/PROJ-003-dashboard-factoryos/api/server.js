/**
 * FactoryOS Dashboard API
 * API Backend para CRUD de projetos + WebSocket futuro
 */

const http = require('http');
const fs = require('fs').promises;
const path = require('path');
const { parse: parseYaml } = require('yaml');
const { marked } = require('marked');

// Configuração
const CONFIG = {
    PORT: process.env.PORT || 3000,
    BASE_PATH: path.join(__dirname, '..', '..', '..', '..'),
    CORS_ORIGINS: process.env.CORS_ORIGINS?.split(',') || ['*']
};

// Logging
const log = (level, message, data = {}) => {
    const timestamp = new Date().toISOString();
    console[level](`[${timestamp}] [${level.toUpperCase()}] ${message}`, data);
};

// CORS Headers
const setCors = (res) => {
    const origin = CONFIG.CORS_ORIGINS[0] || '*';
    res.setHeader('Access-Control-Allow-Origin', origin);
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
};

// Parse Frontmatter YAML
const parseFrontmatter = (content) => {
    const regex = /^---\n([\s\S]*?)\n---\n([\s\S]*)$/;
    const match = content.match(regex);
    
    if (match) {
        try {
            const frontmatter = parseYaml(match[1]);
            const markdown = match[2].trim();
            return { frontmatter, markdown, raw: content };
        } catch (e) {
            log('error', 'Failed to parse frontmatter', { error: e.message });
            return { frontmatter: {}, markdown: content, raw: content };
        }
    }
    return { frontmatter: {}, markdown: content, raw: content };
};

// Render Markdown to HTML
const renderMarkdown = (markdown) => {
    return marked.parse(markdown);
};

// Ler INDEX.md
const getProjetos = async () => {
    const indexPath = path.join(CONFIG.BASE_PATH, 'docs', 'projetos', 'INDEX.md');
    try {
        const content = await fs.readFile(indexPath, 'utf-8');
        const { frontmatter, markdown } = parseFrontmatter(content);
        
        // Parse lista de projetos do markdown
        const lines = markdown.split('\n');
        const projetos = [];
        
        // Tabela markdown: | ID | Nome | Status | ...
        // Procura linhas com PROJ-
        const tableLines = lines.filter(l => l.includes('PROJ-') && l.includes('|'));
        
        if (tableLines.length > 0) {
            tableLines.forEach((line, idx) => {
                // Remove pipes e faz split
                const cols = line.split('|').slice(1, -1).map(c => c.trim());
                if (cols.length >= 3) {
                    const id = cols[0].trim();
                    const nome = cols[1].trim();
                    const statusRaw = cols[2].trim();
                    const gate = cols[3]?.trim() || '';
                    const descricao = cols[4]?.trim() || '';
                    
                    // Extrai status (remove emojis e espaços)
                    const status = statusRaw.replace(/[✅🔴🟡🔵🔶]/g, '').replace(/\s+/g, ' ').trim();
                    
                    projetos.push({
                        id: id,
                        titulo: nome,
                        status: status,
                        gate: gate,
                        descricao: descricao,
                        linha: idx + 1
                    });
                }
            });
        }
        
        return { success: true, data: { frontmatter, projetos } };
    } catch (e) {
        log('error', 'Failed to read INDEX.md', { error: e.message });
        return { success: false, error: 'Projetos not found', details: e.message };
    }
};

// Ler STATUS.md/:id
const getProjetoStatus = async (id) => {
    const statusPath = path.join(CONFIG.BASE_PATH, 'docs', 'projetos', id, 'STATUS.md');
    try {
        const content = await fs.readFile(statusPath, 'utf-8');
        const { frontmatter, markdown, raw } = parseFrontmatter(content);
        const html = renderMarkdown(markdown);
        
        return {
            success: true,
            data: {
                id,
                frontmatter,
                markdown,
                html,
                raw
            }
        };
    } catch (e) {
        log('error', 'Failed to read STATUS.md', { id, error: e.message });
        return { success: false, error: 'Projeto not found', details: e.message };
    }
};

// Criar estrutura de pastas para novo projeto
const createProjeto = async (data) => {
    const { id, titulo, descricao } = data;
    
    if (!id || !titulo) {
        return { success: false, error: 'ID and titulo are required' };
    }
    
    const projetoPath = path.join(CONFIG.BASE_PATH, 'docs', 'projetos', id);
    
    try {
        // Criar diretório
        await fs.mkdir(projetoPath, { recursive: true });
        
        // Criar STATUS.md
        const statusContent = `---
titulo: "${titulo}"
status: "planejado"
data_criacao: "${new Date().toISOString().split('T')[0]}"
responsavel: "TBD"
prioridade: "media"
tags: []
---

# ${titulo}

${descricao || 'Sem descrição.'}

## PDCA Log

### Plan
- 

### Do
- 

### Check
- 

### Act
- 
`;
        await fs.writeFile(path.join(projetoPath, 'STATUS.md'), statusContent);
        
        // Criar PDCA_LOG.md
        const pdcaContent = `# PDCA Log - ${titulo}

## Histórico de Alterações

| Data | Ação | Responsável | Notas |
|------|------|-------------|-------|
| ${new Date().toISOString().split('T')[0]} | Criação | Sistema | Projeto inicial criado |
`;
        await fs.writeFile(path.join(projetoPath, 'PDCA_LOG.md'), pdcaContent);
        
        // Criar DOCS.md
        const docsContent = `# Documentação - ${titulo}

## Visão Geral

${descricao || 'Sem descrição.'}

## Objetivos

-

## Entregáveis

-

## Referências

-
`;
        await fs.writeFile(path.join(projetoPath, 'DOCS.md'), docsContent);
        
        log('info', 'Projeto criado', { id, titulo });
        return { success: true, data: { id, titulo, path: projetoPath } };
    } catch (e) {
        log('error', 'Failed to create projeto', { id, error: e.message });
        return { success: false, error: 'Failed to create projeto', details: e.message };
    }
};

// Atualizar STATUS.md
const updateStatus = async (id, data) => {
    const statusPath = path.join(CONFIG.BASE_PATH, 'docs', 'projetos', id, 'STATUS.md');
    
    try {
        const content = await fs.readFile(statusPath, 'utf-8');
        let { frontmatter, markdown } = parseFrontmatter(content);
        
        // Atualizar frontmatter
        frontmatter = { ...frontmatter, ...data };
        frontmatter.data_atualizacao = new Date().toISOString().split('T')[0];
        frontmatter.status = data.status || frontmatter.status;
        
        // Reconstruir arquivo
        const yaml = require('yaml');
        const newContent = `---\n${yaml.stringify(frontmatter)}---\n${markdown}`;
        await fs.writeFile(statusPath, newContent);
        
        log('info', 'Status atualizado', { id, data });
        return { success: true, data: { id, frontmatter } };
    } catch (e) {
        log('error', 'Failed to update status', { id, error: e.message });
        return { success: false, error: 'Failed to update status', details: e.message };
    }
};

// Append ao PDCA_LOG.md
const addLog = async (id, logData) => {
    const pdcaPath = path.join(CONFIG.BASE_PATH, 'docs', 'projetos', id, 'PDCA_LOG.md');
    const { acao, responsavel, notas } = logData;
    
    if (!acao) {
        return { success: false, error: 'Ação é obrigatória' };
    }
    
    try {
        const data = new Date().toISOString().split('T')[0];
        const novaLinha = `| ${data} | ${acao} | ${responsavel || 'TBD'} | ${notas || '-'} |\n`;
        
        // Ler arquivo
        let content = await fs.readFile(pdcaPath, 'utf-8');
        
        // Append antes da tabela de histórico (se existir) ou no final
        if (content.includes('| Data | Ação')) {
            // Insert after header row
            const lines = content.split('\n');
            const headerEndIndex = lines.findIndex(line => line.startsWith('| ---'));
            if (headerEndIndex !== -1) {
                lines.splice(headerEndIndex + 1, 0, novaLinha);
                content = lines.join('\n');
            } else {
                content += novaLinha;
            }
        } else {
            content += novaLinha;
        }
        
        await fs.writeFile(pdcaPath, content);
        
        log('info', 'Log adicionado', { id, acao });
        return { success: true, data: { id, acao, data } };
    } catch (e) {
        log('error', 'Failed to add log', { id, error: e.message });
        return { success: false, error: 'Failed to add log', details: e.message };
    }
};

// Parse body JSON
const parseBody = (req) => {
    return new Promise((resolve, reject) => {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
            try {
                resolve(body ? JSON.parse(body) : {});
            } catch (e) {
                reject(new Error('Invalid JSON'));
            }
        });
        req.on('error', reject);
    });
};

// ========== FILE BROWSER ==========

// Pastas bloqueadas
const BLOCKED = ['.git', 'node_modules', '.openclaw'];

function normalizeFilePath(requestPath) {
    if (!requestPath) return null;
    const clean = requestPath.split('?')[0].split('#')[0];
    const decoded = decodeURIComponent(clean);
    if (decoded.startsWith('/')) return null;
    const normalized = path.normalize(decoded);
    if (normalized.includes('..')) return null;
    const absolute = path.resolve(CONFIG.BASE_PATH, normalized);
    if (!absolute.startsWith(CONFIG.BASE_PATH)) return null;
    return absolute;
}

function isBlocked(absPath) {
    const rel = path.relative(CONFIG.BASE_PATH, absPath);
    return BLOCKED.some(b => rel === b || rel.startsWith(b + '/'));
}

function formatSize(bytes) {
    if (bytes === 0) return '0B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + sizes[i];
}

function getFileIcon(filename) {
    const ext = path.extname(filename).toLowerCase();
    const icons = {
        '.md': '📝', '.js': '📜', '.html': '⚙️', '.css': '🎨',
        '.json': '📋', '.sh': '🔧', '.png': '🖼️', '.jpg': '🖼️',
        '.pdf': '📕', '.zip': '📦'
    };
    return icons[ext] || '📄';
}

async function listFiles(absPath) {
    const entries = await fs.readdir(absPath, { withFileTypes: true });
    const folders = [];
    const files = [];
    
    for (const entry of entries) {
        if (entry.name.startsWith('.')) continue;
        const full = path.join(absPath, entry.name);
        const rel = path.relative(CONFIG.BASE_PATH, full);
        
        if (entry.isDirectory()) {
            folders.push({ name: entry.name, path: rel });
        } else if (entry.isFile()) {
            const stats = await fs.stat(full);
            files.push({
                name: entry.name,
                path: rel,
                size: formatSize(stats.size),
                icon: getFileIcon(entry.name)
            });
        }
    }
    
    folders.sort((a, b) => a.name.localeCompare(b.name));
    files.sort((a, b) => a.name.localeCompare(b.name));
    
    return { path: path.relative(CONFIG.BASE_PATH, absPath), folders, files };
}

async function handleFiles(req, res, pathname, method, url) {
    setCors(res);
    
    try {
        // Download: GET /api/arquivos/path/to/file
        const downloadMatch = pathname.match(/^\/api\/arquivos\/(.+)$/);
        if (downloadMatch) {
            const absPath = normalizeFilePath(downloadMatch[1]);
            if (!absPath || isBlocked(absPath)) {
                res.writeHead(403, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: 'Acesso negado' }));
                return;
            }
            if (!await fs.stat(absPath).then(s => s.isFile())) {
                res.writeHead(404, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: 'Arquivo não encontrado' }));
                return;
            }
            res.setHeader('Content-Type', 'application/octet-stream');
            res.setHeader('Content-Disposition', `attachment; filename="${path.basename(absPath)}"`);
            const stream = fs.createReadStream(absPath);
            stream.pipe(res);
            return;
        }
        
        // List: GET /api/arquivos?path=...
        const queryPath = url.searchParams.get('path') || '';
        const absPath = normalizeFilePath(queryPath);
        
        if (!absPath || isBlocked(absPath)) {
            res.writeHead(403, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Path inválido ou bloqueado' }));
            return;
        }
        
        try {
            const stat = await fs.stat(absPath);
        } catch (e) {
            res.writeHead(404, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Diretório não encontrado' }));
            return;
        }
        
        const result = await listFiles(absPath);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(result));
        
    } catch (e) {
        console.error('Files API Error:', e);
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Erro interno' }));
    }
}

// Router
const router = async (req, res) => {
    setCors(res);
    
    const url = new URL(req.url, `http://${req.headers.host}`);
    const pathname = url.pathname;
    const method = req.method;
    
    log('info', `${method} ${pathname}`);
    
    // Health check
    if (pathname === '/health') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'ok', timestamp: new Date().toISOString() }));
        return;
    }
    
    // OPTIONS /api/arquivos (CORS preflight)
    if (method === 'OPTIONS' && pathname.startsWith('/api/arquivos')) {
        res.writeHead(200);
        res.end();
        return;
    }
    
    // GET /api/arquivos (list or download)
    if (method === 'GET' && pathname.startsWith('/api/arquivos')) {
        await handleFiles(req, res, pathname, method, url);
        return;
    }
    
    // GET /api/projetos
    if (method === 'GET' && pathname === '/api/projetos') {
        const result = await getProjetos();
        res.writeHead(result.success ? 200 : 404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(result));
        return;
    }
    
    // GET /api/projetos/:id
    const projetoMatch = pathname.match(/^\/api\/projetos\/([^/]+)$/);
    if (method === 'GET' && projetoMatch) {
        const result = await getProjetoStatus(projetoMatch[1]);
        res.writeHead(result.success ? 200 : 404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(result));
        return;
    }
    
    // POST /api/projetos
    if (method === 'POST' && pathname === '/api/projetos') {
        try {
            const body = await parseBody(req);
            const result = await createProjeto(body);
            res.writeHead(result.success ? 201 : 400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify(result));
        } catch (e) {
            res.writeHead(400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ success: false, error: e.message }));
        }
        return;
    }
    
    // PUT /api/projetos/:id/status
    const statusMatch = pathname.match(/^\/api\/projetos\/([^/]+)\/status$/);
    if (method === 'PUT' && statusMatch) {
        try {
            const body = await parseBody(req);
            const result = await updateStatus(statusMatch[1], body);
            res.writeHead(result.success ? 200 : 400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify(result));
        } catch (e) {
            res.writeHead(400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ success: false, error: e.message }));
        }
        return;
    }
    
    // POST /api/projetos/:id/log
    const logMatch = pathname.match(/^\/api\/projetos\/([^/]+)\/log$/);
    if (method === 'POST' && logMatch) {
        try {
            const body = await parseBody(req);
            const result = await addLog(logMatch[1], body);
            res.writeHead(result.success ? 201 : 400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify(result));
        } catch (e) {
            res.writeHead(400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ success: false, error: e.message }));
        }
        return;
    }
    
    // 404
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ success: false, error: 'Not found' }));
};

// Server
const server = http.createServer(router);

// WebSocket setup (placeholder para futuro)
let wss = null;
const setupWebSocket = (wsServer) => {
    wss = wsServer;
    wss.on('connection', (ws) => {
        log('info', 'WebSocket client connected');
        ws.on('message', (message) => {
            log('info', 'WebSocket message received', { message: message.toString() });
        });
        ws.send(JSON.stringify({ type: 'connected', message: 'FactoryOS Dashboard API WebSocket' }));
    });
};

// Start server
server.listen(CONFIG.PORT, () => {
    log('info', `FactoryOS Dashboard API started on port ${CONFIG.PORT}`);
    log('info', `Base path: ${CONFIG.BASE_PATH}`);
    console.log(`
╔════════════════════════════════════════════════════════════╗
║  FactoryOS Dashboard API                                   ║
╠════════════════════════════════════════════════════════════╣
║  Endpoints:                                                ║
║  GET  /api/projetos           → Lista projetos             ║
║  GET  /api/projetos/:id       → Detalhes do projeto        ║
║  POST /api/projetos           → Criar novo projeto         ║
║  PUT  /api/projetos/:id/status → Atualizar status          ║
║  POST /api/projetos/:id/log   → Adicionar log PDCA         ║
║  GET  /health                 → Health check                ║
╠════════════════════════════════════════════════════════════╣
║  Running on http://localhost:${CONFIG.PORT}                      ║
╚════════════════════════════════════════════════════════════╝
    `);
});

// Graceful shutdown
process.on('SIGTERM', () => {
    log('info', 'SIGTERM received, shutting down');
    server.close(() => {
        log('info', 'Server closed');
        process.exit(0);
    });
});

module.exports = { server, setupWebSocket };
