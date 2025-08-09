(function ($) {
  function wireToasts(root) {
    $(root).find('.toast').toast({
      autohide: true,
      delay: 3500
    }).toast('show').on('hidden.bs.toast', function () {
      // remove toast DOM when done to prevent stacking
      const $t = $(this);
      const $container = $t.closest('.toast-container, .position-fixed, #toast-root');
      $t.remove();
      if ($container && !$container.find('.toast').length && $container.attr('id') !== 'toast-root') {
        $container.remove();
      }
    });
  }

  $(function () {
    wireToasts(document);

    // Optional helper if you use AJAX to return `toast_html`
    window.showToastHtml = function (html) {
      const mount = document.getElementById('toast-root') || (function () {
        const d = document.createElement('div');
        d.id = 'toast-root';
        d.setAttribute('aria-live', 'polite');
        d.setAttribute('aria-atomic', 'true');
        d.style.position = 'fixed';
        d.style.top = '80px';
        d.style.right = '20px';
        d.style.zIndex = 2000;
        document.body.appendChild(d);
        return d;
      })();
      const wrapper = document.createElement('div');
      wrapper.innerHTML = html;
      mount.appendChild(wrapper);
      wireToasts(wrapper);
    };
  });
})(jQuery);