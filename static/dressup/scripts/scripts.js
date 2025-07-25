// ==============================
// Main Script for Dressup App
// ==============================
import { avatarModule } from './avatarModule.js';
import { toastModule } from './toastModule.js';
import { initCycling } from './itemCycling.js';
import { navigationModule } from './navigationModule.js';
import { dressUpLivePreview } from './dress_up_live_preview.js';
// Initialize the avatar module

avatarModule.init();
// Initialize the toast module
toastModule.init();
// Initialize item cycling functionality
initCycling();
// Initialize the navigation module
navigationModule.init();
// Initialize the live preview module
livePreviewModule.init();
