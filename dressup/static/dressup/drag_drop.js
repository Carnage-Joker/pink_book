document.addEventListener('DOMContentLoaded', () => {
    const items = document.querySelectorAll('.item');
    const avatarContainer = document.getElementById('avatar');

    // Allow the avatar to accept drops
    avatarContainer.addEventListener('dragover', (e) => {
        e.preventDefault();
    });

    avatarContainer.addEventListener('drop', (e) => {
        e.preventDefault();
        const itemID = e.dataTransfer.getData('item-id');
        const category = e.dataTransfer.getData('category');

        // Find the corresponding avatar layer
        const targetLayer = document.getElementById(`layer-${category}`);

        if (targetLayer) {
            // Replace the avatar layer with the new item
            targetLayer.src = e.dataTransfer.getData('image-url');

            // Optional: Send a POST request to update equipped items
            fetch(`/dressup/equip_item/${itemID}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/json',
                },
            }).then(response => {
                if (response.ok) {
                    alert('Item equipped successfully!');
                } else {
                    alert('Failed to equip item.');
                }
            });
        }
    });

    // Dragstart event for inventory items
    items.forEach(item => {
        item.addEventListener('dragstart', (e) => {
            const image = item.querySelector('img').src;
            e.dataTransfer.setData('item-id', item.dataset.itemId);
            e.dataTransfer.setData('category', item.dataset.category);
            e.dataTransfer.setData('image-url', image);
        });
    });

    // Function to get CSRF token for POST requests
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
});
