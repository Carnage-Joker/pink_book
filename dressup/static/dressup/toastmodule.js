// ==============================
// Module: Toast Notifications
// ==============================
export const toastModule = (() => {
    function showToast(message, type = 'info') {
        const toastContainer = document.querySelector('.toast-container');
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerText = message;

        toastContainer.appendChild(toast);
        animateToast(toast);

        setTimeout(() => {
            toastContainer.removeChild(toast);
        }, 3000);
    }

    function animateToast(toast) {
        toast.style.opacity = 0;
        setTimeout(() => {
            toast.style.transition = 'opacity 0.5s';
            toast.style.opacity = 1;
        }, 10);
    }

    return { showToast };
})();