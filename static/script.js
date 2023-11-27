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

// dashboard function
function dashboard() {
    document.getElementById('dashboard').innerHTML = '<button class="exit_dashboard" onclick="exit_dashboard(document.getElementById(\'dashboard\'))">X</button> <ul><li>User Profile</li><li>Update Information</li><li>Notifications</li></ul>'
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
  
