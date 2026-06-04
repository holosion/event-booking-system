document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('navToggle');
  const links = document.getElementById('navLinks');
  const navbar = document.getElementById('navbar');

  if (toggle && links) {
    toggle.addEventListener('click', () => {
      links.classList.toggle('is-open');
    });
  }

  window.addEventListener('scroll', () => {
    if (!navbar) return;
    navbar.style.boxShadow = window.scrollY > 20
      ? '0 4px 30px rgba(0,0,0,0.3)'
      : 'none';
  });

  document.querySelectorAll('[data-auto-dismiss]').forEach((el) => {
    setTimeout(() => {
      el.style.opacity = '0';
      el.style.transition = 'opacity 0.4s';
      setTimeout(() => el.remove(), 400);
    }, 5000);
  });

  document.querySelectorAll('input, select, textarea').forEach((input) => {
    if (!input.classList.length && input.type !== 'hidden' && input.type !== 'checkbox') {
      input.classList.add('styled-input');
    }
  });
});
