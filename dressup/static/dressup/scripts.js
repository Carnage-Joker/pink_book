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
