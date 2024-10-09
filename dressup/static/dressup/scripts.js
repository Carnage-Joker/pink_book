// Toggle Mobile Navigation Menu
function toggleMobileNav() {
    const mobileNav = document.getElementById('mobile-nav');
    mobileNav.classList.toggle('active');
}

// Close Mobile Navigation Menu when clicking a link
document.querySelectorAll('.mobile-nav a').forEach(link => {
    link.addEventListener('click', () => {
        const mobileNav = document.getElementById('mobile-nav');
        mobileNav.classList.remove('active');
    });
});

// Drag and Drop for Dress-up Game
document.addEventListener('DOMContentLoaded', function () {
    // Make clothing items draggable
    const clothingItems = document.querySelectorAll('.clothing-item');
    clothingItems.forEach(item => {
        item.draggable = true;

        item.addEventListener('dragstart', function (event) {
            event.dataTransfer.setData('text/plain', event.target.id);
            event.dataTransfer.effectAllowed = 'move';
        });
    });

    // Avatar areas where clothing can be dropped
    const dropAreas = document.querySelectorAll('.drop-area');
    dropAreas.forEach(area => {
        area.addEventListener('dragover', function (event) {
            event.preventDefault();
            event.dataTransfer.dropEffect = 'move';
        });

        area.addEventListener('drop', function (event) {
            event.preventDefault();
            const itemId = event.dataTransfer.getData('text/plain');
            const item = document.getElementById(itemId);

            // Clone the item for multiple usage (remove original if needed)
            const clonedItem = item.cloneNode(true);
            area.innerHTML = ''; // Clear previous item
            area.appendChild(clonedItem);

            // Update avatar with selected clothing
            updateAvatar(area.dataset.type, itemId);
        });
    });
});

// Update avatar with selected clothing
function updateAvatar(type, itemId) {
    // Logic for updating avatar state based on type (e.g., 'top', 'bottom')
    const avatar = document.getElementById('avatar');
    const clothingElement = document.getElementById(itemId);

    // Update the avatar display (this can be customized)
    if (type === 'top') {
        avatar.querySelector('.top').src = clothingElement.dataset.imageSrc;
    } else if (type === 'bottom') {
        avatar.querySelector('.bottom').src = clothingElement.dataset.imageSrc;
    } else if (type === 'shoes') {
        avatar.querySelector('.shoes').src = clothingElement.dataset.imageSrc;
    } else if (type === 'accessory') {
        avatar.querySelector('.accessory').src = clothingElement.dataset.imageSrc;
    }
}

// Toggle post-it notes for navigation on different screen sizes
window.addEventListener('resize', function () {
    const postItNav = document.querySelector('nav.post-it-notes');
    const hamburgerMenu = document.querySelector('.hamburger-menu');

    if (window.innerWidth < 768) {
        postItNav.style.display = 'none';
        hamburgerMenu.style.display = 'block';
    } else {
        postItNav.style.display = 'flex';
        hamburgerMenu.style.display = 'none';
    }
});

// On document load, set the proper navigation display
document.addEventListener('DOMContentLoaded', function () {
    const postItNav = document.querySelector('nav.post-it-notes');
    const hamburgerMenu = document.querySelector('.hamburger-menu');

    if (window.innerWidth < 768) {
        postItNav.style.display = 'none';
        hamburgerMenu.style.display = 'block';
    } else {
        postItNav.style.display = 'flex';
        hamburgerMenu.style.display = 'none';
    }
});

// Handle premium item purchases
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

// Function to handle item purchase logic
function purchaseItem(itemId) {
    // Send request to backend to complete the purchase (AJAX or form submission)
    // Update the UI to reflect the item being added to the user's collection
    console.log(`Item with ID: ${itemId} purchased successfully!`);
    alert(`Item with ID: ${itemId} has been purchased!`);
}

// Toggle the display of premium items vs. free items in the mall
document.getElementById('toggle-premium').addEventListener('click', function () {
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

// Toast Notifications for various actions
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerText = message;

    toastContainer.appendChild(toast);

    // Remove the toast after 3 seconds
    setTimeout(() => {
        toastContainer.removeChild(toast);
    }, 3000);
}
