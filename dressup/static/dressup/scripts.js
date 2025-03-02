import { avatarModule } from './avatarModule.js';
import { toastModule } from './toastModule.js';
import { navigationModule } from './navigationModule.js';
import { dragDrop } from './drag_drop.js';

document.addEventListener('DOMContentLoaded', () => {
    avatarModule.init();
    navigationModule.init();
    toastModule.showToast('Welcome to the Avatar Customization!', 'success');
    dragDrop.init();
});


document.addEventListener('DOMContentLoaded', function () {
    const items = {
        'dress': ['dress1.svg', 'dress2.svg', 'dress3.svg'],
        'skirt': ['skirt1.svg', 'skirt2.svg', 'skirt3.svg'],
        'top': ['top1.svg', 'top2.svg', 'top3.svg'],
        'shoes': ['shoes1.svg', 'shoes2.svg', 'shoes3.svg'],
        'accessories': ['accessory1.svg', 'accessory2.svg', 'accessory3.svg']
    };

    let currentIndex = {
        'dress': 0,
        'skirt': 0,
        'top': 0,
        'shoes': 0,
        'accessories': 0
    };

    function changeItem(category, direction) {
        const categoryItems = items[category];
        const currentItemIndex = currentIndex[category];
        const totalItems = categoryItems.length;

        if (direction === 'next') {
            currentIndex[category] = (currentItemIndex + 1) % totalItems;
        } else {
            currentIndex[category] = (currentItemIndex - 1 + totalItems) % totalItems;
        }

        document.getElementById(`layer-${category}`).src = `/static/items/${categoryItems[currentIndex[category]]}`;
    }

    function allowDrop(event) {
        event.preventDefault();
    }

    function drag(event) {
        event.dataTransfer.setData("item-id", event.target.dataset.itemId);
        event.dataTransfer.setData("category", event.target.dataset.category);
        event.dataTransfer.setData("image-url", event.target.src);
    }

    function drop(event) {
        event.preventDefault();
        const itemId = event.dataTransfer.getData("item-id");
        const category = event.dataTransfer.getData("category");
        const imageUrl = event.dataTransfer.getData("image-url");

        const targetLayer = document.getElementById(`layer-${category}`);
        if (targetLayer) {
            targetLayer.src = imageUrl;

            fetch(`/dressup/equip_item/${itemId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'equipped') {
                    alert(`${data.message}`);
                } else {
                    alert(`Failed to equip item.`);
                }
            });
        }
    }

    document.querySelectorAll('.item').forEach(item => {
        item.addEventListener('dragstart', drag);
    });

    document.getElementById('avatar-container').addEventListener('dragover', allowDrop);
    document.getElementById('avatar-container').addEventListener('drop', drop);

    // Example event listeners for navigation
    document.querySelectorAll('.prev-arrow').forEach(btn => {
        btn.addEventListener('click', () => changeItem(btn.dataset.category, 'prev'));
    });

    document.querySelectorAll('.next-arrow').forEach(btn => {
        btn.addEventListener('click', () => changeItem(btn.dataset.category, 'next'));
    });
});
