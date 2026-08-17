//
// NAVIGATION BAR
//

// dashboard function
function dashboard() {
  document.getElementById('dashboard').innerHTML =
   `<ul>
      <li>
        <form action="/enable_dashboard_filter/" method="POST">
            <div class="catagory-placeholder">
                <input hidden="text" value='information' name="catagory">
            </div>
            <input type="submit" value="Dashboard">
        </form>
      </li> 
      <li>
        <a href="/services/">
          Services
        </a>
      </li>
      <li>
        <a href="/real_estate/">
          Real estate
        </a>
      </li>
      <li>
        <a href="/notifications/">
          notification
        </a>
      </li>
      <li>
        <a href="/logout/" >
          logout
        </a> 
      </li>
    </ul>
      <button class="exit_dashboard" onclick="exit_dashboard(document.getElementById(\'dashboard\'))">
        X
      </button>`
}

//exit dashboard function
function exit_dashboard() {
    document.getElementById('dashboard').innerHTML = ''
}

// document content function
function placeholder() {
    document.getElementById('document_content').innerHTML = '<div class="document_content"><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.Mauris pharetra et ultrices neque ornare aenean. Iaculis nunc sed augue lacus viverra vitae congue eu consequat. Sed vulputate odio ut enim blandit volutpat maecenas volutpat. Rhoncus aenean vel elit scelerisque mauris pellentesque pulvinar.Sem nulla pharetra diam sit. Mauris pellentesque pulvinar pellentesque habitant.Congue nisi vitae suscipit tellus. Sit amet venenatis urna cursus eget nunc scelerisque viverra mauris. Sit amet nisl purus in mollis nunc sed. Bibendum ut tristique et egestas quis ipsum. Tortor id aliquet lectus proin. Enim nec dui nunc mattis enim. Sed vulputate mi sit amet mauris commodo. Tristique sollicitudin nibh sit amet commodo nulla. Fringilla est ullamcorper eget nulla facilisi etiam dignissim diam quis. Pharetra sit amet aliquam id diam maecenas ultricies mi.</p></div>'
}

// login popup function
function closeForm() {
  $('.login').removeClass('visible');
}

$(document).ready(function($) {
  
  // Form Interactions //
  $('#user_access_button').on('click', function(event) {
    event.preventDefault();

    $('.login').addClass('visible');
  });

  // close popup
  $('.login').on('click', function(event) {
    if ($(event.target).is('.login') || $(event.target).is('#close_login_popup')) {
      event.preventDefault();
      $(this).removeClass('visible');
    }
  });



});

// registration popup function
function closeForm() {
$('.register').removeClass('visible');
}

$(document).ready(function($) {

// Form Interactions //
$('#user_registration_button').on('click', function(event) {
  event.preventDefault();

  $('.register').addClass('visible');
});

// close popup
$('.register').on('click', function(event) {
  if ($(event.target).is('.register') || $(event.target).is('#close_registration_popup')) {
    event.preventDefault();
    $(this).removeClass('visible');
  }
});



});

// INDEX.HTML
// scroll function
window.smoothScroll = function(target) {
    var scrollContainer = target;
    do {
        scrollContainer = scrollContainer.parentNode;
        if (!scrollContainer) return;
        scrollContainer.scrollTop += 1;
    } while (scrollContainer.scrollTop == 0);

    var targetY = 0;
    do {
        if (target == scrollContainer) break;
        targetY += target.offsetTop;
    } while (target = target.offsetParent);

    scroll = function(c, a, b, i) {
        i++; if (i > 30) return;
        c.scrollTop = a + (b - a) / 30 * i;
        setTimeout(function(){ scroll(c, a, b, i); }, 20);
    }
    
    scroll(scrollContainer, scrollContainer.scrollTop, targetY, 0);
}

// app.html catagory functions
// catagoryOne ()
function catagoryOne() {
    document.getElementById('productContainer').innerHTML = `
    {% for catagoryOne in catagory %}
    <h1>
        {{ catagoryOne }}
    </h1>
    {% endfor %}
    `
}

// INFORMATION.HTML
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
    
    //dashbord
    //upload form
    function toggleUploadForm() {
    document.getElementById('information-container').innerHTML =
    `
    <div class="listing_form">
        <form action="/list_item/" method="POST" enctype="multipart/form-data">
            <input type="text" placeholder="name of item" name="item_name" required>
            <input type="text" placeholder="model description" name="model_description" required>
            <input type="number" placeholder="price per 24hrs" name="price" required>
            <input type="file" placeholder="upload item image" name="item_img" required>
            <input type="hidden" value='pending' name="catagory">
            <input type="submit" value="upload">
        </form>
    </div>
    
    `
}