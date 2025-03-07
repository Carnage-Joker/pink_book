// ==============================
// Module: Drag-and-Drop Logic
// ==============================
document.addEventListener('DOMContentLoaded', () => {
    const items = document.querySelectorAll('.item');
    const avatarContainer = document.getElementById('avatar');

    avatarContainer.addEventListener('dragover', (e) => {
        e.preventDefault();
    });

    avatarContainer.addEventListener('drop', (e) => {
        e.preventDefault();
        const itemID = e.dataTransfer.getData('item-id');
        const category = e.dataTransfer.getData('category');

        const targetLayer = document.getElementById(`layer-${category}`);

        if (targetLayer) {
            targetLayer.src = e.dataTransfer.getData('image-url');
            const csrfToken = getCSRFToken();
            if (!csrfToken) {
                alert('Failed to retrieve CSRF token.');
                return;
            }
            fetch(`/dressup/equip_item/${itemID}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => {
                if (response.ok) {
                    alert('Item equipped successfully!');
                } else {
                    console.error('Equip item failed:', response.statusText);
                    alert('Failed to equip item.');
                }
            })
            .catch(error => console.error('Network error:', error));
        }
    });
        


    items.forEach(item => {
        item.addEventListener('dragstart', (e) => {
            const image = item.querySelector('img').src;
            e.dataTransfer.setData('item-id', item.dataset.itemId);
            e.dataTransfer.setData('category', item.dataset.category);
        });
    });

    // Function to retrieve the CSRF token from the HTML document
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
});

