//
// NAVIGATION BAR
//

// dashboard function
function dashboard() {
  document.getElementById('dashboard').innerHTML = '<button class="exit_dashboard" onclick="exit_dashboard(document.getElementById(\'dashboard\'))">X</button> <ul> <li><a href="/dashboard/">User Dashboard</a></li> <li><a href="/user_information/">Information</a></li> <li><a href="/services/">Services</a></li> <li><a href="/real_estate/">Real estate</a></li> <li><a href="/notifications/">notification</a></li> <li> <a href="/logout/" >logout</a> </ul></ul> '
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