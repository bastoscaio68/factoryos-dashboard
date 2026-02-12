# GUIA DE IMPLEMENTAÇÃO VISUAL — FactoryOS

**Data:** 2026-02-12  
**Projeto:** Melhoria da Qualidade Visual  
**Versão:** 1.0

---

## 1. RESUMO DO PROJETO

### 1.1 Diagnóstico Consolidado

O FactoryOS apresenta oportunidades significativas de melhoria visual. O diagnóstico identificou que o sistema atual carece de:

- **Ilustrações** ausentes ou básicas
- **Ícones** sem padronização
- **Animações** inexistentes
- **Tipografia** não otimizada
- **Elementos 3D** completamente ausentes

### 1.2 Ferramentas Selecionadas

| Categoria | Ferramenta | Prioridade |
|-----------|------------|------------|
| Ilustrações | unDraw + Blush | Alta |
| Ícones | Phosphor Icons + Font Awesome | Alta |
| Animações | GSAP + Framer Motion | Média |
| Fonts | Google Fonts + Adobe Fonts | Alta |
| 3D | Spline | Média |

---

## 2. IMPLEMENTAÇÃO DE ILUSTRAÇÕES

### 2.1 unDraw

**Instalação via CDN:**

```html
<!-- Inclusão direta no HTML -->
<link rel="stylesheet" href="https://unpkg.com/@undraw/viewer@1.0.0/dist/undraw-viewer.css">
```

**Uso com Pigment (cores personalizadas):**

```javascript
// Instalação
npm install @undraw/illustrations pigment

// Uso com cores customizadas
import undraw from '@undraw/illustrations/pigment';

const svgContent = undraw('analytics', '#6366f1', '#8b5cf6');
document.getElementById('illustration').innerHTML = svgContent;
```

**Exemplo prático em Reveal.js:**

```javascript
// Reveal.js - Adicionar ilustração em slide
 Reveal.on('slidechanged', event => {
    if (event.currentSlide.querySelector('.illustration-container')) {
      const illustration = undraw('teamwork', '#0f172a', '#334155');
      event.currentSlide.querySelector('.illustration-container').innerHTML = illustration;
    }
});
```

**Exemplo HTML:**

```html
<div class="illustration-container" data-color="primary">
  <!-- SVG será injetado aqui -->
</div>

<style>
.illustration-container {
  width: 100%;
  max-width: 600px;
  margin: 2rem auto;
}
.illustration-container svg {
  width: 100%;
  height: auto;
}
</style>
```

### 2.2 Blush

**Instalação via CDN:**

```html
<!-- Blush Player -->
<script src="https://blush.design/player/v1/player.js"></script>
```

**Uso com componente:**

```html
<!-- Ilustração básica -->
<blush-illustration
  collection="illustrations"
  name="teamwork"
  style="--w: 640px; --h: 480px">
</blush-illustration>

<!-- Com cores personalizadas -->
<blush-illustration
  collection="illustrations"
  name="teamwork"
  colors="#6366f1:#8b5cf6:#f59e0b"
  style="--w: 640px; --h: 480px">
</blush-illustration>
```

**Uso via API:**

```javascript
// Gerar URL da ilustração
const baseUrl = 'https://blush.design/api/v1/illustrations';
const illustrationId = 'teamwork';
const colors = '6366f1,8b5cf6,f59e0b';

const url = `${baseUrl}/${illustrationId}?colors=${colors}&format=svg`;
```

**Exemplo em React:**

```jsx
import { useEffect, useRef } from 'react';

const BlushIllustration = ({ name, collection = 'illustrations', colors }) => {
  const containerRef = useRef(null);

  useEffect(() => {
    const initBlush = async () => {
      if (window.Blush) {
        const illustration = await window.Blush.createIllustration({
          container: containerRef.current,
          collection,
          name,
          colors: colors?.split(','),
        });
        return illustration;
      }
    };
    
    const illust = initBlush();
    return () => illust?.then(i => i?.remove());
  }, [name, collection, colors]);

  return <div ref={containerRef} style={{ width: '100%', maxWidth: 640 }} />;
};

export default BlushIllustration;
```

---

## 3. IMPLEMENTAÇÃO DE ÍCONES

### 3.1 Phosphor Icons

**Instalação via NPM:**

```bash
npm install @phosphor-icons/react
```

**Uso básico em React:**

