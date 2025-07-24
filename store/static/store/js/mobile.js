// Mobile-specific optimizations and enhancements

document.addEventListener('DOMContentLoaded', function() {
    // Detect if user is on mobile device
    const isMobile = window.innerWidth <= 768;
    const isTouch = 'ontouchstart' in window;

    // Mobile-specific optimizations
    if (isMobile) {
        // Reduce animation durations for better performance
        const floatingElements = document.querySelectorAll('.animate-float');
        floatingElements.forEach(el => {
            el.style.animationDuration = '8s';
        });

        // Optimize scroll behavior
        document.documentElement.style.scrollBehavior = 'smooth';
        
        // Add mobile-specific classes
        document.body.classList.add('mobile-device');
    }

    // Touch feedback for interactive elements
    if (isTouch) {
        const touchElements = document.querySelectorAll('.touch-manipulation');
        
        touchElements.forEach(element => {
            element.addEventListener('touchstart', function(e) {
                this.style.transform = 'scale(0.95)';
                this.style.transition = 'transform 0.1s ease';
                
                // Add visual feedback
                this.classList.add('touching');
            }, { passive: true });
            
            element.addEventListener('touchend', function(e) {
                setTimeout(() => {
                    this.style.transform = '';
                    this.style.transition = '';
                    this.classList.remove('touching');
                }, 100);
            }, { passive: true });

            element.addEventListener('touchcancel', function(e) {
                this.style.transform = '';
                this.style.transition = '';
                this.classList.remove('touching');
            }, { passive: true });
        });
    }

    // Enhanced mobile navigation
    const mobileMenuButton = document.querySelector('[\\@click*="mobileOpen"]');
    if (mobileMenuButton) {
        mobileMenuButton.addEventListener('click', function() {
            // Haptic feedback for supported devices
            if (navigator.vibrate) {
                navigator.vibrate(50);
            }
            
            // Prevent body scroll when menu is open
            const body = document.body;
            const isMenuOpen = this.getAttribute('aria-expanded') === 'true';
            
            if (!isMenuOpen) {
                body.style.overflow = 'hidden';
            } else {
                body.style.overflow = '';
            }
        });
    }

    // Optimize carousel for mobile
    const carousel = document.getElementById('carousel-images');
    if (carousel && isMobile) {
        let startX = 0;
        let currentX = 0;
        let isDragging = false;

        carousel.addEventListener('touchstart', function(e) {
            startX = e.touches[0].clientX;
            isDragging = true;
        }, { passive: true });

        carousel.addEventListener('touchmove', function(e) {
            if (!isDragging) return;
            currentX = e.touches[0].clientX;
            const diffX = startX - currentX;
            
            // Add resistance effect
            if (Math.abs(diffX) > 10) {
                this.style.transform = `translateX(-${diffX * 0.3}px)`;
            }
        }, { passive: true });

        carousel.addEventListener('touchend', function(e) {
            if (!isDragging) return;
            isDragging = false;
            
            const diffX = startX - currentX;
            this.style.transform = '';
            
            // Trigger navigation based on swipe direction
            if (Math.abs(diffX) > 50) {
                if (diffX > 0) {
                    // Swipe left - next image
                    const nextBtn = document.getElementById('next');
                    if (nextBtn) nextBtn.click();
                } else {
                    // Swipe right - previous image
                    const prevBtn = document.getElementById('prev');
                    if (prevBtn) prevBtn.click();
                }
            }
        }, { passive: true });
    }

    // Lazy loading optimization for mobile
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        observer.unobserve(img);
                    }
                }
            });
        }, {
            rootMargin: '50px 0px',
            threshold: 0.1
        });

        // Observe all images with data-src attribute
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Optimize form inputs for mobile
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        // Prevent zoom on focus for iOS
        input.addEventListener('touchstart', function() {
            if (window.innerWidth < 768) {
                const viewport = document.querySelector('meta[name=viewport]');
                if (viewport) {
                    viewport.setAttribute('content', 
                        'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
                }
            }
        });

        input.addEventListener('blur', function() {
            if (window.innerWidth < 768) {
                const viewport = document.querySelector('meta[name=viewport]');
                if (viewport) {
                    viewport.setAttribute('content', 
                        'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes');
                }
            }
        });
    });

    // Performance monitoring for mobile
    if (isMobile && 'performance' in window) {
        window.addEventListener('load', () => {
            const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
            
            // Log slow loading times
            if (loadTime > 3000) {
                console.warn('Slow page load detected:', loadTime + 'ms');
            }
        });
    }

    // Handle orientation changes
    window.addEventListener('orientationchange', function() {
        // Refresh viewport calculations
        setTimeout(() => {
            window.dispatchEvent(new Event('resize'));
        }, 100);
    });

    // Add CSS classes based on device capabilities
    if (isTouch) {
        document.body.classList.add('touch-device');
    }

    if (window.DeviceMotionEvent) {
        document.body.classList.add('motion-device');
    }

    // Progressive Web App features
    if ('serviceWorker' in navigator && isMobile) {
        // Register service worker for offline functionality
        // navigator.serviceWorker.register('/sw.js');
    }
});

// Export functions for use in other scripts
window.MobileOptimizations = {
    isMobile: () => window.innerWidth <= 768,
    isTouch: () => 'ontouchstart' in window,
    
    // Utility function to add touch feedback to any element
    addTouchFeedback: (element) => {
        if (!element || !('ontouchstart' in window)) return;
        
        element.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.95)';
            this.style.transition = 'transform 0.1s ease';
        }, { passive: true });
        
        element.addEventListener('touchend', function() {
            setTimeout(() => {
                this.style.transform = '';
                this.style.transition = '';
            }, 100);
        }, { passive: true });
    }
};
