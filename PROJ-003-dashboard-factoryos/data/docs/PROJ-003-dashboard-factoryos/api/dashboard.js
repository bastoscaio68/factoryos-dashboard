const fs = require('fs');
const path = require('path');

module.exports = async (req, res) => {
    // CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
    
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }
    
    const BASE_PATH = path.join(__dirname, 'data', 'docs');
    const mode = req.query.mode || 'projetos';
    
    let html = `<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FactoryOS Dashboard</title>
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: #0a1628;
            color: #fff;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
        }
        .header {
            background: #1e1e1e;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo { font-size: 24px; font-weight: bold; color: #00d4ff; }
        .nav { display: flex; gap: 10px; }
        .nav a {
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            color: #fff;
            background: #333;
        }
        .nav a.active { background: #00d4ff; color: #000; }
        .section { background: #1e1e1e; border-radius: 10px; padding: 20px; margin-bottom: 20px; }
        h2 { color: #00d4ff; margin-bottom: 15px; border-bottom: 1px solid #333; padding-bottom: 10px; }
        .project-card {
            background: #252525;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #00d4ff;
        }
        .project-id { color: #00ffcc; font-size: 12px; font-weight: bold; }
        .project-name { font-size: 18px; font-weight: bold; margin: 5px 0; }
        .badges { display: flex; gap: 10px; margin-top: 10px; flex-wrap: wrap; }
        .badge { padding: 4px 12px; border-radius: 20px; font-size: 12px; }
        .badge-complete { background: #10b981; color: #fff; }
        .badge-aguardando { background: #f59e0b; color: #000; }
        .badge-andamento { background: #00d4ff; color: #000; }
        .files-list { list-style: none; }
        .files-list li {
            padding: 12px;
            border-bottom: 1px solid #333;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .folder { color: #ffd700; }
        .file { color: #fff; }
        .file-icon { margin-right: 10px; }
        .footer { text-align: center; padding: 20px; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">⚡ FactoryOS Dashboard</div>
        <div class="nav">
            <a href="/?mode=projetos" class="${mode === 'projetos' ? 'active' : ''}">📊 Projetos</a>
            <a href="/?mode=arquivos" class="${mode === 'arquivos' ? 'active' : ''}">📁 Arquivos</a>
        </div>
    </div>`;
    
    try {
        if (mode === 'projetos') {
            // Ler INDEX.md
            const indexPath = path.join(BASE_PATH, 'INDEX.md');
            const content = fs.readFileSync(indexPath, 'utf-8');
            const lines = content.split('\n');
            const tableLines = lines.slice(0, 20).filter(l => l.includes('PROJ-') && l.includes('|'));
            
            html += '<div class="section"><h2>📊 Projetos</h2>';
            
            tableLines.forEach(line => {
                const cols = line.split('|').slice(1, -1).map(c => c.trim());
                if (cols.length >= 3) {
                    const id = cols[0];
                    const titulo = cols[1];
                    const statusRaw = cols[2].replace(/[✅🔴🟡🔵🔶]/g, '').replace(/\s+/g, ' ').trim();
                    const gate = cols[3] || '';
                    
                    let statusClass = 'badge-aguardando';
                    let statusText = statusRaw;
                    const statusLower = statusRaw.toLowerCase();
                    if (statusLower.includes('conclu') || statusLower.includes('completo')) {
                        statusClass = 'badge-complete';
                        statusText = 'CONCLUÍDO';
                    } elseif (statusLower.includes('andamento')) {
                        statusClass = 'badge-andamento';
                        statusText = 'EM ANDAMENTO';
                    }
                    
                    html += `<div class="project-card">
                        <div class="project-id">${id}</div>
                        <div class="project-name">${titulo}</div>
                        <div class="badges">
                            <span class="badge ${statusClass}">${statusText}</span>
                            <span class="badge" style="background:#333;">${gate}</span>
                        </div>
                    </div>`;
                }
            });
            
            html += '</div>';
        } else {
            // Listar arquivos
            const targetPath = req.query.path ? path.join(BASE_PATH, req.query.path) : BASE_PATH;
            
            html += '<div class="section"><h2>📁 Arquivos</h2>';
            
            if (fs.existsSync(targetPath)) {
                const entries = fs.readdirSync(targetPath, { withFileTypes: true });
                html += '<ul class="files-list">';
                
                for (const entry of entries) {
                    if (entry.name.startsWith('.')) continue;
                    
                    const fullPath = path.join(targetPath, entry.name);
                    const relPath = req.query.path ? req.query.path + '/' + entry.name : entry.name;
                    
                    if (entry.isDirectory()) {
                        html += `<li>
                            <span class="folder">📁 <a href="/?mode=arquivos&path=${relPath}" style="color:#ffd700;text-decoration:none;">${entry.name}</a></span>
                            <span style="color:#666;">pasta</span>
                        </li>`;
                    } else if (entry.isFile()) {
                        let icon = '📄';
                        const ext = path.extname(entry.name).toLowerCase();
                        if (ext === '.html') icon = '⚙️';
                        else if (ext === '.md') icon = '📝';
                        else if (['.png', '.jpg', '.jpeg'].includes(ext)) icon = '🖼️';
                        else if (ext === '.pdf') icon = '📕';
                        else if (ext === '.zip') icon = '📦';
                        
                        const stats = fs.statSync(fullPath);
                        const size = stats.size < 1024 ? `${stats.size}B` : `${(stats.size/1024).toFixed(1)}KB`;
                        
                        html += `<li>
                            <span class="file"><span class="file-icon">${icon}</span>${entry.name}</span>
                            <span style="color:#666;">${size}</span>
                        </li>`;
                    }
                }
                html += '</ul>';
            } else {
                html += '<p>Diretório não encontrado</p>';
            }
            html += '</div>';
        }
    } catch (e) {
        html += '<div class="section"><p>Erro: ' + e.message + '</p></div>';
    }
    
    html += `<div class="footer">
        <small>Atualizado: ${new Date().toLocaleString('pt-BR')}</small>
    </div></body></html>`;
    
    res.setHeader('Content-Type', 'text/html');
    res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
    res.status(200).send(html);
};
