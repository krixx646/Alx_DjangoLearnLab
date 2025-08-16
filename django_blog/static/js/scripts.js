// Basic example script to demonstrate dynamic behavior
document.addEventListener('DOMContentLoaded', function() {
    console.log('Blog page loaded');
  // Add smooth scrolling for anchor links
  $('a[href^="#"]').on('click', function(event) {
    if (this.hash !== '') {
      event.preventDefault();
      const hash = this.hash;
      $('html, body').animate({
        scrollTop: $(hash).offset().top
      }, 800, function() {
        window.location.hash = hash;
      });
    }
  });

  // Add animation to messages
  $('.message').fadeIn(500).delay(3000).fadeOut(500);

  // Add hover effect to navigation items
  $('header nav ul li a').hover(
    function() { $(this).addClass('hover-effect'); },
    function() { $(this).removeClass('hover-effect'); }
  );

  // Add responsive menu toggle for mobile
  $('.menu-toggle').on('click', function() {
    $('header nav ul').toggleClass('active');
  });
});