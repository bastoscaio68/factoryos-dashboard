# FactoryOS Dashboard Design System

> Documento técnico de design system para o FactoryOS Dashboard
> Versão: 1.0.0
> Público: Caio Bastos (single-user)

---

## 1. Cores (Colors)

### 1.1 Cores Primárias (FactoryOS)

```css
:root {
  /* Primárias */
  --color-deep-ocean: #0a1628;
  --color-electric-blue: #00d4ff;
  --color-neon-cyan: #00ffcc;
  
  /* Neutros */
  --color-bg-primary: #0a1628;
  --color-bg-secondary: #0f1f35;
  --color-bg-tertiary: #152a47;
  --color-border: rgba(0, 212, 255, 0.2);
  --color-text-primary: #ffffff;
  --color-text-secondary: rgba(255, 255, 255, 0.7);
  --color-text-muted: rgba(255, 255, 255, 0.5);
}
```

### 1.2 Cores Derivadas

```css
:root {
  /* Electric Blue - Variações */
  --color-electric-hover: #00b8e6;
  --color-electric-light: rgba(0, 212, 255, 0.15);
  --color-electric-muted: rgba(0, 212, 255, 0.4);
  
  /* Neon Cyan - Variações */
  --color-neon-hover: #00e6b8;
  --color-neon-light: rgba(0, 255, 204, 0.15);
  --color-neon-muted: rgba(0, 255, 204, 0.4);
  
  /* Superfícies */
  --color-surface-elevated: rgba(15, 31, 53, 0.95);
  --color-surface-glass: rgba(10, 22, 40, 0.8);
}
```

### 1.3 Cores Semânticas

```css
:root {
  /* Estados */
  --color-success: #10b981;
  --color-success-bg: rgba(16, 185, 129, 0.15);
  --color-success-border: rgba(16, 185, 129, 0.3);
  
  --color-warning: #f59e0b;
  --color-warning-bg: rgba(245, 158, 11, 0.15);
  --color-warning-border: rgba(245, 158, 11, 0.3);
  
  --color-error: #ef4444;
  --color-error-bg: rgba(239, 68, 68, 0.15);
  --color-error-border: rgba(239, 68, 68, 0.3);
  
  --color-info: #3b82f6;
  --color-info-bg: rgba(59, 130, 246, 0.15);
  --color-info-border: rgba(59, 130, 246, 0.3);
}
```

### 1.4 Cores de Status de Projeto

```css
:root {
  --color-status-active: #10b981;
  --color-status-paused: #f59e0b;
  --color-status-archived: #6b7280;
  --color-status-pending: #3b82f6;
}
```

---

## 2. Tipografia (Typography)

### 2.1 Fontes

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
  --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
}
```

### 2.2 Hierarchy

```css
:root {
  /* Headings */
  --font-h1: 600 2.5rem/1.2 var(--font-primary);
  --font-h2: 600 2rem/1.25 var(--font-primary);
  --font-h3: 600 1.5rem/1.3 var(--font-primary);
  --font-h4: 600 1.25rem/1.4 var(--font-primary);
  
  /* Body */
  --font-body: 400 1rem/1.6 var(--font-primary);
  --font-body-medium: 500 1rem/1.6 var(--font-primary);
  --font-body-semibold: 600 1rem/1.5 var(--font-primary);
  
  /* Small */
  --font-small: 400 0.875rem/1.5 var(--font-primary);
  --font-small-medium: 500 0.875rem/1.5 var(--font-primary);
  --font-small-semibold: 600 0.875rem/1.4 var(--font-primary);
  
  /* Mono (código) */
  --font-mono-sm: 400 0.75rem/1.6 var(--font-mono);
  --font-mono-base: 400 0.875rem/1.6 var(--font-mono);
  --font-mono-medium: 500 0.875rem/1.6 var(--font-mono);
}
```

---

## 3. Componentes (Components)

### 3.1 Cards

```html
<!-- Card de Projeto -->
<div class="card">
  <div class="card-header">
    <h3 class="card-title">Projeto Alpha</h3>
    <span class="badge badge-success">ativo</span>
  </div>
  <div class="card-body">
    <p class="card-description">Descrição do projeto</p>
    <div class="card-meta">
      <span class="meta-item">
        <span class="icon">📊</span>
        75% completo
      </span>
    </div>
  </div>
  <div class="card-footer">
    <button class="btn btn-primary btn-sm">Ver Detalhes</button>
  </div>
