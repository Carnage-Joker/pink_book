// ==============================
// Module: UI Helpers
// ==============================
export const uiHelpers = (() => {
    const toastContainerId = 'toast-container';

    // Ensure a container for toasts exists
    function getToastContainer() {
        let container = document.getElementById(toastContainerId);
        if (!container) {
            container = document.createElement('div');
            container.id = toastContainerId;
            // Inline styles for demo purposes; ideally, these should be in your CSS file.
            container.style.position = 'fixed';
            container.style.top = '20px';
            container.style.right = '20px';
            container.style.zIndex = '10000';
            container.style.display = 'flex';
            container.style.flexDirection = 'column';
            container.style.gap = '10px';
            document.body.appendChild(container);
        }
        return container;
    }

    /**
     * Displays a toast notification.
     * @param {string} message - The message to display.
     * @param {string} type - The type of toast (e.g., 'info', 'success', 'error').
     * @param {number} duration - How long (in ms) before the toast starts fading out.
     */
    function showToast(message, type = 'info', duration = 3000) {
        const container = getToastContainer();
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerText = message;
        container.appendChild(toast);

        // Start fade-out after the specified duration
        setTimeout(() => {
            toast.classList.add('fade-out');
            toast.addEventListener('transitionend', () => {
                toast.remove();
                // Remove container if no toasts remain
                if (container.children.length === 0) {
                    container.remove();
                }
            });
        }, duration);
    }

    return { showToast };
})();
