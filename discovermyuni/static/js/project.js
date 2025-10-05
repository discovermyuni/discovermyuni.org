/* Project specific Javascript goes here. */

// Enhanced Theme Toggle System
document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('themeToggle');
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = localStorage.getItem('theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            // Apply theme immediately
            if (newTheme === 'dark') {
                document.body.classList.add('theme-dark', 'dark');
                document.documentElement.classList.add('dark');
            } else {
                document.body.classList.remove('theme-dark', 'dark');
                document.documentElement.classList.remove('dark');
            }
            
            // Save to localStorage
            localStorage.setItem('theme', newTheme);
        });
    }
    
    // Update theme toggle icons based on current theme
    function updateThemeToggleIcons() {
        const isDark = document.body.classList.contains('dark');
        const sunIcon = document.querySelector('.theme-icon-sun');
        const moonIcon = document.querySelector('.theme-icon-moon');
        
        if (sunIcon && moonIcon) {
            if (isDark) {
                sunIcon.classList.add('hidden');
                moonIcon.classList.remove('hidden');
            } else {
                sunIcon.classList.remove('hidden');
                moonIcon.classList.add('hidden');
            }
        }
    }
    
    // Initialize icons
    updateThemeToggleIcons();
    
    // Watch for theme changes
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                updateThemeToggleIcons();
            }
        });
    });
    
    observer.observe(document.body, {
        attributes: true,
        attributeFilter: ['class']
    });
});