</div>

<!-- Card de Stat -->
<div class="stat-card">
  <div class="stat-icon stat-icon-primary">
    <svg>...</svg>
  </div>
  <div class="stat-content">
    <span class="stat-label">Projetos Ativos</span>
    <span class="stat-value">12</span>
    <span class="stat-change stat-change-positive">+2 esta semana</span>
  </div>
</div>
```

```css
/* Card Base */
.card {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 1.5rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 212, 255, 0.1);
}

/* Card Header */
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.card-title {
  font: var(--font-h4);
  color: var(--color-text-primary);
  margin: 0;
}

/* Card de Stat */
.stat-card {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.25rem;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: 12px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon-primary {
  background: var(--color-electric-light);
  color: var(--color-electric-blue);
}

.stat-value {
  font: var(--font-h2);
  color: var(--color-text-primary);
  font-weight: 700;
}

.stat-label {
  font: var(--font-small);
  color: var(--color-text-secondary);
}
```

### 3.2 Badges

```html
<!-- Badge Tier -->
<span class="badge badge-tier badge-tier-gold">
  <span class="badge-dot"></span>
  Gold Tier
</span>

<!-- Badge Status -->
<span class="badge badge-status badge-status-active">ativo</span>
<span class="badge badge-status badge-status-paused">pausado</span>
<span class="badge badge-status badge-status-pending">pendente</span>

<!-- Badge Simple -->
<span class="badge badge-outline">outline</span>
```

```css
/* Badge Base */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 500;
  border-radius: 100px;
  font-family: var(--font-primary);
}

/* Badge Tier */
.badge-tier {
  background: transparent;
  border: 1px solid currentColor;
}

.badge-tier-gold {
  color: #ffd700;
  border-color: rgba(255, 215, 0, 0.4);
}

.badge-tier-silver {
  color: #c0c0c0;
  border-color: rgba(192, 192, 192, 0.4);
}

.badge-tier-bronze {
  color: #cd7f32;
  border-color: rgba(205, 127, 50, 0.4);
}

.badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

/* Badge Status */
.badge-status-active {
  background: rgba(16, 185, 129, 0.15);
  color: var(--color-status-active);
}

.badge-status-paused {
  background: rgba(245, 158, 11, 0.15);
  color: var(--color-status-paused);
}

.badge-status-pending {
  background: rgba(59, 130, 246, 0.15);
  color: var(--color-status-pending);
}

/* Badge Outline */
.badge-outline {
  background: transparent;
  border: 1px solid var(--color-border);
  color: var(--color-text-secondary);
}
```

### 3.3 Buttons

```html
<!-- Primary -->
<button class="btn btn-primary">Primary Button</button>

<!-- Secondary -->
<button class="btn btn-secondary">Secondary Button</button>

<!-- Ghost -->
<button class="btn btn-ghost">Ghost Button</button>

<!-- Danger -->
<button class="btn btn-danger">Danger Button</button>

<!-- Sizes -->
<button class="btn btn-primary btn-sm">Small</button>
<button class="btn btn-primary btn-md">Medium</button>
<button class="btn btn-primary btn-lg">Large</button>

<!-- With Icon -->
<button class="btn btn-primary">
  <svg class="btn-icon">...</svg>
  Button with Icon
</button>
```

```css
/* Button Base */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-family: var(--font-primary);
  font-weight: 500;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.btn:focus-visible {
  outline: 2px solid var(--color-electric-blue);
  outline-offset: 2px;
}

/* Sizes */
.btn-sm {
  padding: 0.5rem 0.875rem;
  font-size: 0.8125rem;
}

