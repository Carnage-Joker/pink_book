// ==============================
// Main Script for Dressup App
// ==============================
import { avatarModule } from './avatarModule.js';
import { toastModule } from './toastModule.js';



document.addEventListener('DOMContentLoaded', () => {
    avatarModule.init();
    navigationModule.init();
    toastModule.showToast('Welcome to the Avatar Customization!', 'success');
    dragDrop.init();
});


// Example: dressup/scripts.js
function changeItem(category, direction) {
    // Retrieve current image element for the category
    const itemImg = document.getElementById(category + '-item');
    // Logic to change the item source (e.g., increment an index or fetch from a list)
    // This could be a preloaded array or fetched via AJAX.
    // Example:
    let currentSrc = itemImg.getAttribute('data-image-src');
    let newSrc = getNextImageSrc(currentSrc, direction); // You need to define getNextImageSrc()
    itemImg.src = newSrc;
    // Update corresponding hidden input so that when form is submitted, server knows new selection
    document.getElementById(category + '-input').value = newSrc;
}
