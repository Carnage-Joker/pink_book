                                                // ==============================
                                                // Module: Mobile Navigation
                                                // ==============================
                                                export const navigationModule = () => {
                                                    const mobileNav = document.getElementById('mobile-nav');

                                                    function toggleMobileNavigation() {
                                                        if (mobileNav) {
                                                            mobileNav.classList.toggle('active');
                                                        }
                                                    }

                                                    const hamburgerMenu = document.getElementById('hamburger-menu');

                                                    if (hamburgerMenu) {
                                                        hamburgerMenu.addEventListener('click', toggleMobileNavigation);
                                                    }

                                                    if (mobileNav) {
                                                        document.querySelectorAll('.mobile-nav a').forEach(link => {
                                                            link.addEventListener('click', () => mobileNav.classList.remove('active'));
                                                        });
                                                    }

                                                    return { init: setupNavigation };
                                                };
                                                })();
