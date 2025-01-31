// ==============================
// Main Script for Dressup App
// ==============================
import { avatarModule } from './avatarModule.js';
import { toastModule } from './toastModule.js';
import { navigationModule } from './navigationModule.js';
import { dragDrop } from './dragDrop.js';

document.addEventListener('DOMContentLoaded', () => {
    avatarModule.init();
    navigationModule.init();
    toastModule.showToast('Welcome to the Avatar Customization!', 'success');
    dragDrop.init();
});
