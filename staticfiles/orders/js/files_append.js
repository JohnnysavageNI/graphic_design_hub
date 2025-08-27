(function () {
  var input = document.getElementById('id_uploaded_files');
  if (!input) return;

  var list = document.getElementById('selected-files');
  var dt = new DataTransfer();

  function renderList() {
    if (!list) return;
    list.innerHTML = '';
    Array.from(dt.files).forEach(function (f, idx) {
      var li = document.createElement('li');
      li.className = 'd-flex align-items-center mb-1';
      var name = document.createElement('span');
      name.textContent = f.name + ' (' + Math.round(f.size / 1024) + ' KB)';
      name.className = 'mr-2';

      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'btn btn-sm btn-outline-danger py-0';
      btn.textContent = 'Remove';
      btn.setAttribute('data-index', String(idx));
      btn.addEventListener('click', function () {
        var i = Number(this.getAttribute('data-index'));
        var next = new DataTransfer();
        Array.from(dt.files).forEach(function (file, j) {
          if (j !== i) next.items.add(file);
        });
        dt = next;
        input.files = dt.files;
        renderList();
      });

      li.appendChild(name);
      li.appendChild(btn);
      list.appendChild(li);
    });

    if (dt.files.length === 0) {
      var li = document.createElement('li');
      li.textContent = 'No files selected yet.';
      list.appendChild(li);
    }
  }

  input.addEventListener('change', function () {
    for (const f of input.files) {
      var exists = Array.from(dt.files).some(function (x) {
        return x.name === f.name && x.size === f.size && x.lastModified === f.lastModified;
      });
      if (!exists) dt.items.add(f);
    }
    input.files = dt.files;
    renderList();
  });

  renderList();
})();
