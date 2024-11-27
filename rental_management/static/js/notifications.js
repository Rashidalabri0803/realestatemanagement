document.addEventListener('DOMContentLoaded', function(){
  const markAllReadBtn = document.querySelectorAll('#mark-all-read');
  if (markAllReadBtn) {
    markAllReadBtn.addEventListner('click', function () {
      fetch('/api/notifications/mark_all_read', {method: 'POST'})
        .then(response => response.json())
        .then(data => {
          alert(data.message || 'تم تحديد الإشعارات كمثروءة.');
          location.reload();
        })
        .catch(error => console.error('Error:', error));
    });
  }
});