```jsx
import { House, Gear, Bell, User, ArrowRight } from '@phosphor-icons/react';

const Navigation = () => {
  return (
    <nav>
      <House weight="bold" size={24} color="#6366f1" />
      <Gear weight="regular" size={24} />
      <Bell weight="duotone" size={24} />
      <User weight="fill" size={24} />
    </nav>
  );
};
```

**Ícones com diferentes weights:**

```jsx
// Thin (100)
<Icon weight="thin" size={24} />

// Light (300)
<Icon weight="light" size={24} />

// Regular (400)
<Icon weight="regular" size={24} />

// Medium (500)
<Icon weight="medium" size={24} />

// Bold (700)
<Icon weight="bold" size={24} />

// Fill (filled version)
<Icon weight="fill" size={24} />

// Duotone (two-tone)
<Icon weight="duotone" size={24} />
```

**SVG direto no HTML:**

```html
<!-- Baixar SVG individual -->
<script src="https://unpkg.com/@phosphor-icons/web"></script>

<i class="ph ph-house"></i>
<i class="ph ph-gear"></i>
<i class="ph ph-bell"></i>

<!-- Com classes de tamanho -->
<i class="ph ph-house ph-lg"></i>
<i class="ph ph-house ph-xl"></i>

<!-- Com cores -->
<i class="ph ph-house" style="--primary: #6366f1;"></i>
```

**Integração com Reveal.js:**

```javascript
// Adicionar ícones nos slides
Reveal.initialize({
  // Configuração padrão
}).then(() => {
  // Personalizar navegação com ícones
  document.querySelectorAll('.slide-nav-next').forEach(el => {
    el.innerHTML = '<i class="ph ph-arrow-right"></i>';
  });
  document.querySelectorAll('.slide-nav-prev').forEach(el => {
    el.innerHTML = '<i class="ph ph-arrow-left"></i>';
  });
});
```

### 3.2 Font Awesome

**Instalação via CDN:**

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
```

**Uso básico:**

```html
<i class="fa-solid fa-house"></i>
<i class="fa-solid fa-gear"></i>
<i class="fa-brands fa-github"></i>
<i class="fa-brands fa-twitter"></i>

<!-- Tamanhos -->
<i class="fa-solid fa-house fa-xs"></i>
<i class="fa-solid fa-house fa-sm"></i>
<i class="fa-solid fa-house fa-lg"></i>
<i class="fa-solid fa-house fa-2x"></i>
<i class="fa-solid fa-house fa-5x"></i>

<!-- Animações -->
<i class="fa-solid fa-circle-notch fa-spin"></i>
<i class="fa-solid fa-heart fa-beat"></i>
<i class="fa-solid fa-bell fa-shake"></i>
```

**Font Awesome com React:**

```bash
npm install @fortawesome/react-fontawesome @fortawesome/free-solid-svg-icons @fortawesome/free-brands-svg-icons
```

```jsx
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHouse, faGear, faBell } from '@fortawesome/free-solid-svg-icons';
import { faGithub, faTwitter } from '@fortawesome/free-brands-svg-icons';

const SocialLinks = () => (
  <div className="social-links">
    <a href="#github">
      <FontAwesomeIcon icon={faGithub} size="2x" />
    </a>
    <a href="#twitter">
      <FontAwesomeIcon icon={faTwitter} size="2x" />
    </a>
  </div>
);
```

---

## 4. IMPLEMENTAÇÃO DE ANIMAÇÕES

### 4.1 GSAP (GreenSock)

**Instalação:**

```bash
npm install gsap
```

**Uso básico:**

```javascript
import gsap from 'gsap';

// Animação simples
gsap.to('.element', {
  duration: 1,
  x: 100,
  opacity: 1,
  ease: 'power2.out'
});

// Timeline para sequências
const tl = gsap.timeline();

tl.from('.title', {
  duration: 1,
  y: 50,
  opacity: 0,
  ease: 'power3.out'
})
.from('.subtitle', {
  duration: 0.8,
  y: 30,
  opacity: 0,
  ease: 'power2.out'
}, '-=0.5')
.from('.content', {
  duration: 0.6,
  x: -20,
  opacity: 0,
  stagger: 0.1
}, '-=0.3');
```

**ScrollTrigger:**

```javascript
import gsap from 'gsap';
import ScrollTrigger from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

// Animação no scroll
gsap.from('.card', {
  scrollTrigger: {
    trigger: '.card-container',
    start: 'top 80%',
    end: 'bottom 20%',
    toggleActions: 'play none none reverse'
  },
  y: 50,
  opacity: 0,
  duration: 0.6,
  stagger: 0.2
});

