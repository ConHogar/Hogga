(() => {
    'use strict';
  
    // ===== Utilidades pequeñas =====
    const $ = (s, r = document) => r.querySelector(s);
    const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
    const prefersMotion = () =>
      !window.matchMedia || window.matchMedia('(prefers-reduced-motion: no-preference)').matches;
  
    // ===== Lazy loading defensivo =====
    function setupLazyImages() {
      $$('img:not([loading])').forEach(img => (img.loading = 'lazy'));
    }
  
    // ===== Animación del chat demo =====
    function animateChatDemo() {
      const bubbles = $$('.chat-demo .bubble');
      if (!bubbles.length || !prefersMotion()) return;
  
      bubbles.forEach((b, i) => {
        b.style.opacity = '0';
        b.style.transform = 'translateY(8px)';
        // repaint para que el transition se aplique
        // eslint-disable-next-line no-unused-expressions
        b.offsetHeight;
        setTimeout(() => {
          b.style.transition = 'opacity .5s ease, transform .5s ease';
          b.style.opacity = '1';
          b.style.transform = 'translateY(0)';
        }, 600 + i * 500);
      });
  
      // Si existe una burbuja "typing", quítala suave tras 2.6s
      const typing = $('.chat-demo .bubble.typing');
      if (typing) {
        setTimeout(() => {
          typing.style.transition = 'opacity .3s ease';
          typing.style.opacity = '0';
          setTimeout(() => typing.remove(), 320);
        }, 2600);
      }
    }
  
    // ===== Formulario: envío con fallback =====
    function setupLeadForm() {
      const form = document.forms['lead-form'];
      if (!form) return;
  
      // Configura TU endpoint real (Formspree / Worker / Supabase Edge)
      const FORM_ENDPOINT = ''; // ej: 'https://formspree.io/f/xxxxxxx'
      const WHATSAPP_FALLBACK =
        'https://wa.me/569XXXXXXXX?text=Hola%20Hogga%2C%20necesito%20un%20dato';
  
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
  
        const btn = form.querySelector('button[type="submit"]');
        const originalText = btn ? btn.textContent : '';
        if (btn) { btn.disabled = true; btn.textContent = 'Enviando…'; }
  
        // Construir payload seguro
        const data = new FormData(form);
  
        // AbortController para evitar colgarse
        const ac = new AbortController();
        const timeout = setTimeout(() => ac.abort(), 10000); // 10s
  
        try {
          if (!FORM_ENDPOINT) throw new Error('No endpoint configured');
  
          const res = await fetch(FORM_ENDPOINT, {
            method: 'POST',
            body: data,
            signal: ac.signal,
          });
  
          clearTimeout(timeout);
  
          if (!res.ok) {
            throw new Error(`Bad status: ${res.status}`);
          }
  
          // Éxito UX
          if (btn) btn.textContent = '¡Listo!';
          form.reset();
  
          // Vuelve el botón a su estado luego de un respiro
          setTimeout(() => {
            if (btn) { btn.disabled = false; btn.textContent = originalText || 'Enviar'; }
          }, 1000);
  
        } catch (err) {
          clearTimeout(timeout);
          console.error('Form submit error:', err);
  
          // Fallback amable a WhatsApp
          alert('No se pudo enviar. Te redirijo a WhatsApp para ayudarte al tiro.');
          window.open(WHATSAPP_FALLBACK, '_blank', 'noopener');
  
          if (btn) { btn.disabled = false; btn.textContent = originalText || 'Enviar'; }
        }
      });
    }
  
    // ===== Año dinámico en footer (si existe #y) =====
    function setupFooterYear() {
      const y = $('#y');
      if (y) y.textContent = new Date().getFullYear();
    }
  
    // ===== Nav activo (mejora UX, opcional) =====
    function setupActiveNav() {
      const links = $$('header nav a[href^="#"]');
      const sections = links
        .map(a => document.getElementById(a.getAttribute('href').slice(1)))
        .filter(Boolean);
  
      if (!sections.length) return;
  
      const io = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          const id = entry.target.id;
          const link = $(`header nav a[href="#${id}"]`);
          if (!link) return;
          if (entry.isIntersecting) {
            links.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            link.setAttribute('aria-current', 'page');
          }
        });
      }, { rootMargin: '-40% 0px -50% 0px', threshold: 0.01 });
  
      sections.forEach(s => io.observe(s));
    }
  
    // ===== Init =====
    document.addEventListener('DOMContentLoaded', () => {
      setupLazyImages();
      animateChatDemo();
      setupLeadForm();
      setupFooterYear();
      setupActiveNav();
    });
  })();
  