.btn-md {
  padding: 0.625rem 1.25rem;
  font-size: 0.875rem;
}

.btn-lg {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
}

/* Primary */
.btn-primary {
  background: linear-gradient(135deg, var(--color-electric-blue), var(--color-neon-cyan));
  color: var(--color-deep-ocean);
}

.btn-primary:hover {
  filter: brightness(1.1);
  box-shadow: 0 4px 20px rgba(0, 212, 255, 0.3);
}

/* Secondary */
.btn-secondary {
  background: var(--color-bg-tertiary);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
}

.btn-secondary:hover {
  background: var(--color-electric-light);
  border-color: var(--color-electric-blue);
}

/* Ghost */
.btn-ghost {
  background: transparent;
  color: var(--color-text-secondary);
}

.btn-ghost:hover {
  background: var(--color-electric-light);
  color: var(--color-electric-blue);
}

/* Danger */
.btn-danger {
  background: var(--color-error);
  color: white;
}

.btn-danger:hover {
  background: #dc2626;
}

/* Icon Button */
.btn-icon {
  width: 16px;
  height: 16px;
}
```

### 3.4 Tabs (Filtros)

```html
<div class="tabs">
  <button class="tab active">Todos</button>
  <button class="tab">Ativos</button>
  <button class="tab">Pausados</button>
  <button class="tab">Arquivados</button>
</div>
```

```css
/* Tabs Container */
.tabs {
  display: inline-flex;
  gap: 0.25rem;
  padding: 0.25rem;
  background: var(--color-bg-tertiary);
  border-radius: 10px;
}

/* Tab */
.tab {
  padding: 0.5rem 1rem;
  font-family: var(--font-primary);
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-text-secondary);
  background: transparent;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab:hover {
  color: var(--color-text-primary);
}

.tab.active {
  background: var(--color-bg-secondary);
  color: var(--color-text-primary);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}
```

### 3.5 Modal

```html
<div class="modal-overlay">
  <div class="modal" role="dialog" aria-modal="true">
    <div class="modal-header">
      <h2 class="modal-title">Novo Projeto</h2>
      <button class="modal-close" aria-label="Fechar">
        <svg>...</svg>
      </button>
    </div>
    <div class="modal-body">
      <form class="form">
        <div class="form-group">
          <label class="form-label">Nome do Projeto</label>
          <input type="text" class="form-input" placeholder="Digite o nome">
        </div>
        <div class="form-group">
          <label class="form-label">Descrição</label>
          <textarea class="form-input" rows="3"></textarea>
        </div>
      </form>
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary">Cancelar</button>
      <button class="btn btn-primary">Criar Projeto</button>
    </div>
  </div>
</div>
```

```css
/* Modal Overlay */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

/* Modal */
.modal {
  background: var(--color-surface-elevated);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  animation: slideUp 0.3s ease;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--color-border);
}

.modal-title {
  font: var(--font-h4);
  margin: 0;
}

.modal-close {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  color: var(--color-text-secondary);
  border-radius: 6px;
  cursor: pointer;
}

.modal-close:hover {
  background: var(--color-electric-light);
  color: var(--color-electric-blue);
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--color-border);
}
```

### 3.6 Form Inputs

```html
<!-- Text Input -->
<div class="form-group">
  <label class="form-label">Nome</label>
  <input type="text" class="form-input" placeholder="Digite seu nome">
</div>

<!-- With Helper -->
<div class="form-group">
  <label class="form-label">Email</label>
  <input type="email" class="form-input" placeholder="email@exemplo.com">
  <span class="form-helper">Nunca compartilharemos seu email</span>
</div>

<!-- Error State -->
<div class="form-group">
  <label class="form-label">Senha</label>
  <input type="password" class="form-input form-input-error" value="123">
  <span class="form-error">Senha muito curta</span>
</div>

<!-- Select -->
<div class="form-group">
  <label class="form-label">Tipo</label>
  <select class="form-input">
    <option>Selecione...</option>
    <option>Tipo A</option>
    <option>Tipo B</option>
  </select>
