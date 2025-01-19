// ==============================
// Module: Toast Notifications
// ==============================
export const toastModule = (() => {
    function showToast(message, type = 'info', duration = 3000) {
        const toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            console.error('Toast container not found.');
            return;
        }

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerText = message;

        toastContainer.appendChild(toast);
        animateToast(toast);

        setTimeout(() => {
            if (toast.parentElement === toastContainer) {
                toastContainer.removeChild(toast);
            }
        }, duration);
    }

    function animateToast(toast) {
        toast.style.opacity = 0;
        setTimeout(() => {
            toast.style.transition = 'opacity 0.5s';
            toast.style.opacity = 1;
        }, 10);

    return { showToast };
})();
