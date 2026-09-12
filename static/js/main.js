document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                // Mobile behavior: toggle 'open' class
                sidebar.classList.toggle('open');
            } else {
                // Desktop behavior: toggle 'collapsed' class
                sidebar.classList.toggle('collapsed');
            }
        });
    }

    // Add animation delay to stat cards and list items
    const elementsToStagger = document.querySelectorAll('.stat-card, .dashboard-item, .card');
    elementsToStagger.forEach((el, index) => {
        el.classList.add('animate-fade-in');
        // Add stagger class based on index (1-4 max)
        const staggerIndex = (index % 4) + 1;
        el.classList.add(`stagger-${staggerIndex}`);
    });
});
