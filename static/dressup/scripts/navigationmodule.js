// navigationModule.js

export const navigationModule = (() => {
    // We define a function to do all the DOM lookups and event bindings.
    function setupNavigation() {
        const mobileNav = document.getElementById('mobile-nav');
        const hamburgerMenu = document.getElementById('hamburger-menu');

        function toggleMobileNavigation() {
            if (mobileNav) {
                mobileNav.classList.toggle('active');
            }
        }

        // If hamburgerMenu exists, attach the toggle function
        if (hamburgerMenu) {
            hamburgerMenu.addEventListener('click', toggleMobileNavigation);
        }

        // If mobileNav exists, each link closes the nav on click
        if (mobileNav) {
            document.querySelectorAll('.mobile-nav a').forEach(link => {
                link.addEventListener('click', () => mobileNav.classList.remove('active'));
            });
        }
    }

    // Return an object with an init method that calls setupNavigation
    return {
        init: setupNavigation
    };
})();
