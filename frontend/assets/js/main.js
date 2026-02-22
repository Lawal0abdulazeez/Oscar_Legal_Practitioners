/**
 * Oscar Legal Practitioners - Core JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            // In a real app, this would show/hide a mobile menu
            console.log('Mobile menu toggled');
            alert('Mobile menu functionality would open here in the full version.');
        });
    }

    // Intersection Observer for Reveal Animations
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal-active');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Apply reveal classes to elements
    const revealElements = document.querySelectorAll('.feature-card, .service-list li, .hero-content, .hero-image');
    revealElements.forEach(el => {
        el.classList.add('reveal');
        observer.observe(el);
    });

    // Handle smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Check Auth State (Mock)
    const checkAuthStatus = () => {
        const token = localStorage.getItem('access_token');
        if (token) {
            // Update UI for logged in state
            const authButtons = document.querySelectorAll('.nav-links a.btn');
            authButtons.forEach(btn => btn.style.display = 'none');
            
            const dashboardBtn = document.createElement('a');
            dashboardBtn.href = 'dashboard.html';
            dashboardBtn.className = 'btn btn-primary';
            dashboardBtn.textContent = 'Go to Dashboard';
            document.querySelector('.nav-links').appendChild(dashboardBtn);
        }
    };

    checkAuthStatus();
});

// Add these reveal styles via JS for progressive enhancement
const style = document.createElement('style');
style.textContent = `
    .reveal {
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .reveal-active {
        opacity: 1;
        transform: translateY(0);
    }
    .hero-image.reveal {
        transform: scale(0.9);
    }
    .hero-image.reveal-active {
        transform: scale(1);
    }
`;
document.head.appendChild(style);
