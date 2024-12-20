// ==============================
// Module: Avatar Customization
// ==============================
export const avatarModule = (() => {
    const items = {
        'dress': ['dress1.png', 'dress2.png', 'dress3.png'],
        'skirt': ['skirt1.png', 'skirt2.png', 'skirt3.png'],
        'top': ['top1.png', 'top2.png', 'top3.png'],
        'shoes': ['shoes1.png', 'shoes2.png', 'shoes3.png'],
        'accessories': ['accessory1.png', 'accessory2.png', 'accessory3.png']
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

        document.getElementById(category).src = `/static/items/${categoryItems[currentIndex[category]]}`;
    }

    function allowDrop(event) {
        event.preventDefault();
    }

    function drag(event) {
        event.dataTransfer.setData("text", event.target.id);
    }

    function drop(event) {
        event.preventDefault();
        const data = event.dataTransfer.getData("text");
        const draggedElement = document.getElementById(data);
        const targetElement = event.target;

        targetElement.src = draggedElement.src;
        animateDrop(targetElement);
    }

    function animateDrop(element) {
        element.classList.add('drop-animation');
        setTimeout(() => element.classList.remove('drop-animation'), 500);
    }

    function initDragAndDrop() {
        document.querySelectorAll('.draggable').forEach(item => {
            item.addEventListener('dragstart', drag);
        });

        document.getElementById('avatar-canvas').addEventListener('dragover', allowDrop);
        document.getElementById('avatar-canvas').addEventListener('drop', drop);
    }

    return { changeItem, initDragAndDrop };
})();
