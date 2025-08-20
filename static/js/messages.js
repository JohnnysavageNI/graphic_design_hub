(function () {
  function levelToClass(level){
    if (!level) return 'info';
    if (level.includes('success')) return 'success';
    if (level.includes('warning')) return 'warning';
    if (level.includes('error') || level.includes('danger')) return 'danger';
    return 'info';
  }

  function showPopup(text, level){
    var root = document.getElementById('auth-toast-root');
    if(!root) return;

    var box = document.createElement('div');
    box.className = 'auth-popup ' + levelToClass(level);
    box.setAttribute('role','alert');
    box.innerHTML = '<span>'+ text +'</span><button class="close-btn" aria-label="Close">&times;</button>';
    root.appendChild(box);

    requestAnimationFrame(function(){ box.classList.add('show'); });

    box.querySelector('.close-btn').addEventListener('click', function(){
      hideAndRemove(box);
    });
    setTimeout(function(){ hideAndRemove(box); }, 4000);
  }

  function hideAndRemove(el){
    el.classList.remove('show');
    el.addEventListener('transitionend', function(){
      el.parentNode && el.parentNode.removeChild(el);
    }, { once: true });
  }

  document.addEventListener('DOMContentLoaded', function(){
    var data = document.getElementById('auth-messages-data');
    if(!data) return;
    data.querySelectorAll('.auth-msg').forEach(function(n){
      var level = n.getAttribute('data-level') || 'info';
      var text  = n.textContent.trim();
      if(text){ showPopup(text, level); }
    });
  });
})();