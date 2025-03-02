export const avatarModule = (() => {
    let equippedItems = {};  // Stores equipped items per category

    async function loadEquippedItems() {
        try {
            let response = await fetch('/dressup/get_equipped_items/');
            let data = await response.json();
            equippedItems = data;
            updateAvatarDisplay();
        } catch (error) {
            console.error("Error fetching equipped items:", error);
        }
    }

    async function equipItem(itemId, button) {
        if (button.disabled) return;
        button.disabled = true;

        try {
            let response = await fetch(`/dressup/equip_item/${itemId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/json',
                },
                credentials: 'include'
            });

            let data = await response.json();
            if (data.status) {
                button.innerText = data.status === "equipped" ? "Unequip" : "Equip";
            }
        } catch (error) {
            console.error("Error:", error);
        } finally {
            button.disabled = false;
        }
    }

    function changeItem(category, direction) {
        if (!equippedItems[category] || !equippedItems[category].items.length) return;

        let categoryItems = equippedItems[category].items;
        let targetLayer = document.getElementById(`layer-${category}`);
        if (!targetLayer) return;

        let currentIndex = parseInt(targetLayer.dataset.index) || 0;

        currentIndex = (direction === 'next')
            ? (currentIndex + 1) % categoryItems.length
            : (currentIndex - 1 + categoryItems.length) % categoryItems.length;

        targetLayer.dataset.index = currentIndex;

        // Preload new image
        let newImage = new Image();
        newImage.src = categoryItems[currentIndex].image_path;
        newImage.onload = () => {
            targetLayer.src = newImage.src;  // Update only after it's loaded
        };

        // Send AJAX request to update equipped item in Django
        fetch(`/dressup/equip_item/${categoryItems[currentIndex].id}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json',
            },
            credentials: 'include'
        }).catch(error => console.error("Error equipping item:", error));
    }

    function updateAvatarDisplay() {
        Object.keys(equippedItems).forEach(category => {
            const categoryData = equippedItems[category];
            const targetLayer = document.getElementById(`layer-${category}`);
            if (targetLayer && categoryData.items.length > 0) {
                let currentIndex = parseInt(targetLayer.dataset.index) || 0;
                targetLayer.src = categoryData.items[currentIndex].image_path;
            }
        });
    }

    function getCSRFToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfToken ? csrfToken.value : '';
    }

    return { loadEquippedItems, changeItem, equipItem };
})();

// Load equipped items on page load
document.addEventListener('DOMContentLoaded', () => {
    avatarModule.loadEquippedItems();
});
