document.addEventListener('DOMContentLoaded', function () {
  const drawer = document.querySelector('.mini-cart-drawer');
  const overlay = drawer?.querySelector('.mini-cart-overlay');
  const panel = drawer?.querySelector('.mini-cart-panel') || drawer;
  const openers = document.querySelectorAll('[data-mini-cart-open]');
  const closers = drawer?.querySelectorAll('[data-mini-cart-close]');

  let lastFocusedElement = null;

  function openDrawer() {
    if (!drawer) return;
    lastFocusedElement = document.activeElement;
    drawer.classList.add('is-open');
    document.body.classList.add('body--no-scroll');
    trapFocus();
  }

  function closeDrawer() {
    if (!drawer) return;
    drawer.classList.remove('is-open');
    document.body.classList.remove('body--no-scroll');
    releaseFocus();
  }

  function trapFocus() {
    const focusable = drawer.querySelectorAll('a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])');
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    drawer.addEventListener('keydown', function (e) {
      if (e.key === 'Tab') {
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    });
    first.focus();
  }

  function releaseFocus() {
    if (lastFocusedElement) lastFocusedElement.focus();
  }

  openers.forEach(btn => btn.addEventListener('click', e => {
    e.preventDefault();
    openDrawer();
  }));

  closers?.forEach(btn => btn.addEventListener('click', closeDrawer));
  overlay?.addEventListener('click', closeDrawer);

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeDrawer();
  });
});