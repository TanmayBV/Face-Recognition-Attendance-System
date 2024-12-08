document.addEventListener('DOMContentLoaded', () => {
    const circles = document.querySelectorAll('.circle-progress');
  
    circles.forEach(circle => {
      const percentage = parseInt(circle.getAttribute('data-percentage'), 10);
      circle.style.setProperty('--percentage', percentage);
  
      // Add animation class
      setTimeout(() => {
        circle.classList.add('animate-progress');
      }, 200);
    });
  
    // Optional: Toggle Dark Mode
    const body = document.body;
    const themeToggle = document.querySelector('.theme-toggle');
    themeToggle?.addEventListener('click', () => {
      const currentTheme = body.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      body.setAttribute('data-theme', currentTheme);
    });
  });
  