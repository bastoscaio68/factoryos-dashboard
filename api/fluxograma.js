const fs = require('fs');
const path = require('path');

module.exports = async (req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
    
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }
    
    // Tentar múltiplas localizações
    const possiblePaths = [
        path.join(__dirname, '..', 'fluxograma-metodologia.html'),
        path.join(__dirname, 'data', 'docs', 'fluxograma-metodologia.html'),
        path.join(__dirname, '..', '..', 'fluxograma-metodologia.html'),
        path.join(process.cwd(), 'fluxograma-metodologia.html')
    ];
    
    let html = null;
    for (const p of possiblePaths) {
        if (fs.existsSync(p)) {
            html = fs.readFileSync(p, 'utf-8');
            break;
        }
    }
    
    if (html) {
        res.setHeader('Content-Type', 'text/html');
        res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
        res.status(200).send(html);
    } else {
        res.status(404).send('Fluxograma nao encontrado: ' + __dirname);
    }
};
