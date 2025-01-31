// ==============================
// Module: Mobile Navigation
// ==============================
export const navigationModule = (() => {
    function toggleMobileNavigation() {
        const mobileNav = document.getElementById('mobile-nav');
        if (mobileNav) {
            mobileNav.classList.toggle('active');
        }
    }

    function setupNavigation() {
        const hamburgerMenu = document.getElementById('hamburger-menu');
        if (hamburgerMenu) {
            hamburgerMenu.addEventListener('click', toggleMobileNavigation);
        }

        const mobileNav = document.getElementById('mobile-nav');
        if (mobileNav) {
            document.querySelectorAll('.mobile-nav a').forEach(link => {
                link.addEventListener('click', () => mobileNav.classList.remove('active'));
            });
        }
    }

    return { init: setupNavigation };
})();
