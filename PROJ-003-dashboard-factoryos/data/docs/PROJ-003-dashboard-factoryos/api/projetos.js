const fs = require('fs');
const path = require('path');

module.exports = async (req, res) => {
    // CORS + No Cache
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
    res.setHeader('Pragma', 'no-cache');
    res.setHeader('Expires', '0');
    
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }
    
    try {
        const BASE_PATH = path.join(__dirname, 'data');
        const indexPath = path.join(BASE_PATH, 'INDEX.md');
        
        const content = fs.readFileSync(indexPath, 'utf-8');
        
        // Parse frontmatter
        const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
        const markdown = frontmatterMatch ? frontmatterMatch[2] : content;
        
        // Parse tabela (só a primeira tabela)
        const lines = markdown.split('\n');
        const projetos = [];
        
        const tableLines = lines.slice(0, 20).filter(l => l.includes('PROJ-') && l.includes('|'));
        
        tableLines.forEach((line) => {
            const cols = line.split('|').slice(1, -1).map(c => c.trim());
            if (cols.length >= 3) {
                projetos.push({
                    id: cols[0],
                    titulo: cols[1],
                    status: cols[2].replace(/[✅🔴🟡🔵🔶]/g, '').replace(/\s+/g, ' ').trim(),
                    gate: cols[3] || '',
                    descricao: cols[4] || ''
                });
            }
        });
        
        res.status(200).json({ success: true, data: { projetos } });
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
};
