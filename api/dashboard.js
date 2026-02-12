const fs = require('fs');
const path = require('path');

module.exports = async (req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
    
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }
    
    const BASE_PATH = path.join(__dirname, 'data', 'docs');
    const mode = req.query.mode || 'projetos';
    const filter = req.query.filter || 'todos';
    const projeto = req.query.projeto || '';
    
    const descricoes = {
        'proj-003-dashboard-factoryos': 'Dashboard web para visualizacao e gerenciamento de projetos do FactoryOS. Inclui API, filtros, detalhes, metodologia e download de arquivos.',
        'proj-003-ext': 'Extensao do Dashboard para visualizacao e download de arquivos dos projetos. Interface integrada com API de arquivos.',
        'proj-002-visual-improvement': 'Melhoria da qualidade visual de todos os outputs do sistema. Padronizacao de cores, design e identidade visual.',
        'proj-001-procedure-check': 'Verificacao de procedimentos e documento inicial do FactoryOS. Primeira implementacao do sistema multi-agentes.'
    };
    
    let html = '<!DOCTYPE html>\n<html lang="pt-BR">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>FactoryOS Dashboard</title>\n<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">\n<style>\n* { margin: 0; padding: 0; box-sizing: border-box; }\nbody { font-family: "Segoe UI", system-ui, sans-serif; background: #0a1628; color: #fff; padding: 20px; max-width: 900px; margin: 0 auto; }\n.header { background: #1e1e1e; padding: 20px; border-radius: 16px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; }\n.logo { font-size: 24px; font-weight: bold; color: #00d4ff; display: flex; align-items: center; gap: 10px; }\n.nav { display: flex; gap: 10px; flex-wrap: wrap; }\n.nav a { padding: 10px 20px; border-radius: 10px; text-decoration: none; color: #fff; background: #333; transition: 0.3s; }\n.nav a.active { background: linear-gradient(135deg, #00d4ff, #8b5cf6); color: #000; font-weight: bold; }\n.nav a:hover { transform: translateY(-2px); }\n.section { background: #1e1e1e; border-radius: 16px; padding: 20px; margin-bottom: 20px; }\nh2 { color: #00d4ff; margin-bottom: 15px; border-bottom: 1px solid #333; padding-bottom: 10px; }\n.filters { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }\n.filter-btn { padding: 8px 16px; border: none; border-radius: 20px; background: #333; color: #fff; cursor: pointer; }\n.filter-btn.active { background: linear-gradient(135deg, #00d4ff, #8b5cf6); color: #000; font-weight: bold; }\n.project-card { background: #252525; border-radius: 12px; padding: 20px; margin-bottom: 15px; border-left: 4px solid #00d4ff; transition: 0.3s; cursor: pointer; }\n.project-card:hover { transform: translateX(5px); box-shadow: 0 4px 20px rgba(0, 212, 255, 0.2); }\n.project-id { color: #00ffcc; font-size: 12px; font-weight: bold; }\n.project-name { font-size: 18px; font-weight: bold; margin: 5px 0; }\n.project-desc { color: #a0aec0; font-size: 14px; margin: 8px 0; line-height: 1.5; }\n.badges { display: flex; gap: 10px; margin-top: 12px; flex-wrap: wrap; }\n.badge { padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 600; }\n.badge-complete { background: linear-gradient(135deg, #10b981, #059669); color: #fff; }\n.badge-andamento { background: linear-gradient(135deg, #00d4ff, #0891b2); color: #000; }\n.badge-gate { background: #333; color: #fff; }\n.stats-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 20px; }\n.stat-card { background: #252525; border-radius: 12px; padding: 20px; text-align: center; }\n.stat-number { font-size: 32px; font-weight: bold; color: #00d4ff; }\n.stat-label { color: #a0aec0; font-size: 14px; margin-top: 5px; }\n.stat-card.complete .stat-number { color: #10b981; }\n.stat-card.andamento .stat-number { color: #f59e0b; }\n.files-list { list-style: none; }\n.files-list li { padding: 15px; border-bottom: 1px solid #333; display: flex; justify-content: space-between; align-items: center; }\n.folder { color: #ffd700; }\n.file-btn { background: linear-gradient(135deg, #00d4ff, #8b5cf6); color: #000; padding: 6px 14px; border-radius: 8px; text-decoration: none; font-size: 12px; font-weight: 600; }\n.detail-card { background: #252525; border-radius: 16px; padding: 25px; margin-bottom: 20px; }\n.detail-title { font-size: 24px; color: #00d4ff; margin-bottom: 5px; }\n.detail-id { color: #00ffcc; font-size: 14px; margin-bottom: 15px; }\n.detail-desc { color: #a0aec0; font-size: 15px; line-height: 1.6; margin-bottom: 20px; padding: 15px; background: #1e1e1e; border-radius: 10px; border-left: 3px solid #8b5cf6; }\n.detail-section { margin-bottom: 20px; }\n.detail-section h4 { color: #8b5cf6; margin-bottom: 10px; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }\n.detail-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #333; }\n.detail-label { color: #a0aec0; }\n.detail-value { color: #fff; font-weight: 500; }\n.back-btn { display: inline-flex; align-items: center; gap: 8px; background: #333; color: #fff; padding: 10px 20px; border-radius: 10px; text-decoration: none; margin-bottom: 20px; }\n.ksf-list { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 8px; }\n.ksf-item { padding: 6px 12px; border-radius: 8px; font-size: 12px; background: #333; color: #a0aec0; }\n.ksf-item.done { background: linear-gradient(135deg, #10b981, #059669); color: #fff; }\n.deliverable-item { display: flex; justify-content: space-between; align-items: center; padding: 10px; background: #1e1e1e; border-radius: 8px; margin-bottom: 10px; }\n.footer { text-align: center; padding: 30px; color: #666; }\n@media (max-width: 600px) { .header { flex-direction: column; text-align: center; } .nav { width: 100%; justify-content: center; } }\n</style>\n</head>\n<body>\n<div class="header">\n<div class="logo"><span>⚡</span> FactoryOS Dashboard</div>\n<div class="nav">\n<a href="/?mode=projetos" class="' + (mode === 'projetos' ? 'active' : '') + '">📊 Projetos</a>\n<a href="/?mode=arquivos" class="' + (mode === 'arquivos' ? 'active' : '') + '">📁 Arquivos</a>\n<a href="/?mode=fluxograma" class="' + (mode === 'fluxograma' ? 'active' : '') + '">🔄 Metodologia</a>\n<a href="/?mode=reunioes" class="' + (mode === 'reunioes' ? 'active' : '') + '">📅 Reuniões</a>\n</div>\n</div>\n';
    
    try {
        if (mode === 'fluxograma') {
            const fluxPath = path.join(BASE_PATH, 'fluxograma-metodologia.html');
            if (fs.existsSync(fluxPath)) {
                const fluxHtml = fs.readFileSync(fluxPath, 'utf-8');
                html += '<div class="section"><h2>Metodologia FactoryOS</h2>' + fluxHtml + '</div>';
            } else {
                html += '<div class="section"><h2>Metodologia</h2><p>Fluxograma em manutencao</p></div>';
            }
        } else if (mode === 'arquivos') {
            const targetPath = req.query.path ? path.join(BASE_PATH, req.query.path) : BASE_PATH;
            html += '<div class="section"><h2>Arquivos</h2>';
            if (fs.existsSync(targetPath)) {
                const entries = fs.readdirSync(targetPath, { withFileTypes: true });
                html += '<ul class="files-list">';
                for (const entry of entries) {
                    if (entry.name.startsWith('.')) continue;
                    const fullPath = path.join(targetPath, entry.name);
                    const relPath = req.query.path ? req.query.path + '/' + entry.name : entry.name;
                    if (entry.isDirectory()) {
                        html += '<li><span class="folder"><a href="/?mode=arquivos&path=' + relPath + '" style="color:#ffd700;text-decoration:none;">📁 ' + entry.name + '</a></span><span style="color:#666;">pasta</span></li>';
                    } else if (entry.isFile()) {
                        let icon = '📄';
                        const ext = path.extname(entry.name).toLowerCase();
                        if (ext === '.html') icon = '⚙️';
                        else if (ext === '.md') icon = '📝';
                        const stats = fs.statSync(fullPath);
                        const size = stats.size < 1024 ? stats.size + 'B' : (stats.size/1024).toFixed(1) + 'KB';
                        html += '<li><span>' + icon + ' ' + entry.name + '</span><a href="/api/download?file=' + relPath + '" class="file-btn" download>Download</a></li>';
                    }
                }
                html += '</ul>';
            }
            html += '</div>';
        } else if (mode === 'reunioes') {
            html += '<div class="section"><h2>📅 Atas de Reuniões</h2>';
            const reunioesPath = path.join(BASE_PATH, 'REUNIOES');
            let temReuniao = false;
            if (fs.existsSync(reunioesPath)) {
                const entries = fs.readdirSync(reunioesPath).sort().reverse();
                html += '<div style="display:grid;gap:15px;">';
                for (const entry of entries) {
                    if (entry.endsWith('.md')) {
                        temReuniao = true;
                        const dateStr = entry.replace('REUNIAO_', '').replace('.md', '');
                        html += '<a href="/api/download?file=REUNIOES/' + entry + '" class="project-card" style="text-decoration:none;display:block;" download>';
                        html += '<div class="project-id">' + dateStr + '</div>';
                        html += '<div class="project-name">Daily Strategic Sync</div>';
                        html += '<div class="badges"><span class="badge badge-gate">📄 Download ATA</span></div></a>';
                    }
                }
                html += '</div>';
            }
            if (!temReuniao) {
                html += '<p style="color:#666;text-align:center;padding:40px;">Nenhuma ata encontrada.</p>';
            }
            html += '<div style="margin-top:30px;padding:20px;background:#252525;border-radius:12px;text-align:center;">';
            html += '<p style="color:#a0aec0;margin-bottom:10px;">📅 Próxima reunião: Hoje às 12:00</p>';
            html += '</div></div>';
        } else if (projeto) {
            const projectKey = projeto.toLowerCase();
            const projectName = projeto.replace('-factoryos', '').toUpperCase().replace('/', '');
            const descricao = descricoes[projectKey] || 'Projeto do FactoryOS';
            html += '<a href="/?mode=projetos&filter=' + filter + '" class="back-btn">← Voltar</a>';
            html += '<div class="detail-card">';
            html += '<div class="detail-title">' + projectName + '</div><div class="detail-id">Projeto FactoryOS</div>';
            html += '<div class="detail-desc">' + descricao + '</div>';
            html += '<div class="detail-section"><h4>Status</h4><div class="badges"><span class="badge badge-complete">✅ COMPLETO</span><span class="badge badge-gate">QA Aprovado</span></div></div>';
            html += '<div class="detail-section"><h4>KSFs Definidos</h4><div class="ksf-list"><div class="ksf-item done">✅ Todos OK</div></div></div>';
            html += '<div class="detail-section"><h4>Entregaveis</h4>';
            html += '<div class="deliverable-item"><span>Dashboard</span><a href="https://factoryos-dashboard.vercel.app/" class="file-btn" target="_blank">Acessar</a></div>';
            html += '<div class="deliverable-item"><span>Metodologia</span><a href="/?mode=fluxograma" class="file-btn">Ver</a></div></div></div>';
        } else {
            const indexPath = path.join(BASE_PATH, 'INDEX.md');
            const content = fs.readFileSync(indexPath, 'utf-8');
            const lines = content.split('\n');
            const tableLines = lines.slice(0, 20).filter(function(l) { return l.includes('PROJ-') && l.includes('|'); });
            let countConcluido = 0;
            let countAndamento = 0;
            const projetos = [];
            tableLines.forEach(function(line) {
                const cols = line.split('|').slice(1, -1).map(function(c) { return c.trim(); });
                if (cols.length >= 3) {
                    const id = cols[0];
                    const titulo = cols[1];
                    const statusRaw = cols[2].replace(/[✅🔴🟡🔵🔶]/g, '').replace(/\s+/g, ' ').trim();
                    const gate = cols[3] || '';
                    const statusLower = statusRaw.toLowerCase();
                    let statusClass = 'badge-aguardando';
                    let statusText = statusRaw;
                    let displayStatus = 'PENDENTE';
                    if (statusLower.includes('conclu') || statusLower.includes('completo')) {
                        statusClass = 'badge-complete';
                        statusText = 'CONCLUIDO';
                        displayStatus = 'CONCLUIDO';
                        countConcluido++;
                    } else if (statusLower.includes('andamento') || statusLower.includes('planejamento')) {
                        statusClass = 'badge-andamento';
                        statusText = 'EM ANDAMENTO';
                        displayStatus = 'ANDAMENTO';
                        countAndamento++;
                    }
                    projetos.push({ id, titulo, statusClass, statusText, gate, displayStatus });
                }
            });
            const total = projetos.length;
            html += '<div class="stats-row"><div class="stat-card"><div class="stat-number">' + total + '</div><div class="stat-label">Total</div></div>';
            html += '<div class="stat-card complete"><div class="stat-number">' + countConcluido + '</div><div class="stat-label">Concluidos</div></div>';
            html += '<div class="stat-card andamento"><div class="stat-number">' + countAndamento + '</div><div class="stat-label">Em Andamento</div></div></div>';
            html += '<div class="filters">';
            html += '<button class="filter-btn ' + (filter === 'todos' ? 'active' : '') + '" onclick="window.location.href=\'/?mode=projetos&filter=todos\'">Todos</button>';
            html += '<button class="filter-btn ' + (filter === 'concluido' ? 'active' : '') + '" onclick="window.location.href=\'/?mode=projetos&filter=concluido\'">Concluidos</button>';
            html += '<button class="filter-btn ' + (filter === 'andamento' ? 'active' : '') + '" onclick="window.location.href=\'/?mode=projetos&filter=andamento\'">Em Andamento</button></div>';
            html += '<div class="section"><h2>Projetos</h2>';
            const filtered = projetos.filter(function(p) { if (filter === 'todos') return true; return p.displayStatus.toLowerCase() === filter; });
            if (filtered.length === 0) {
                html += '<p style="color:#666;text-align:center;padding:40px;">Nenhum projeto encontrado</p>';
            } else {
                filtered.forEach(function(p) {
                    const projKey = p.id.toLowerCase() + '-factoryos';
                    const desc = descricoes[projKey] || '';
                    html += '<a href="/?mode=projetos&filter=' + filter + '&projeto=' + p.id.toLowerCase() + '-factoryos" style="text-decoration:none;color:inherit;display:block;">';
                    html += '<div class="project-card"><div class="project-id">' + p.id + '</div><div class="project-name">' + p.titulo + '</div>';
                    if (desc) { html += '<div class="project-desc">' + desc + '</div>'; }
                    html += '<div class="badges"><span class="badge ' + p.statusClass + '">' + p.statusText + '</span><span class="badge badge-gate">' + p.gate + '</span></div></div></a>';
                });
            }
            html += '</div>';
        }
    } catch (e) {
        html += '<div class="section"><p>Erro: ' + e.message + '</p></div>';
    }
    html += '<div class="footer"><small>FactoryOS Dashboard v2.3 • ' + new Date().toLocaleString('pt-BR') + '</small></div></body></html>';
    res.setHeader('Content-Type', 'text/html');
    res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
    res.status(200).send(html);
};
