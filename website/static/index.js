$(document).ready(function () {
    function hideMessages() {
      $('.mensagem-alerta .alert').addClass('hide-message');
    } 
    showMessages(); 
    setTimeout(hideMessages, 3000);
  });
  function showMessages() {
    $('.mensagem-alerta .alert').removeClass('hide-message');
  }