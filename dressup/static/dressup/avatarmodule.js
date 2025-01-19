// ==============================
// Module: Avatar Customization
// ==============================
export const avatarModule = (() => {
    const items = {
        'dresses': ['00.png', '01.png', '02.png'],
        'skirts': ['00.png', '01.png', '02.png'],
        'tops': ['00.png', '01.png', '02.png'],
        'shoes': ['00.png', '01.png', '02.png'],
        'accessories': ['00.png', '01.png', '02.png']
    };

    let currentIndex = {
        'dresses': 0,
        'skirts': 0,
        'tops': 0,
        'shoes': 0,
        'accessories': 0
    };

    function changeItem(category, direction, callback) {
        const categoryItems = items[category];
        const currentItemIndex = currentIndex[category];
        const totalItems = categoryItems.length;

        if (direction === 'next') {
            currentIndex[category] = (currentItemIndex + 1) % totalItems;
        } else {
            currentIndex[category] = (currentItemIndex - 1 + totalItems) % totalItems;
        }

        const newItemPath = `/static/dressup/avatars/${categoryItems[currentIndex[category]]}`;
        document.getElementById(category).src = newItemPath;

        if (callback) callback(category, currentIndex[category]);
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