</div>
```

```css
/* Form Group */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
}

/* Label */
.form-label {
  font: var(--font-small-semibold);
  color: var(--color-text-primary);
}

/* Input */
.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  font: var(--font-body);
  color: var(--color-text-primary);
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  transition: all 0.2s ease;
}

.form-input::placeholder {
  color: var(--color-text-muted);
}

.form-input:hover {
  border-color: var(--color-electric-muted);
}

.form-input:focus {
  outline: none;
  border-color: var(--color-electric-blue);
  box-shadow: 0 0 0 3px var(--color-electric-light);
}

/* Error State */
.form-input-error {
  border-color: var(--color-error);
}

.form-input-error:focus {
  box-shadow: 0 0 0 3px var(--color-error-bg);
}

.form-error {
  font: var(--font-small);
  color: var(--color-error);
}

.form-helper {
  font: var(--font-small);
  color: var(--color-text-muted);
}

/* Select */
.form-input select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='%23ffffff' viewBox='0 0 16 16'%3E%3Cpath d='M8 11L3 6h10l-5 5z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  padding-right: 2.5rem;
}
```

### 3.7 Tables (Projetos)

```html
<table class="table">
  <thead>
    <tr>
      <th>Projeto</th>
      <th>Status</th>
      <th>Progresso</th>
      <th>Última Atualização</th>
      <th>Ações</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <div class="table-project">
          <span class="project-name">FactoryOS Alpha</span>
          <span class="project-key">FOA-001</span>
        </div>
      </td>
      <td><span class="badge badge-status-active">ativo</span></td>
      <td>
        <div class="progress">
          <div class="progress-bar" style="width: 75%"></div>
        </div>
      </td>
      <td class="table-date">2 horas atrás</td>
      <td>
        <div class="table-actions">
          <button class="btn btn-ghost btn-sm">Editar</button>
        </div>
      </td>
    </tr>
  </tbody>
</table>
```

```css
/* Table */
.table {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--font-primary);
}

.table th {
  text-align: left;
  padding: 1rem;
  font: var(--font-small-semibold);
  color: var(--color-text-secondary);
  border-bottom: 1px solid var(--color-border);
}

.table td {
  padding: 1rem;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text-primary);
}

.table tbody tr {
  transition: background 0.2s ease;
}

.table tbody tr:hover {
  background: var(--color-bg-secondary);
}

/* Table Project Cell */
.table-project {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.project-name {
  font-weight: 500;
}

.project-key {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  font-family: var(--font-mono);
}

.table-date {
  color: var(--color-text-secondary);
  font-size: 0.875rem;
}

/* Table Actions */
.table-actions {
  display: flex;
  gap: 0.5rem;
}
```

### 3.8 Progress Bars (Gates)

```html
<!-- Progress Bar Simple -->
<div class="progress">
  <div class="progress-bar" style="width: 75%"></div>
</div>

<!-- Progress Bar with Label -->
<div class="progress progress-lg">
  <div class="progress-bar" style="width: 50%">
    <span class="progress-label">50%</span>
  </div>
</div>

<!-- Gates Progress -->
<div class="gates-progress">
  <div class="gate gate-completed">
    <span class="gate-icon">✓</span>
  </div>
  <div class="gate-connector"></div>
  <div class="gate gate-active">
    <span class="gate-icon">2</span>
  </div>
  <div class="gate-connector"></div>
  <div class="gate gate-pending">
    <span class="gate-icon">3</span>
  </div>
</div>
```

```css
/* Progress Base */
.progress {
  height: 8px;
  background: var(--color-bg-tertiary);
  border-radius: 100px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, var(--color-electric-blue), var(--color-neon-cyan));
  border-radius: 100px;
  transition: width 0.3s ease;
}

/* Progress Sizes */
.progress-sm {
  height: 4px;
}

.progress-lg {
  height: 12px;
}

/* Gates Progress */
.gates-progress {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
}

