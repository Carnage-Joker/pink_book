// ==============================
// Module: Mobile Navigation
// ==============================
export const navigationModule = (() => {
    function toggleMobileNav() {
        const mobileNav = document.getElementById('mobile-nav');
        mobileNav.classList.toggle('active');
    }

    function closeMobileNavOnClick() {
        document.querySelectorAll('.mobile-nav a').forEach(link => {
            link.addEventListener('click', () => {
                const mobileNav = document.getElementById('mobile-nav');
                mobileNav.classList.remove('active');
            });
        });
    }

    function init() {
        document.getElementById('hamburger-menu').addEventListener('click', toggleMobileNav);
        closeMobileNavOnClick();
    }

    return { init };
})();