document.addEventListener('DOMContentLoaded', function() {
  const deleteButtons = document.querySelectorAll('.btn-danger');
  deleteButtons.forEach(button => {
    button.addEventListener('click', function(event) {
      if (!confirm('هل أنت متأكد من أنك تريد حذف هذا العنصر؟')) {
        event.preventDefault();
      }
    });
  });
});