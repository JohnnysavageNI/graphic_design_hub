(function ($) {
  $(function () {
    var $modal = $('#confirmDeleteModal');
    if (!$modal.length) return;

    $modal.on('show.bs.modal', function (e) {
      var $btn = $(e.relatedTarget);
      var url = $btn.data('delete-url');
      var label = $btn.data('item-label') || 'this item';

      var $form = $modal.find('#delete-form');
      var $labelNode = $modal.find('#delete-item-label');

      if (url) $form.attr('action', url);
      $labelNode.text(label);
    });
  });
})(jQuery);