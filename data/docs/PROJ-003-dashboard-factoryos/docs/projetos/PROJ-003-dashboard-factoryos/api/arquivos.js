const fs = require('fs');
const path = require('path');

module.exports = async (req, res) => {
    // CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }
    
    try {
        const BASE_PATH = path.join(process.cwd(), 'docs');
        const queryPath = req.query.path || '';
        
        // Normalizar path
        if (queryPath.includes('..') || queryPath.startsWith('/')) {
            return res.status(403).json({ error: 'Path inválido' });
        }
        
        const absolutePath = path.join(BASE_PATH, queryPath);
        
        if (!fs.existsSync(absolutePath)) {
            return res.status(404).json({ error: 'Diretório não encontrado' });
        }
        
        const stats = fs.statSync(absolutePath);
        
        // Se for arquivo, faz download
        if (stats.isFile()) {
            const filename = path.basename(absolutePath);
            res.setHeader('Content-Type', 'application/octet-stream');
            res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
            const stream = fs.createReadStream(absolutePath);
            stream.pipe(res);
            return;
        }
        
        // Lista diretório
        const entries = fs.readdirSync(absolutePath, { withFileTypes: true });
        const folders = [];
        const files = [];
        
        const BLOCKED = ['.git', 'node_modules', '.openclaw', '.vercel'];
        
        for (const entry of entries) {
            if (entry.name.startsWith('.')) continue;
            if (BLOCKED.some(b => entry.name.startsWith(b))) continue;
            
            const fullPath = path.join(absolutePath, entry.name);
            const relPath = path.relative(BASE_PATH, fullPath);
            
            if (entry.isDirectory()) {
                folders.push({ name: entry.name, path: relPath });
            } else if (entry.isFile()) {
                const ext = path.extname(entry.name).toLowerCase();
                const icons = {
                    '.md': '📝', '.js': '📜', '.html': '⚙️', '.css': '🎨',
                    '.json': '📋', '.sh': '🔧', '.png': '🖼️', '.jpg': '🖼️',
                    '.pdf': '📕', '.zip': '📦'
                };
                const icon = icons[ext] || '📄';
                const size = fs.statSync(fullPath).size;
                const sizeStr = size < 1024 ? `${size}B` : `${(size/1024).toFixed(1)}KB`;
                
                files.push({
                    name: entry.name,
                    path: relPath,
                    size: sizeStr,
                    icon: icon
                });
            }
        }
        
        folders.sort((a, b) => a.name.localeCompare(b.name));
        files.sort((a, b) => a.name.localeCompare(b.name));
        
        res.status(200).json({
            path: queryPath,
            folders,
            files
        });
    } catch (e) {
        console.error('Files API Error:', e);
        res.status(500).json({ error: 'Erro interno' });
    }
};