// Parallax effect
gsap.to('.parallax-bg', {
  scrollTrigger: {
    trigger: '.parallax-section',
    start: 'top bottom',
    end: 'bottom top',
    scrub: true
  },
  yPercent: 30
});
```

**Exemplo em Reveal.js:**

```javascript
// Animar elementos quando o slide aparecer
Reveal.on('slidechanged', event => {
  const slide = event.currentSlide;
  
  // Animar título
  gsap.fromTo(slide.querySelector('h1'), 
    { opacity: 0, y: 30 },
    { opacity: 1, y: 0, duration: 0.8, ease: 'power2.out' }
  );
  
  // Animar lista com stagger
  gsap.fromTo(slide.querySelectorAll('li'),
    { opacity: 0, x: -20 },
    { opacity: 1, x: 0, duration: 0.4, stagger: 0.1 }
  );
});
```

### 4.2 Framer Motion

**Instalação:**

```bash
npm install framer-motion
```

**Uso básico:**

```jsx
import { motion } from 'framer-motion';

const FadeIn = ({ children }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5 }}
  >
    {children}
  </motion.div>
);

// Com variants
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const itemVariants = {
  hidden: { opacity: 0, x: -20 },
  visible: { opacity: 1, x: 0 }
};

const AnimatedList = ({ items }) => (
  <motion.ul
    variants={containerVariants}
    initial="hidden"
    animate="visible"
  >
    {items.map((item, i) => (
      <motion.li key={i} variants={itemVariants}>
        {item}
      </motion.li>
    ))}
  </motion.ul>
);
```

**Animações de hover e tap:**

```jsx
const Button = ({ children }) => (
  <motion.button
    whileHover={{ scale: 1.05 }}
    whileTap={{ scale: 0.95 }}
    whileFocus={{ scale: 1.02 }}
    transition={{ type: 'spring', stiffness: 400, damping: 17 }}
  >
    {children}
  </motion.button>
);
```

**AnimatePresence para transições:**

```jsx
import { AnimatePresence, motion } from 'framer-motion';

const Slideshow = ({ currentSlide }) => (
  <AnimatePresence mode="wait">
    <motion.div
      key={currentSlide}
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -50 }}
      transition={{ duration: 0.3 }}
    >
      {currentSlide.content}
    </motion.div>
  </AnimatePresence>
);
```

---

## 5. IMPLEMENTAÇÃO DE TIPOGRAFIA

### 5.1 Google Fonts

**Instalação via HTML:**

```html
<!-- Link no head -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

**CSS personalizado:**

```css
:root {
  --font-primary: 'Inter', system-ui, -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  --font-display: 'Playfair Display', serif;
}

body {
  font-family: var(--font-primary);
}

code, pre {
  font-family: var(--font-mono);
}

h1, h2, h3 {
  font-family: var(--font-display);
}
```

**Importação via CSS (@import):**

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@400;600;700&display=swap');
```

**Google Fonts no Reveal.js:**

```javascript
Reveal.initialize({
  // ...
}).then(() => {
  // Adicionar fonts ao documento
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@400;600;700&display=swap';
  document.head.appendChild(link);
});
```

**Font Display Swap:**

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">

<style>
  body {
    font-family: 'Inter', sans-serif;
    /* Garante que o texto seja visível antes da fonte carregar */
    font-display: swap;
  }
</style>
```

### 5.2 Adobe Fonts

**Configuração:**

```html
<!-- Adicionar ao head do projeto -->
<link rel="stylesheet" href="https://use.typekit.net/[project-id].css">
```

**Projeto Typekit:**

```javascript
// Exemplo de configuração para projetos FactoryOS
const adobeFontsConfig = {
  projectId: 'factory-os-2024',
  fonts: [
    'proxima-nova',      // Interface
    'brandon-grotesque', // Títulos
    'minion-pro'         // Corpo de texto premium
  ]
};
```

**Uso em CSS:**

```css
:root {
  --font-interface: 'proxima-nova', sans-serif;
  --font-display: 'brandon-grotesque', sans-serif;
  --font-body-premium: 'minion-pro', serif;
}
```

---

## 6. IMPLEMENTAÇÃO DE ELEMENTOS 3D

### 6.1 Spline

**Instalação via NPM:**

```bash
npm install @splinetool/react-spline
```

**Uso em React:**

```jsx
import Spline from '@splinetool/react-spline';

const Scene3D = () => (
  <div className="spline-container">
    <Spline scene="https://prod.spline.design/[scene-id]/scene.splinecode" />
  </div>
);

export default Scene3D;
```

