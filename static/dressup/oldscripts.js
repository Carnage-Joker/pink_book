// static/dressup/scripts.js

// Function to change clothing items
function changeItem(type, direction) {
    // Logic to change the clothing item based on type and direction
    // This could involve cycling through available items
    
    console.log(`Changing ${type} to ${direction}`);
    // Implement the actual logic to update the item
}


avatarContainer.addEventListener('dragover', (e) => {
    e.preventDefault();
    avatarContainer.classList.add('dragover');
});

avatarContainer.addEventListener('dragleave', () => {
    avatarContainer.classList.remove('dragover');
});

avatarContainer.addEventListener('drop', (e) => {
    e.preventDefault();
    avatarContainer.classList.remove('dragover');
    // Existing drop logic...
});
function setupDragAndDrop() {
    // Logic to initialize drag and drop functionality
    const items = document.querySelectorAll('.item');
    items.forEach(item => {
        item.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('text/plain', item.id);
        });
    });
}
// Drag and Drop for Dress-up Game
document.addEventListener('DOMContentLoaded', function () {
    setupDragAndDrop();
    setupNavigationToggle();
    setupPurchaseButtons();
    setupTogglePremium();
    setupToastNotifications();
});

        item.addEventListener('dragstart', function (event) {
            event.dataTransfer.setData('text/plain', event.target.id);
            event.dataTransfer.effectAllowed = 'move';
        });

    // Avatar areas where clothing can be dropped
    const dropAreas = document.querySelectorAll('#avatar-canvas img');
    dropAreas.forEach(area => {
        area.addEventListener('dragover', function (event) {
            event.preventDefault();
            event.dataTransfer.dropEffect = 'move';
        });

        area.addEventListener('drop', function (event) {
            event.preventDefault();
            const itemId = event.dataTransfer.getData('text/plain');
            const item = document.getElementById(itemId);

            if (item) {
                // Update the avatar's clothing part
                const clothingType = area.id.replace('avatar-', '');  // e.g., 'top'
                const imageSrc = item.getAttribute('data-image-src');

                if (imageSrc) {
                    area.src = imageSrc;
                    // Update hidden input value
                    const inputId = `${clothingType}-input`;
                    const hiddenInput = document.getElementById(inputId);
                    if (hiddenInput) {
                        hiddenInput.value = imageSrc;
                    }
                    showToast(`${clothingType.charAt(0).toUpperCase() + clothingType.slice(1)} updated!`, 'success');
                }
            }
        });
    });


function setupNavigationToggle() {
    const hamburgerMenu = document.querySelector('.hamburger-menu');
    if (hamburgerMenu) {
        hamburgerMenu.addEventListener('click', toggleMobileNav);
    }

    // Close Mobile Navigation Menu when clicking a link
    document.querySelectorAll('.mobile-nav a').forEach(link => {
        link.addEventListener('click', () => {
            const mobileNav = document.getElementById('mobile-nav');
            if (mobileNav) {
                mobileNav.classList.remove('active');
            }
        });
    });
}

function toggleMobileNav() {
    const mobileNav = document.getElementById('mobile-nav');
    if (mobileNav) {
        mobileNav.classList.toggle('active');
    }
}

function setupPurchaseButtons() {
    document.querySelectorAll('.purchase-premium').forEach(button => {
        button.addEventListener('click', function () {
            const itemId = button.dataset.itemId;
            const userSubscriptionStatus = button.dataset.subscriptionStatus;

            if (userSubscriptionStatus !== 'premium') {
                alert('You need a premium subscription to purchase this item.');
            } else {
                purchaseItem(itemId);
            }
        });
    });
}

function purchaseItem(itemId) {
    // Send request to backend to complete the purchase (AJAX or form submission)
    // For simplicity, using fetch API here
    fetch(`/dressup/purchase/${itemId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            } else {
                return response.json();
            }
        })
        .catch(error => {
            console.error('Error purchasing item:', error);
            showToast('Error purchasing item. Please try again.', 'error');
        });
}

function setupTogglePremium() {
    const togglePremium = document.getElementById('toggle-premium');
    if (togglePremium) {
        togglePremium.addEventListener('change', function () {
            const premiumItems = document.querySelectorAll('.premium-item');
            const freeItems = document.querySelectorAll('.free-item');
            const isPremiumOnly = this.checked;

            if (isPremiumOnly) {
                premiumItems.forEach(item => item.style.display = 'block');
                freeItems.forEach(item => item.style.display = 'none');
            } else {
                premiumItems.forEach(item => item.style.display = 'block');
                freeItems.forEach(item => item.style.display = 'block');
            }
        });
    }
}

function setupToastNotifications() {
    // Ensure there is a toast container in your base template
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container';
        document.body.appendChild(toastContainer);
    }
}

function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerText = message;

    toastContainer.appendChild(toast);

    // Remove the toast after 3 seconds
    setTimeout(() => {
        toastContainer.removeChild(toast);
    }, 3000);
}

// Utility function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (const cookie of cookies) {
            const trimmedCookie = cookie.trim();
            // Does this cookie string begin with the name we want?
            if (trimmedCookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(trimmedCookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
