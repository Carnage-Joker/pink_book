// ==============================
// Module: Mobile Navigation
// ==============================
export const navigationModule = () => {
    function toggleMobileNavigation() {
        const mobileNav = document.getElementById('mobile-nav');
        mobileNav.classList.toggle('active');
    }

    function closeMobileNavigationOnClick() {
        document.querySelectorAll('.mobile-nav a').forEach(link => {
            link.addEventListener('click', () => {
                const mobileNav = document.getElementById('mobile-nav');
                mobileNav.classList.remove('active');
            });
        });
    }

    function setupHamburgerMenu() {
        const hamburgerMenu = document.getElementById('hamburger-menu');
        if (hamburgerMenu) {
            hamburgerMenu.addEventListener('click', toggleMobileNavigation);
        } else {
            console.warn('Hamburger menu not found.');
        }
    }
            console.warn('Warning: Navigation elements not found.');
    function setupMobileNav() {
        const mobileNav = document.getElementById('mobile-nav');
        if (mobileNav) {
            closeMobileNavigationOnClick();
        } else {
            console.warn('Mobile navigation not found.');
        }
    }

    function init() {
        setupHamburgerMenu();
        setupMobileNav();
    }

    return { init: init };
})();