**Spline Viewer (Web Component):**

```html
<!-- Via CDN -->
<script type="module" src="https://unpkg.com/@splinetool/viewer@1.0.94/build/spline-viewer.js"></script>

<spline-viewer 
  url="https://prod.spline.design/[scene-id]/scene.splinecode"
  loading-anim-type="spinner-small-dark"
  background-color="#0f172a"
>
</spline-viewer>
```

**Configurações do viewer:**

```html
<spline-viewer
  url="https://prod.spline.design/[scene-id]/scene.splinecode"
  events-target="global"
  loading-anim-type="spinner-small-dark"
  background-color="#0f172a"
  camera-initial-position="0 0 1000"
  camera-initial-target="0 0 0"
>
</spline-viewer>
```

**Interação via JavaScript:**

```javascript
const viewer = document.querySelector('spline-viewer');

viewer.addEventListener('mouseDown', (e) => {
  console.log('Mouse clicked on:', e.target.name);
});

viewer.addEventListener('load', () => {
  console.log('Spline scene loaded');
});

// Exportar para uso em Reveal.js
viewer.addEventListener('sceneChange', (e) => {
  console.log('Scene changed to:', e.detail.name);
});
```

**Spline no Reveal.js:**

```javascript
// Adicionar após a inicialização do Reveal
Reveal.initialize({
  // Configurações padrão
}).then(() => {
  // Carregar Spline viewer
  const script = document.createElement('script');
  script.type = 'module';
  script.src = 'https://unpkg.com/@splinetool/viewer@1.0.94/build/spline-viewer.js';
  document.head.appendChild(script);
  
  // Inserir elemento 3D no slide
  document.querySelectorAll('.slide-3d').forEach(slide => {
    const viewer = document.createElement('spline-viewer');
    viewer.setAttribute('url', slide.dataset.splineUrl);
    viewer.setAttribute('loading-anim-type', 'spinner-small-dark');
    viewer.style.width = '100%';
    viewer.style.height = '500px';
    slide.appendChild(viewer);
  });
});
```

---

## 7. CONFIGURAÇÃO NO REVEAL.JS

### 7.1 Estrutura Base

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FactoryOS - Apresentação</title>
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@400;600;700&display=swap" rel="stylesheet">
  
  <!-- Phosphor Icons -->
  <link rel="stylesheet" href="https://unpkg.com/@undraw/viewer@1.0.0/dist/undraw-viewer.css">
  <script src="https://unpkg.com/@phosphor-icons/web"></script>
  
  <!-- Reveal.js CSS -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.6.1/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.6.1/dist/theme/black.css">
  
  <style>
    :root {
      --font-primary: 'Inter', sans-serif;
      --font-display: 'Playfair Display', serif;
      --color-primary: #6366f1;
      --color-secondary: #8b5cf6;
      --color-accent: #f59e0b;
      --color-bg: #0f172a;
    }
    
    .reveal {
      font-family: var(--font-primary);
    }
    
    .reveal h1, .reveal h2, .reveal h3 {
      font-family: var(--font-display);
      color: var(--color-primary);
    }
    
    .reveal .slides section {
      text-align: left;
    }
    
    /* Ícones */
    .reveal .icon {
      display: inline-block;
      vertical-align: middle;
      margin-right: 0.5rem;
    }
    
    /* Ilustrações */
    .illustration-container {
      margin: 2rem 0;
    }
    
    /* Cards */
    .card {
      background: rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      padding: 1.5rem;
      margin: 1rem 0;
    }
  </style>
</head>
<body>
  <div class="reveal">
    <div class="slides">
      <!-- Slides aqui -->
    </div>
  </div>
  
  <!-- Scripts -->
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.6.1/dist/reveal.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
  
  <script>
    // Inicialização
    Reveal.initialize({
      hash: true,
      slideNumber: true,
      transition: 'slide',
      transitionSpeed: 'default',
      backgroundTransition: 'fade',
      center: false,
      width: 1280,
      height: 720,
      margin: 0.04,
    }).then(() => {
      // GSAP animations
      gsap.from('.reveal .slides section.present h1', {
        y: 30,
        opacity: 0,
        duration: 0.8,
        ease: 'power2.out'
      });
    });
  </script>
