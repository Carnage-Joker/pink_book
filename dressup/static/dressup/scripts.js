import { avatarModule } from './avatarModule.js';
import { toastModule } from './toastModule.js';
import { navigationModule } from './navigationModule.js';

document.addEventListener('DOMContentLoaded', () => {
    avatarModule.initDragAndDrop();
    navigationModule.init();
    toastModule.showToast('Welcome to the Avatar Customization!', 'success');
});
