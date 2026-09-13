(() => {
  'use strict';

  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hasFinePointer = window.matchMedia('(pointer: fine)').matches;

  /* ─────────────────────────────────────────────
     1. PARALLAX SUTIL DOS ORBS
     Move os círculos de fundo com o mouse, em
     profundidades diferentes. Suave, discreto.
  ───────────────────────────────────────────── */
  function initParallax() {
    const orbs = document.querySelectorAll('.orb');
    if (!orbs.length || prefersReduced || !hasFinePointer) return;

    const DEPTH = [8, 12, 6]; // px máximos de deslocamento por orb
    let rafId = null;

    function apply(x, y) {
      orbs.forEach((orb, i) => {
        const d = DEPTH[i] ?? 8;
        orb.style.setProperty('--ox', `${x * d}px`);
        orb.style.setProperty('--oy', `${y * d}px`);
      });
    }

    window.addEventListener('mousemove', (e) => {
      if (rafId) return;
      rafId = requestAnimationFrame(() => {
        const x = (e.clientX / window.innerWidth  - 0.5) * 2;
        const y = (e.clientY / window.innerHeight - 0.5) * 2;
        apply(x, y);
        rafId = null;
      });
    }, { passive: true });

    document.addEventListener('mouseleave', () => apply(0, 0));
  }

  /* ─────────────────────────────────────────────
     2. TOGGLE DE SENHA
  ───────────────────────────────────────────── */
  function initPasswordToggle() {
    const wrap = document.querySelector('[data-password-wrap]');
    if (!wrap) return;

    const input = wrap.querySelector('input[type="password"], input[type="text"]');
    if (!input) return;

    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'pwd-toggle';
    btn.setAttribute('aria-label', 'Mostrar senha');
    btn.setAttribute('tabindex', '-1');

    const EYE_OPEN = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></svg>`;
    const EYE_OFF  = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 10 8 10 8a17.5 17.5 0 0 1-2.16 3.19"/><path d="M6.61 6.61A17.5 17.5 0 0 0 2 12s3.5 8 10 8a9 9 0 0 0 5.39-1.61"/><path d="M14.12 14.12a3 3 0 1 1-4.24-4.24"/><path d="M2 2l20 20"/></svg>`;

    btn.innerHTML = EYE_OPEN;
    wrap.appendChild(btn);

    btn.addEventListener('click', () => {
      const showing = input.type === 'text';
      input.type = showing ? 'password' : 'text';
      btn.classList.toggle('is-active', !showing);
      btn.setAttribute('aria-label', showing ? 'Mostrar senha' : 'Ocultar senha');
      btn.innerHTML = showing ? EYE_OPEN : EYE_OFF;
      input.focus({ preventScroll: true });
    });
  }

   function initValidation() {
    const form = document.getElementById('login-form');
    if (!form) return;

    const fields = form.querySelectorAll('[data-validate="required"]');

    function check(el, showError = false) {
      const empty = !el.value.trim();
      el.classList.toggle('is-invalid', empty && showError);
      return !empty;
    }

    fields.forEach((el) => {
      el.addEventListener('input', () => check(el, false));
      el.addEventListener('blur',  () => check(el, el.value.length > 0));
    });

    form.addEventListener('submit', (e) => {
      let ok = true;
      fields.forEach((el) => {
        const valid = check(el, true);
        if (!valid) {
          el.classList.add('shake');
          el.addEventListener('animationend', () => el.classList.remove('shake'), { once: true });
          if (ok) el.focus({ preventScroll: true });
          ok = false;
        }
      });

      if (!ok) {
        e.preventDefault();
        return;
      }

      const btn = form.querySelector('.btn-submit');
      if (btn) {
        btn.classList.add('is-loading');
        btn.disabled = true;
        setTimeout(() => {
          btn.classList.remove('is-loading');
          btn.disabled = false;
        }, 8000);
      }
    });
  }
  /* ─────────────────────────────────────────────
     5. BOTÃO DE SUBMIT (label + spinner)
  ───────────────────────────────────────────── */
  function initSubmitButton() {
    const btn = document.querySelector('.btn-submit');
    if (!btn) return;

    const label = btn.dataset.label || btn.value || 'Entrar';
    btn.value = label;
    btn.innerHTML = `
      <span class="btn-label">${label}</span>
      <span class="btn-spinner"><span class="spinner-ring"></span></span>
    `;
  }

  /* ─────────────────────────────────────────────
     BOOT
  ───────────────────────────────────────────── */
  function boot() {
    initParallax();
    initPasswordToggle();
    initSubmitButton();
    initValidation();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();