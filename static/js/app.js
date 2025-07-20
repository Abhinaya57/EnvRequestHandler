// XR News Aggregator - Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });

    // Add loading state to action buttons
    const actionButtons = document.querySelectorAll('a[href*="refresh"], a[href*="send_email"], a[href*="test_email"]');
    actionButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const originalText = this.innerHTML;
            this.innerHTML = '<i data-feather="loader" class="me-1"></i>Processing...';
            feather.replace();
            
            // Re-enable button if user navigates back
            setTimeout(() => {
                this.innerHTML = originalText;
                feather.replace();
            }, 10000);
        });
    });

    // Enhance article cards with hover effects
    const articleCards = document.querySelectorAll('.card');
    articleCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.transition = 'transform 0.2s ease-in-out';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Real-time clock for schedule display
    function updateClock() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', {
            hour12: true,
            hour: '2-digit',
            minute: '2-digit'
        });
        
        const clockElements = document.querySelectorAll('.current-time');
        clockElements.forEach(element => {
            element.textContent = timeString;
        });
    }

    // Update clock every second
    setInterval(updateClock, 1000);
    updateClock(); // Initial call

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl+R or Cmd+R for refresh (prevent default and use our refresh)
        if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
            e.preventDefault();
            window.location.href = '/refresh_news';
        }
        
        // Ctrl+E or Cmd+E for email
        if ((e.ctrlKey || e.metaKey) && e.key === 'e') {
            e.preventDefault();
            window.location.href = '/send_email';
        }
    });

    // Add smooth scrolling to anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Form validation for keywords
    const keywordsForm = document.querySelector('form[action*="update_keywords"]');
    if (keywordsForm) {
        keywordsForm.addEventListener('submit', function(e) {
            const keywordsTextarea = this.querySelector('textarea[name="keywords"]');
            const keywords = keywordsTextarea.value.trim();
            
            if (!keywords) {
                e.preventDefault();
                alert('Keywords cannot be empty!');
                keywordsTextarea.focus();
                return false;
            }
            
            // Add loading state to submit button
            const submitBtn = this.querySelector('button[type="submit"]');
            submitBtn.innerHTML = '<i data-feather="loader" class="me-1"></i>Updating...';
            submitBtn.disabled = true;
            feather.replace();
        });
    }

    // Lazy loading for article images
    const articleImages = document.querySelectorAll('.card-img-top');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    observer.unobserve(img);
                }
            });
        });

        articleImages.forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Service worker registration for offline support (optional)
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/sw.js')
            .then(registration => {
                console.log('Service Worker registered successfully');
            })
            .catch(error => {
                console.log('Service Worker registration failed');
            });
    }
});

// Utility functions
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    const toast = createToast(message, type);
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast element after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1050';
    document.body.appendChild(container);
    return container;
}

function createToast(message, type) {
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i data-feather="${getIconForType(type)}" class="me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    return toast;
}

function getIconForType(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'x-circle',
        'warning': 'alert-triangle',
        'info': 'info',
        'primary': 'star'
    };
    return icons[type] || 'info';
}

// API helper functions
async function fetchArticles() {
    try {
        const response = await fetch('/api/articles');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching articles:', error);
        return { success: false, error: error.message };
    }
}

// Export functions for use in templates
window.NewsApp = {
    showToast,
    fetchArticles
};