</body>
</html>
```

### 7.2 Exemplo de Slide Completo

```html
<section data-background-color="#0f172a">
  <div class="slide-layout-split">
    <div class="slide-content">
      <h1>
        <i class="ph ph-rocket-launch icon"></i>
        FactoryOS
      </h1>
      <p class="subtitle">Plataforma de Manufatura Inteligente</p>
      
      <div class="features-grid">
        <div class="feature-card">
          <i class="ph ph-gauge icon" style="color: #6366f1;"></i>
          <h3>Performance</h3>
          <p>Otimização em tempo real</p>
        </div>
        <div class="feature-card">
          <i class="ph ph-shield-check icon" style="color: #8b5cf6;"></i>
          <h3>Segurança</h3>
          <p>Proteção avançada</p>
        </div>
        <div class="feature-card">
          <i class="ph ph-users-three icon" style="color: #f59e0b;"></i>
          <h3>Colaboração</h3>
          <p>Trabalho em equipe</p>
        </div>
      </div>
    </div>
    
    <div class="slide-illustration">
      <div class="illustration-container" data-illustration="teamwork"></div>
    </div>
  </div>
  
  <style>
    .slide-layout-split {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 3rem;
      align-items: center;
    }
    
    .subtitle {
      font-size: 1.5rem;
      color: #94a3b8;
      margin-bottom: 2rem;
    }
    
    .features-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1rem;
    }
    
    .feature-card {
      background: rgba(255, 255, 255, 0.05);
      border-radius: 12px;
      padding: 1.5rem;
      text-align: center;
      transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
      transform: translateY(-5px);
      background: rgba(255, 255, 255, 0.1);
    }
    
    .feature-card h3 {
      font-size: 1rem;
      margin: 0.5rem 0;
      color: #f1f5f9;
    }
    
    .feature-card p {
      font-size: 0.875rem;
      color: #94a3b8;
    }
    
    .feature-card i {
      font-size: 2rem;
    }
    
    .slide-illustration {
      display: flex;
      justify-content: center;
      align-items: center;
    }
    
    .illustration-container svg {
      max-width: 100%;
      height: auto;
    }
  </style>
</section>
```

### 7.3 Plugin Personalizado para Assets

```javascript
// assets-plugin.js
// Plugin Reveal.js para gerenciamento de assets visuais

import undraw from '@undraw/illustrations/pigment';
import { gsap } from 'gsap';

const AssetsPlugin = {
  id: 'assets-plugin',
  
  init: function(reveal) {
    this.reveal = reveal;
    this.assets = {};
    
    // Carregar ilustrações
    this.loadIllustrations();
    
    // Configurar animações GSAP
    this.setupAnimations();
    
    // Observer para lazy loading
    this.setupLazyLoading();
  },
  
  loadIllustrations: function() {
    const containers = document.querySelectorAll('[data-illustration]');
    containers.forEach(container => {
      const illustrationName = container.dataset.illustration;
      const color = container.dataset.color || '#6366f1';
      const secondaryColor = container.dataset.secondary || '#8b5cf6';
      
      const svg = undraw(illustrationName, color, secondaryColor);
      container.innerHTML = svg;
    });
  },
  
  setupAnimations: function() {
    this.reveal.on('slidechanged', event => {
      const slide = event.currentSlide;
      
      // Animações definidas no data attributes
      slide.querySelectorAll('[data-animate]').forEach(el => {
        const animation = el.dataset.animate;
        const duration = parseFloat(el.dataset.duration) || 0.5;
        
        gsap.fromTo(el,
          { opacity: 0, y: 20 },
          { opacity: 1, y: 0, duration, ease: 'power2.out' }
        );
      });
    });
  },
  
  setupLazyLoading: function() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          if (img.dataset.src) {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
          }
          observer.unobserve(img);
        }
      });
    }, { rootMargin: '100px' });
    
    document.querySelectorAll('[data-src]').forEach(img => {
      observer.observe(img);
    });
  }
};

