function closeForm() {
  $('.information-container').removeClass('visible');
}

$(document).ready(function($) {
  
  /* Contact Form Interactions */
  $('#open-pending-activation').on('click', function(event) {
    event.preventDefault();

    $('.information-container').addClass('visible');
  });
  
    //close popup when clicking x or off popup
  $('.information-container').on('click', function(event) {
    if ($(event.target).is('.information-container') || $(event.target).is('#clear')) {
      event.preventDefault();
      $(this).removeClass('visible');
    }
  });
  
  
  
  });
