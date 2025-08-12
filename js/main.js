(() => {
    // Espera al DOM listo
    document.addEventListener('DOMContentLoaded', () => {
      // 1) Lazy loading para imágenes que ya tengan el atributo
      document.querySelectorAll('img[loading="lazy"]').forEach(img => {
        img.loading = 'lazy';
      });
  
      // 2) Form handler (reemplaza con tu endpoint real si corresponde)
      const form = document.forms['lead-form'];
      if (form) {
        form.addEventListener('submit', async (e) => {
          e.preventDefault();
          const btn = form.querySelector('button[type="submit"]');
          if (btn) { btn.disabled = true; btn.textContent = 'Enviando…'; }
          try {
            // TODO: reemplazar con tu endpoint (Formspree / Supabase Edge / Worker)
            // await fetch('https://tu-endpoint', { method:'POST', body: new FormData(form) });
  
            await new Promise(r => setTimeout(r, 700)); // mock
            if (btn) btn.textContent = '¡Listo!';
            form.reset();
          } catch (err) {
            if (btn) { btn.disabled = false; btn.textContent = 'Enviar'; }
            alert('No se pudo enviar. Intenta por WhatsApp.');
            console.error(err);
          }
        });
      }
  
      // En main.js, cambia el timing:
        const bubbles = document.querySelectorAll('.chat-demo .bubble');
        const motionOK = !window.matchMedia || window.matchMedia('(prefers-reduced-motion: no-preference)').matches;
        if (bubbles.length && motionOK) {
        bubbles.forEach((b, i) => {
            b.style.opacity = 0;
            b.style.transform = 'translateY(8px)';
            setTimeout(() => {
            b.style.transition = 'opacity .5s ease, transform .5s ease';
            b.style.opacity = 1;
            b.style.transform = 'translateY(0)';
            }, 600 + i * 500); // antes 250 + i*220 → ahora más lento
        });
        }
    });
  })();
  