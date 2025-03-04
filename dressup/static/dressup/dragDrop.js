function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}

export function dragDrop() {
    const items = document.querySelectorAll('.draggable');
    document.addEventListener('DOMContentLoaded', () => {
        const avatarContainer = document.getElementById('avatar-container');

        if (!avatarContainer) {
            console.error("Avatar container not found!");
            return;
        }

                // Enable dragover on avatar
                avatarContainer.addEventListener('dragover', (e) => {
                    e.preventDefault();
        });

        avatarContainer.addEventListener('drop', (e) => {
            e.preventDefault();
            const itemID = e.dataTransfer.getData('item-id');
            const category = e.dataTransfer.getData('category');

            // Find corresponding avatar layer
            const targetLayer = document.querySelector(`.layer.${category}`);

            if (!targetLayer) {
                console.warn(`No avatar layer found for category: ${category}`);
                return;
            }

            targetLayer.src = e.dataTransfer.getData('image-url');

            // Send AJAX request to equip item
            fetch(`/dressup/equip_item/${itemID}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/json',
                },
            }).then(response => {
                if (response.ok) {
                    console.log('Item equipped successfully!');
                } else {
                    console.error('Failed to equip item.');
                }
            }).catch(error => console.error('Error:', error));
        });
                    const category = e.dataTransfer.getData('category');
        
                    // Find corresponding avatar layer
                    const targetLayer = document.querySelector(`.layer.${category}`);
        
                    if (!targetLayer) {
                        console.warn(`No avatar layer found for category: ${category}`);
                        return;
                    }
        
                    targetLayer.src = e.dataTransfer.getData('image-url');
        
                    // Send AJAX request to equip item
                    fetch(`/dressup/equip_item/${itemID}/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCSRFToken(),
                            'Content-Type': 'application/json',
                        },
                    }).then(response => {
                        if (response.ok) {
                            console.log(`Item ${itemID} equipped successfully in category ${category}!`);
                        } else {
                            console.error(`Failed to equip item ${itemID} in category ${category}. Response status: ${response.status}`);
                        }
                    }).catch(error => console.error(`Error equipping item ${itemID}:`, error));
                });
        
                // Enable dragging for inventory items
                items.forEach(item => {
                    item.addEventListener('dragstart', (e) => {
                        console.log(`Dragging item: ${item.dataset.itemId}`);
                        const image = item.querySelector('img').src;
                console.log(`Dragging item: ${item.dataset.itemId}, category: ${item.dataset.category}`);
                        e.dataTransfer.setData('image-url', image);
                        e.dataTransfer.setData('category', item.dataset.category);
                    });
                });
            });
        }