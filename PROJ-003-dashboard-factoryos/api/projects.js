// FactoryOS Dashboard API - Busca projetos do GitHub em tempo real
const GITHUB_API = 'https://api.github.com/repos/bastoscaio68/factoryos-dashboard/contents';

// Pastas dos projetos
const PROJECTS = [
    'PROJ-001-procedure-check',
    'PROJ-002-visual-improvement',
    'PROJ-003-dashboard-factoryos',
    'PROJ-004-trading-dashboard'
];

// Arquivos de status por projeto
const STATUS_FILES = {
    'PROJ-001-procedure-check': 'STATUS.md',
    'PROJ-002-visual-improvement': 'STATUS.md',
    'PROJ-003-dashboard-factoryos/STATUS.md': 'STATUS.md',
    'PROJ-004-trading-dashboard': 'STATUS.md'
};

// Outputs por projeto (hardcoded pois outputs não estão padronizados)
const OUTPUTS = {
    'PROJ-001-procedure-check': ['SLIDES-001.html', 'QA-REPORT.md'],
    'PROJ-002-visual-improvement': ['SLIDES-001-MELHORADO.html', 'ROADMAP.md', 'BUDGET-DETALHADO.md'],
    'PROJ-003-dashboard-factoryos': ['DASHBOARD.html', 'MANUAL.html', 'DESIGN-SYSTEM.md'],
    'PROJ-004-trading-dashboard': ['REQUEST.md', 'RESPONSIBILITY_MATRIX.md', 'STATUS.md', 'RD-001.md', 'DESIGN-001.md', 'MC-001.md', 'IA-ANALYST.md', 'INTEGRATION.md', 'bot_api.py', 'trade.py', 'dashboard.html']
};

// Nomes e descrições
const PROJECT_INFO = {
    'PROJ-001-procedure-check': { name: 'Procedure Check + Marketing', desc: 'Procedure check completo de todos os 26 agentes do FactoryOS e produção de material de marketing visual inicial.' },
    'PROJ-002-visual-improvement': { name: 'Melhoria da Qualidade Visual', desc: 'Diagnóstico e plano de ação para melhorar a qualidade visual do ecossistema FactoryOS, incluindo Design System e roadmap de implementação.' },
    'PROJ-003-dashboard-factoryos': { name: 'FactoryOS Dashboard', desc: 'Plataforma web para gestão visual de todos os projetos do FactoryOS, com monitoramento em tempo real, status de gates e KSFs.' },
    'PROJ-004-trading-dashboard': { name: 'Trading Dashboard Quantitativo', desc: 'Dashboard inteligente para trading quantitativo com registro de trades, análise de performance, recomendações automáticas e integração com bots Pionex.' }
};

async function fetchFile(path) {
    try {
        const response = await fetch(`${GITHUB_API}/${path}?ref=dashboard-main`);
        if (!response.ok) return null;
        const data = await response.json();
        const content = Buffer.from(data.content, 'base64').toString('utf-8');
        return content;
    } catch (e) {
        return null;
    }
}

function parseStatus(content, projectId) {
    if (!content) return null;
    
    const info = PROJECT_INFO[projectId] || { name: projectId, desc: '' };
    
    // Extrair status
    const statusMatch = content.match(/status[:\s]+(\w+)/i);
    const gateMatch = content.match(/gate[:\s]+(\d+)/i);
    const ksfsMatch = content.match(/KSFs?[:\s]*(\d+)\s*\/\s*(\d+)/i);
    
    let status = statusMatch ? statusMatch[1].toLowerCase() : 'unknown';
    if (status === 'concluído' || status === 'concluido') statusKey = 'concluido';
    else if (status.includes('andamento') || status.includes('ativo')) statusKey = 'active';
    else if (status.includes('aguardando') || status.includes('valida')) statusKey = 'aguardando';
    else statusKey = 'unknown';
    
    const gate = gateMatch ? parseInt(gateMatch[1]) : 1;
    const ksfsCompleted = ksfsMatch ? parseInt(ksfsMatch[1]) : 0;
    const ksfsTotal = ksfsMatch ? parseInt(ksfsMatch[2]) : 5;
    
    return {
        id: projectId,
        name: info.name,
        descricao: info.desc,
        status: statusMatch ? statusMatch[1] : 'Desconhecido',
        statusKey: statusKey,
        gate: gate,
        gatesTotal: 5,
        ksfs: { completed: ksfsCompleted, total: ksfsTotal },
        outputs: OUTPUTS[projectId] || [],
        lastUpdate: new Date().toISOString()
    };
}

export default async function handler(req, res) {
    const { project } = req.query;
    
    try {
        if (project) {
            // Retornar projeto específico
            const statusPath = project === 'PROJ-003-dashboard-factoryos' 
                ? `${project}/STATUS.md` 
                : `${project}/STATUS.md`;
            const content = await fetchFile(statusPath);
            const data = parseStatus(content, project);
            res.status(200).json(data);
        } else {
            // Retornar todos os projetos
            const projects = [];
            for (const proj of PROJECTS) {
                const statusPath = proj === 'PROJ-003-dashboard-factoryos' 
                    ? `${proj}/STATUS.md` 
                    : `${proj}/STATUS.md`;
                const content = await fetchFile(statusPath);
                const data = parseStatus(content, proj);
                if (data) projects.push(data);
            }
            
            // Calcular stats
            const stats = {
                total: projects.length,
                ativos: projects.filter(p => p.statusKey === 'active').length,
                aguardando: projects.filter(p => p.statusKey === 'aguardando').length,
                concluidos: projects.filter(p => p.statusKey === 'concluido').length
            };
            
            res.status(200).json({ projects, stats });
        }
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
}
