document.addEventListener('DOMContentLoaded', function(){
  const resolveButtons = document.querySelectorAll('.resolve-maintenance');
  resolveButtons.forEach(button => {
    button.addEventListener('click', function () {
      const requestId = this.dataset.requestId;
      fetch('/api/maintenance/${requestId}/resolve/', {method: 'POST'})
        .then(response => response.json())
        .then(data => {
          alert(data.message || 'تمت معالجة طلب الصيانة.');
          location.reload();
        })
        .catch(error => console.error('Error:', error));
    });
  });
});