.gate {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 600;
  position: relative;
}

.gate-completed {
  background: var(--color-success);
  color: white;
}

.gate-active {
  background: var(--color-electric-blue);
  color: var(--color-deep-ocean);
  box-shadow: 0 0 0 4px var(--color-electric-light);
}

.gate-pending {
  background: var(--color-bg-tertiary);
  color: var(--color-text-muted);
  border: 2px solid var(--color-border);
}

.gate-connector {
  flex: 1;
  height: 2px;
  background: var(--color-border);
  margin: 0 0.5rem;
}

.gate-completed + .gate-connector {
  background: var(--color-success);
}
```

---

## 4. Layout

### 4.1 Grid System

```css
:root {
  --grid-columns: 12;
  --grid-gap: 1.5rem;
  --grid-gap-sm: 0.75rem;
  --grid-gap-lg: 2rem;
}

/* Grid Container */
.grid {
  display: grid;
  grid-template-columns: repeat(var(--grid-columns), 1fr);
  gap: var(--grid-gap);
}

/* Grid Columns */
.col-1 { grid-column: span 1; }
.col-2 { grid-column: span 2; }
.col-3 { grid-column: span 3; }
.col-4 { grid-column: span 4; }
.col-6 { grid-column: span 6; }
.col-8 { grid-column: span 8; }
.col-12 { grid-column: span 12; }

/* Responsive Grid */
@media (max-width: 1024px) {
  .col-lg-6 { grid-column: span 6; }
  .col-lg-12 { grid-column: span 12; }
}

@media (max-width: 768px) {
  .grid {
    grid-template-columns: repeat(6, 1fr);
    gap: var(--grid-gap-sm);
  }
  
  .col-md-6 { grid-column: span 6; }
  .col-md-12 { grid-column: span 12; }
}
```

### 4.2 Flexbox Utilities

```css
/* Container */
.flex {
  display: flex;
}

.flex-col {
  flex-direction: column;
}

.flex-wrap {
  flex-wrap: wrap;
}

/* Justify */
.justify-start { justify-content: flex-start; }
.justify-center { justify-content: center; }
.justify-end { justify-content: flex-end; }
.justify-between { justify-content: space-between; }
.justify-around { justify-content: space-around; }

/* Align */
.items-start { align-items: flex-start; }
.items-center { align-items: center; }
.items-end { align-items: flex-end; }
.items-stretch { align-items: stretch; }

/* Gap */
.gap-1 { gap: 0.25rem; }
.gap-2 { gap: 0.5rem; }
.gap-3 { gap: 0.75rem; }
.gap-4 { gap: 1rem; }
.gap-6 { gap: 1.5rem; }
.gap-8 { gap: 2rem; }

/* Flex Sizes */
.flex-1 { flex: 1; }
.flex-auto { flex: 1 1 auto; }
.flex-none { flex: none; }
```

### 4.3 Spacing Scale

```css
:root {
  /* Base: 8px */
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
}

/* Margin */
.m-0 { margin: 0; }
.mt-1 { margin-top: var(--space-1); }
.mt-2 { margin-top: var(--space-2); }
.mt-4 { margin-top: var(--space-4); }
.mt-6 { margin-top: var(--space-6); }
.mb-1 { margin-bottom: var(--space-1); }
.mb-2 { margin-bottom: var(--space-2); }
.mb-4 { margin-bottom: var(--space-4); }
.mb-6 { margin-bottom: var(--space-6); }
.mx-auto { margin-left: auto; margin-right: auto; }

/* Padding */
.p-0 { padding: 0; }
.p-2 { padding: var(--space-2); }
.p-4 { padding: var(--space-4); }
.p-6 { padding: var(--space-6); }
.px-4 { padding-left: var(--space-4); padding-right: var(--space-4); }
.py-2 { padding-top: var(--space-2); padding-bottom: var(--space-2); }
```

### 4.4 Container Widths

```css
:root {
  --container-sm: 640px;
  --container-md: 768px;
  --container-lg: 1024px;
  --container-xl: 1280px;
  --container-2xl: 1440px;
}

