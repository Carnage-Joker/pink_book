// ==============================
// Module: Toast Notifications
// ==============================
export const toastModule = (() => {
    function showToast(message, type = 'info', duration = 3000) {
        const toastContainer = document.querySelector('.toast-container') || createToastContainer();

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerText = message;
        toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, duration);
    }

    function createToastContainer() {
        const container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
        return container;
    }

    return { showToast };
})();
