/**
 * FactoryOS Dashboard - File Browser API
 * Extensão PROJ-003-EXT — File Browser
 * Navegação e download de arquivos
 */

const fs = require('fs');
const path = require('path');

// Diretório base permitido (mesmo do server.js)
const BASE_DIR = path.resolve(__dirname, '..', '..', '..', '..');

// Pastas bloqueadas por segurança
const BLOCKED_PATHS = ['.git', 'node_modules', '.openclaw'];

/**
 * Normaliza o path e prevente directory traversal
 * @param {string} requestPath - Path solicitado
 * @returns {string|null} Path normalizado ou null se inválido
 */
function normalizePath(requestPath) {
  if (!requestPath) return null;
  
  // Remove query strings e fragmentos
  const cleanPath = requestPath.split('?')[0].split('#')[0];
  
  // Decodifica URL
  const decodedPath = decodeURIComponent(cleanPath);
  
  // Impede paths que começam com /
  if (decodedPath.startsWith('/')) return null;
  
  // Impede directory traversal (../)
  const normalized = path.normalize(decodedPath);
  if (normalized.includes('..')) return null;
  
  // Converte para path absoluto
  const absolutePath = path.resolve(BASE_DIR, normalized);
  
  // Garante que está dentro do BASE_DIR
  if (!absolutePath.startsWith(BASE_DIR)) return null;
  
  return absolutePath;
}

/**
 * Verifica se o path está em lista de bloqueio
 * @param {string} absolutePath - Path absoluto
 * @returns {boolean}
 */
function isBlocked(absolutePath) {
  const relativePath = path.relative(BASE_DIR, absolutePath);
  return BLOCKED_PATHS.some(blocked => 
    relativePath === blocked || 
    relativePath.startsWith(blocked + '/')
  );
}

/**
 * Formata tamanho do arquivo para leitura humana
 * @param {number} bytes - Tamanho em bytes
 * @returns {string} - Tamanho formatado (ex: "4KB")
 */
function formatSize(bytes) {
  if (bytes === 0) return '0B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + sizes[i];
}

/**
 * Determina o tipo do arquivo para ícone
 * @param {string} filename - Nome do arquivo
 * @returns {string} - Tipo do arquivo
 */
function getFileType(filename) {
  const ext = path.extname(filename).toLowerCase();
  const typeMap = {
    '.html': 'html',
    '.md': 'markdown',
    '.js': 'javascript',
    '.sh': 'shell',
    '.png': 'image',
    '.jpg': 'image',
    '.jpeg': 'image',
    '.gif': 'image',
    '.webp': 'image',
    '.pdf': 'pdf',
    '.zip': 'archive',
    '.tar': 'archive',
    '.gz': 'archive',
    '.rar': 'archive'
  };
  return typeMap[ext] || 'unknown';
}

/**
 * Retorna ícone baseado no tipo do arquivo
 * @param {string} type - Tipo do arquivo
 * @returns {string} - Emoji do ícone
 */
function getFileIcon(type) {
  const iconMap = {
    'html': '📄',
    'markdown': '📝',
    'javascript': '📜',
    'shell': '📜',
    'image': '🖼️',
    'pdf': '📕',
    'archive': '📦'
  };
  return iconMap[type] || '📄';
}

/**
 * Lista o conteúdo de um diretório
 * GET /api/arquivos?path=docs/projetos
 */
function listDirectory(absolutePath) {
  const entries = fs.readdirSync(absolutePath, { withFileTypes: true });
  
  const folders = [];
  const files = [];
  
  for (const entry of entries) {
    const fullPath = path.join(absolutePath, entry.name);
    const relativePath = path.relative(BASE_DIR, fullPath);
    
    // Pula arquivos e pastas ocultas (exceto as bloqueadas explicitamente)
    if (entry.name.startsWith('.')) continue;
    
    if (entry.isDirectory()) {
      folders.push({
        name: entry.name,
        path: relativePath
      });
    } else if (entry.isFile()) {
      const stats = fs.statSync(fullPath);
      const type = getFileType(entry.name);
      
      files.push({
        name: entry.name,
        path: relativePath,
        size: formatSize(stats.size),
        type: type,
        icon: getFileIcon(type)
      });
    }
  }
  
  // Ordena: pastas primeiro, depois arquivos (ambos alfabeticamente)
  folders.sort((a, b) => a.name.localeCompare(b.name));
  files.sort((a, b) => a.name.localeCompare(b.name));
  
  return {
    path: path.relative(BASE_DIR, absolutePath),
    folders,
    files
  };
}

/**
 * Handler principal da API de arquivos
 * @param {Object} req - Request do Express/HTTP
 * @param {Object} res - Response
 */
function filesHandler(req, res) {
  try {
    // Determina se é download ou listagem
    const isDownload = req.params && req.params.path;
    
    if (isDownload) {
      // Download de arquivo: GET /api/arquivos/:path
      const absolutePath = normalizePath(req.params.path);
      
      if (!absolutePath) {
        return res.status(403).json({ error: 'Path inválido' });
      }
      
      if (isBlocked(absolutePath)) {
        return res.status(403).json({ error: 'Acesso negado' });
      }
      
      if (!fs.existsSync(absolutePath)) {
        return res.status(404).json({ error: 'Arquivo não encontrado' });
      }
      
      if (!fs.statSync(absolutePath).isFile()) {
        return res.status(403).json({ error: 'Path não é um arquivo' });
      }
      
      const filename = path.basename(absolutePath);
      
      res.setHeader('Content-Type', 'application/octet-stream');
      res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
      
      const fileStream = fs.createReadStream(absolutePath);
      fileStream.pipe(res);
      
    } else {
      // Listagem de diretório: GET /api/arquivos?path=...
      const requestedPath = req.query.path || '';
      const absolutePath = normalizePath(requestedPath);
      
      if (!absolutePath) {
        return res.status(403).json({ error: 'Path inválido' });
      }
      
      if (isBlocked(absolutePath)) {
        return res.status(403).json({ error: 'Acesso negado' });
      }
      
      if (!fs.existsSync(absolutePath)) {
        return res.status(404).json({ error: 'Diretório não encontrado' });
      }
      
      if (!fs.statSync(absolutePath).isDirectory()) {
        return res.status(403).json({ error: 'Path não é um diretório' });
      }
      
      const result = listDirectory(absolutePath);
      res.json(result);
    }
    
  } catch (error) {
    console.error('Files API Error:', error);
    res.status(500).json({ error: 'Erro interno do servidor' });
  }
}

/**
 * Registra as rotas no Express
 * @param {Object} app - Instância do Express
 */
function registerRoutes(app) {
  // GET /api/arquivos - Lista diretório
  app.get('/api/arquivos', filesHandler);
  
  // GET /api/arquivos/:path - Download de arquivo
  app.get('/api/arquivos/:path(*)', filesHandler);
  
  console.log('[Files API] Rotas registradas:');
  console.log('  GET /api/arquivos?path=...');
  console.log('  GET /api/arquivos/:path');
}

module.exports = {
  filesHandler,
  registerRoutes,
  normalizePath,
  isBlocked,
  // Exports para testes
  BLOCKED_PATHS,
  BASE_DIR
};
