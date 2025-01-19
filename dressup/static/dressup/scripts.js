import { avatarModule } from './avatarModule.js';
import { toastModule } from './toastModule.js';
import { navigationModule } from './navigationModule.js';
import { dragDrop } from './drag_drop.js';

document.addEventListener('DOMContentLoaded', () => {
    avatarModule.init();
    navigationModule.init();
    toastModule.showToast('Welcome to the Avatar Customization!', 'success');
    dragDrop.init();
});
