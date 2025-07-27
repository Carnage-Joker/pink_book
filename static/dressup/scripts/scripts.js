// ==============================
// Main Script for Dressup App patch
// ==============================
import { avatarModule } from './avatarModule.js';
import { toastModule } from './toastModule.js';
import { initCycling } from './itemCycling.js';
import { navigationModule } from './navigationModule.js';
import { livePreviewModule } from './dress_up_live_preview.js'; // fixed import name

// Initialize modules
avatarModule.init();
toastModule.init();
initCycling();
navigationModule.init();
livePreviewModule.init(); // now matches imported name