.container {
  width: 100%;
  max-width: var(--container-xl);
  margin: 0 auto;
  padding: 0 var(--space-4);
}

.container-sm { max-width: var(--container-sm); }
.container-lg { max-width: var(--container-lg); }
.container-xl { max-width: var(--container-xl); }
```

---

## 5. Animações

### 5.1 Transitions

```css
/* Transition Utilities */
.transition {
  transition: all 0.2s ease;
}

.transition-fast {
  transition: all 0.15s ease;
}

.transition-slow {
  transition: all 0.3s ease;
}

.transition-colors {
  transition: color 0.2s ease, background-color 0.2s ease, border-color 0.2s ease;
}

.transition-transform {
  transition: transform 0.2s ease;
}

/* Hover Effects */
.hover-lift:hover {
  transform: translateY(-2px);
}

.hover-scale:hover {
  transform: scale(1.02);
}

.hover-glow:hover {
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
}
```

### 5.2 Keyframes

```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeOut {
  from { opacity: 1; }
  to { opacity: 0; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Animation Classes */
.animate-fadeIn { animation: fadeIn 0.3s ease; }
.animate-slideUp { animation: slideUp 0.3s ease; }
.animate-slideDown { animation: slideDown 0.3s ease; }
.animate-scaleIn { animation: scaleIn 0.2s ease; }
.animate-pulse { animation: pulse 2s infinite; }
.animate-spin { animation: spin 1s linear infinite; }
```

### 5.3 Duration Classes

```css
:root {
  --duration-fast: 0.15s;
  --duration-normal: 0.2s;
  --duration-slow: 0.3s;
}

.duration-fast { transition-duration: var(--duration-fast); }
.duration-normal { transition-duration: var(--duration-normal); }
.duration-slow { transition-duration: var(--duration-slow); }

.delay-fast { animation-delay: 0.1s; }
.delay-normal { animation-delay: 0.2s; }
.delay-slow { animation-delay: 0.3s; }
```

---

## 6. Responsividade

### 6.1 Mobile First Breakpoints

```css
:root {
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1440px;
}

/* Mobile (default) */

/* Tablet */
@media (min-width: 768px) {
  .md\:flex { display: flex; }
  .md\:grid { grid-template-columns: repeat(6, 1fr); }
  .md\:col-6 { grid-column: span 6; }
  .md\:hidden { display: none; }
  .md\:block { display: block; }
}

/* Laptop */
@media (min-width: 1024px) {
  .lg\:grid { grid-template-columns: repeat(12, 1fr); }
  .lg\:col-4 { grid-column: span 4; }
  .lg\:col-6 { grid-column: span 6; }
  .lg\:col-8 { grid-column: span 8; }
}

/* Desktop */
@media (min-width: 1280px) {
  .xl\:container { max-width: 1280px; }
}

/* Large Desktop */
@media (min-width: 1440px) {
  .2xl\:container { max-width: 1440px; }
}
```

### 6.2 Grid Adaptativo

```css
/* Dashboard Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-6);
  padding: var(--space-4);
}

@media (min-width: 768px) {
  .dashboard-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: var(--space-6);
    padding: var(--space-6);
  }
}

@media (min-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: var(--space-8);
    padding: var(--space-8);
  }
}

@media (min-width: 1440px) {
  .dashboard-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

### 6.3 Responsive Typography

```css
/* Responsive Font Sizes */
.text-sm { font-size: 0.875rem; }
.text-base { font-size: 1rem; }
.text-lg { font-size: 1.125rem; }
.text-xl { font-size: 1.25rem; }
.text-2xl { font-size: 1.5rem; }
.text-3xl { font-size: 1.875rem; }
.text-4xl { font-size: 2.25rem; }

@media (min-width: 768px) {
  .md\:text-sm { font-size: 0.875rem; }
  .md\:text-lg { font-size: 1.125rem; }
  .md\:text-2xl { font-size