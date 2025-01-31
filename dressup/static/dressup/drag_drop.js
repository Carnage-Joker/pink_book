// ==============================
// Module: Drag-and-Drop Logic
// ==============================
export const dragDrop = (() => {
    function allowDrop(event) {
        event.preventDefault();
    }

    function drag(event) {
        event.dataTransfer.setData('text/plain', event.target.id);
    }

    function drop(event) {
        event.preventDefault();
        const itemID = event.dataTransfer.getData('text/plain');
        const category = event.dataTransfer.getData('category');

        const targetLayer = document.getElementById(`layer-${category}`);
        if (targetLayer) {
            targetLayer.src = event.dataTransfer.getData('image-url');
            equipItem(itemID);
        }
    }

    function equipItem(itemID) {
        fetch(`/dressup/equip_item/${itemID}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    toastModule.showToast('Item equipped successfully!', 'success');
                } else {
                    toastModule.showToast('Failed to equip item.', 'error');
                }
            })
            .catch(error => console.error('Network error:', error));
    }

    function getCSRFToken() {
        return document.cookie.split('; ').find(row => row.startsWith('csrftoken'))?.split('=')[1];
    }

    function init() {
        document.querySelectorAll('.draggable').forEach(item => {
            item.addEventListener('dragstart', drag);
        });

        const avatarCanvas = document.getElementById('avatar-canvas');
        if (avatarCanvas) {
            avatarCanvas.addEventListener('dragover', allowDrop);
            avatarCanvas.addEventListener('drop', drop);
        }
    }

    return { init };
})();
