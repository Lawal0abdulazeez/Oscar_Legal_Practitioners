/**
 * Common Logic for Oscar Legal Practitioners Dashboard
 */

document.addEventListener('DOMContentLoaded', () => {
    // Check Authentication
    const token = localStorage.getItem('access_token');
    const path = window.location.pathname;

    // Pages that require authentication
    const authPages = [
        'dashboard.html',
        'clients.html',
        'cases.html',
        'research.html',
        'drafting.html',
        'analysis.html',
        'settings.html'
    ];

    const isAuthPage = authPages.some(page => path.includes(page));

    if (isAuthPage && !token) {
        window.location.href = 'signin.html';
        return;
    }

    // Logout Handler
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.clear();
            window.location.href = 'signin.html';
        });
    }

    // Sidebar Active State
    const sidebarLinks = document.querySelectorAll('.sidebar-nav a');
    sidebarLinks.forEach(link => {
        if (path.includes(link.getAttribute('href'))) {
            link.parentElement.classList.add('active');
        } else {
            link.parentElement.classList.remove('active');
        }
    });
});
