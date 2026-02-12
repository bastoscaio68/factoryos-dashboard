const fs = require('fs');
const path = require('path');

module.exports = async (req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }
    
    const BASE_PATH = path.join(__dirname, 'data', 'docs');
    const filePath = req.query.file;
    
    if (!filePath) {
        return res.status(400).send('Falta parametro file');
    }
    
    const fullPath = path.join(BASE_PATH, filePath);
    
    if (!fs.existsSync(fullPath) || !fs.statSync(fullPath).isFile()) {
        return res.status(404).send('Arquivo nao encontrado');
    }
    
    const content = fs.readFileSync(fullPath);
    const filename = path.basename(filePath);
    
    res.setHeader('Content-Disposition', 'attachment; filename="' + filename + '"');
    res.setHeader('Content-Type', 'application/octet-stream');
    res.status(200).send(content);
};
