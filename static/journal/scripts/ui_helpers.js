// ==============================
// Module: UI Helpers
// ==============================
export const uiHelpers = (() => {
    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerText = message;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    return { showToast };
})();