export default AssetsPlugin;
```

---

## 8. CHECKLIST DE IMPLEMENTAÇÃO

### 8.1 Pré-Implementação

- [ ] **Planejamento**
  - [ ] Revisar diagnóstico visual
  - [ ] Confirmar ferramentas selecionadas
  - [ ] Definir paleta de cores corporativa
  - [ ] Estabelecer guidelines visuais

- [ ] **Preparação Técnica**
  - [ ] Criar conta nas ferramentas necessárias
  - [ ] Gerar API keys (se aplicável)
  - [ ] Configurar repositório
  - [ ] Preparar ambiente de desenvolvimento

### 8.2 Implementação Core

- [ ] **Fonts**
  - [ ] Integrar Google Fonts no projeto
  - [ ] Configurar fallback fonts
  - [ ] Testar em diferentes browsers
  - [ ] Aplicar tipografia em todos os elementos

- [ ] **Ícones**
  - [ ] Instalar Phosphor Icons
  - [ ] Configurar Font Awesome (opcional)
  - [ ] Criar mapeamento de ícones por seção
  - [ ] Padronizar tamanhos e pesos
  - [ ] Testar em modo escuro/claro

- [ ] **Ilustrações**
  - [ ] Instalar unDraw
  - [ ] Configurar Blush (opcional)
  - [ ] Criar biblioteca de ilustrações do projeto
  - [ ] Padronizar cores com paleta corporativa

### 8.3 Animações e Interatividade

- [ ] **GSAP**
  - [ ] Instalar GSAP core
  - [ ] Instalar ScrollTrigger (se necessário)
  - [ ] Criar animações de entrada
  - [ ] Configurar timelines para seções
  - [ ] Otimizar performance

- [ ] **Framer Motion** (se React)
  - [ ] Instalar Framer Motion
  - [ ] Criar componentes animados
  - [ ] Configurar variants reutilizáveis
  - [ ] Implementar transições de slide

### 8.4 Elementos 3D

- [ ] **Spline**
  - [ ] Criar conta Spline
  - [ ] Projetar scenes necessárias
  - [ ] Integrar via React ou Web Component
  - [ ] Configurar interações
  - [ ] Otimizar para web (compression)
  - [ ] Testar performance em dispositivos

### 8.5 Reveal.js

- [ ] **Integração**
  - [ ] Configurar tema base
  - [ ] Integrar fonts e ícones
  - [ ] Adicionar animações GSAP
  - [ ] Configurar transições
  - [ ] Testar em diferentes resoluções
  - [ ] Validar acessibilidade

- [ ] **Slides**
  - [ ] Criar template base
  - [ ] Desenvolver slides com elementos visuais
  - [ ] Adicionar ilustrações relevantes
  - [ ] Incluir ícones informativos
  - [ ] Aplicar animações consistentes

### 8.6 Qualidade e Testes

- [ ] **Revisão Visual**
  - [ ] Verificar consistência visual
  - [ ] Testar contraste de cores
  - [ ] Validar tipografia em todos os tamanhos
  - [ ] Checar alinhamento e espaçamento

- [ ] **Performance**
  - [ ] Medir tempo de carregamento
  - [ ] Otimizar imagens e SVGs
  - [ ] Lazy loading implementado
  - [ ] Testar em dispositivos móveis

- [ ] **Acessibilidade**
  - [ ] Verificar contraste WCAG
  - [ ] Adicionar alt texts
  - [ ] Testar navegação por teclado
  - [ ] Validar ARIA labels

### 8.7 Deploy

- [ ] **Preparação**
  - [ ] Minificar assets
  - [ ] Compilar código (se necessário)
  - [ ] Configurar CDN para assets
  - [ ] Documentar configuração

- [ ] **Validação Final**
  - [ ] Testar em produção
  - [ ] Verificar hotlinks
  - [ ] Backup de configurações
  - [ ] Documentar mudanças

### 8.8 Pós-Implementação

- [ ] **Documentação**
  - [ ] Atualizar guia de estilo
  - [ ] Criar exemplos de uso
  - [ ] Documentar componentes criados
  - [ ] Listar recursos disponíveis

- [ ] **Treinamento**
  - [ ] Apresentar novas ferramentas à equipe
  - [ ] Criar tutoriais rápidos
  - [ ] Estabelecer boas práticas
  - [ ] Definir processo de manutenção

---

## 9. RECURSOS ADICIONAIS

### Links Úteis

- **unDraw:** https://unDraw.co
- **Blush:** https://blush.design
- **Phosphor Icons:** https://phosphoricons.com
- **Font Awesome:** https://fontawesome.com
- **GSAP:** https://greensock.com/gsap/
- **Framer Motion:** https://www.framer.com/motion/
- **Google Fonts:** https://fonts.google.com
- **Adobe Fonts:** https://fonts.adobe.com
- **Spline:** https://spline.design
- **Reveal.js:** https://revealjs.com

### Suporte

Para dúvidas sobre implementação, consulte:
1. Documentação oficial das ferramentas
2. Comunidade Discord do FactoryOS
3. Equipe de design do projeto

---

**Documento criado em:** 2026-02-12  
**Versão:** 1.0  
**Próxima revisão:** 2026-03-12
