
//
// INFORMATION.HTML
//

// edit username
function closeForm() {
    $('.input_username').removeClass('visible');
    }
    
    $(document).ready(function($) {
    
    // Form Interactions //
    $('#edit_username').on('click', function(event) {
      event.preventDefault();
    
      $('.input_username').addClass('visible');
    });
    
    // close popup
    $('.input_username').on('click', function(event) {
      if ($(event.target).is('.input_username') || $(event.target).is('#cancel_username_update')) {
        event.preventDefault();
        $(this).removeClass('visible');
      }
    });
    
    
    
    });
  
  // edit surname
  function closeForm() {
    $('.input_surname').removeClass('visible');
    }
    
    $(document).ready(function($) {
    
    // Form Interactions //
    $('#edit_surname').on('click', function(event) {
      event.preventDefault();
    
      $('.input_surname').addClass('visible');
    });
    
    // close popup
    $('.input_surname').on('click', function(event) {
      if ($(event.target).is('.input_surname') || $(event.target).is('#cancel_surname_update')) {
        event.preventDefault();
        $(this).removeClass('visible');
      }
    });
    
    
    
    });
  
  // edit id number
  function closeForm() {
    $('.input_id_number').removeClass('visible');
    }
    
    $(document).ready(function($) {
    
    // Form Interactions //
    $('#edit_id_number').on('click', function(event) {
      event.preventDefault();
    
      $('.input_id_number').addClass('visible');
    });
    
    // close popup
    $('.input_id_number').on('click', function(event) {
      if ($(event.target).is('.input_id_number') || $(event.target).is('#cancel_id_number_update')) {
        event.preventDefault();
        $(this).removeClass('visible');
      }
    });
    
    
    
    });
  
  // edit residential address
  function closeForm() {
    $('.input_residential_address').removeClass('visible');
    }
    
    $(document).ready(function($) {
    
    // Form Interactions //
    $('#edit_residential_address').on('click', function(event) {
      event.preventDefault();
    
      $('.input_residential_address').addClass('visible');
    });
    
    // close popup
    $('.input_residential_address').on('click', function(event) {
      if ($(event.target).is('.input_residential_address') || $(event.target).is('#cancel_residential_address_update')) {
        event.preventDefault();
        $(this).removeClass('visible');
      }
    });
    
    
    
    });
  
  // edit phone number
  function closeForm() {
    $('.input_phone_number').removeClass('visible');
    }
    
    $(document).ready(function($) {
    
    // Form Interactions //
    $('#edit_phone_number').on('click', function(event) {
      event.preventDefault();
    
      $('.input_phone_number').addClass('visible');
    });
    
    // close popup
    $('.input_phone_number').on('click', function(event) {
      if ($(event.target).is('.input_phone_number') || $(event.target).is('#cancel_phone_number_update')) {
        event.preventDefault();
        $(this).removeClass('visible');
      }
    });
    
    
    
    });
  
  // edit email address
  function closeForm() {
    $('.input_email_address').removeClass('visible');
    }
    
    $(document).ready(function($) {
    
    // Form Interactions //
    $('#edit_email_address').on('click', function(event) {
      event.preventDefault();
    
      $('.input_email_address').addClass('visible');
    });
    
    // close popup
    $('.input_email_address').on('click', function(event) {
      if ($(event.target).is('.input_email_address') || $(event.target).is('#cancel_email_address_update')) {
        event.preventDefault();
        $(this).removeClass('visible');
      }
    });
    
    
    
    });