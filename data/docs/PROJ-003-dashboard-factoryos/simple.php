<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FactoryOS Dashboard</title>
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: #0a1628;
            color: #fff;
            padding: 20px;
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
        .btn { background: #00d4ff; color: #000; padding: 10px 20px; border-radius: 5px; text-decoration: none; }
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
        .badges { display: flex; gap: 10px; margin-top: 10px; }
        .badge { padding: 4px 12px; border-radius: 20px; font-size: 12px; }
        .badge-complete { background: #10b981; color: #fff; }
        .badge-aguardando { background: #f59e0b; color: #000; }
        .badge-andamento { background: #00d4ff; color: #000; }
        .tabs { display: flex; gap: 10px; margin-bottom: 20px; }
        .tab { background: #252525; padding: 10px 20px; border-radius: 5px; cursor: pointer; border: none; color: #fff; }
        .tab.active { background: #00d4ff; color: #000; }
        .loading { text-align: center; padding: 40px; color: #666; }
        .files-list { list-style: none; }
        .files-list li { padding: 10px; border-bottom: 1px solid #333; display: flex; justify-content: space-between; }
        .files-list li:hover { background: #252525; }
        .folder { color: #ffd700; }
        .file { color: #fff; }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">⚡ FactoryOS Dashboard</div>
        <div>
            <a href="?projetos" class="btn" style="background:#00d4ff;color:#000">Projetos</a>
            <a href="?arquivos" class="btn" style="background:#333;color:#fff">Arquivos</a>
        </div>
    </div>

    <?php
    $api_base = '';
    $mode = $_GET['mode'] ?? 'projetos';
    
    function fetchAPI($url) {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 10);
        curl_setopt($ch, CURLOPT_HTTPHEADER, ['Cache-Control: no-cache']);
        $response = curl_exec($ch);
        curl_close($ch);
        return $response;
    }
    ?>
    
    <?php if ($mode === 'projetos'): ?>
    <div class="section">
        <h2>📊 Projetos</h2>
        <div id="projects-list">
            <?php
            $json = fetchAPI($api_base . '/api/projetos');
            $data = json_decode($json, true);
            
            if ($data && isset($data['data']['projetos'])) {
                foreach ($data['data']['projetos'] as $p) {
                    $statusClass = '';
                    $statusText = '';
                    $statusLower = strtolower($p['status']);
                    if (strpos($statusLower, 'conclu') !== false || strpos($statusLower, 'completo') !== false) {
                        $statusClass = 'badge-complete';
                        $statusText = 'CONCLUÍDO';
                    } elseif (strpos($statusLower, 'andamento') !== false) {
                        $statusClass = 'badge-andamento';
                        $statusText = 'EM ANDAMENTO';
                    } else {
                        $statusClass = 'badge-aguardando';
                        $statusText = $p['status'];
                    }
                    
                    echo '<div class="project-card">';
                    echo '<div class="project-id">' . htmlspecialchars($p['id']) . '</div>';
                    echo '<div class="project-name">' . htmlspecialchars($p['titulo']) . '</div>';
                    echo '<div class="badges">';
                    echo '<span class="badge ' . $statusClass . '">' . $statusText . '</span>';
                    echo '<span class="badge" style="background:#333;">' . htmlspecialchars($p['gate']) . '</span>';
                    echo '</div></div>';
                }
            } else {
                echo '<div class="loading">Erro ao carregar projetos</div>';
            }
            ?>
        </div>
    </div>
    <?php elseif ($mode === 'arquivos'): ?>
    <div class="section">
        <h2>📁 Arquivos</h2>
        <ul class="files-list">
            <?php
            $json = fetchAPI($api_base . '/api/arquivos');
            $data = json_decode($json, true);
            
            if ($data && isset($data['folders'])) {
                foreach ($data['folders'] as $f) {
                    echo '<li><span class="folder">📁 ' . htmlspecialchars($f['name']) . '</span></li>';
                }
                foreach ($data['files'] as $f) {
                    $icon = '📄';
                    if (strpos($f['name'], '.html') !== false) $icon = '⚙️';
                    if (strpos($f['name'], '.md') !== false) $icon = '📝';
                    if (strpos($f['name'], '.png') !== false || strpos($f['name'], '.jpg') !== false) $icon = '🖼️';
                    echo '<li><span class="file">' . $icon . ' ' . htmlspecialchars($f['name']) . '</span><span>' . $f['size'] . '</span></li>';
                }
            } else {
                echo '<li class="loading">Erro ao carregar arquivos</li>';
            }
            ?>
        </ul>
    </div>
    <?php endif; ?>
    
    <div style="text-align:center;padding:20px;color:#666;">
        <small>Atualizado: <?php echo date('d/m/Y H:i:s'); ?></small>
    </div>
</body>
</html>
