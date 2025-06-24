// itemCycling.js

const items = {
    'dress': ['00.png', '01.png', '02.png', '03.png', '04.png', '05.png', '06.png', '07.png', '08.png', '09.png'],
    'skirt': ['00.png', '01.png', '02.png', '03.png', '04.png', '05.png', '06.png', '07.png', '08.png', '09.png'],
    'top': ['00.png', '01.png', '02.png', '03.png', '04.png', '05.png', '06.png', '07.png', '08.png', '09.png'],
    'hair': ['00.png', '01.png', '02.png', '03.png', '04.png', '05.png', '06.png', '07.png', '08.png', '09.png'],
    'shoes': ['00.png', '01.png', '02.png', '03.png', '04.png', '05.png', '06.png', '07.png', '08.png', '09.png'],
    'accessory': ['00.png', '01.png', '02.png', '03.png', '04.png', '05.png', '06.png', '07.png', '08.png', '09.png'],
};

let currentIndex = {
    'dress': 0,
    'skirt': 0,
    'top': 0,
    'shoes': 0,
    'accessory': 0,
    'hair': 0
};

function changeItem(category, direction) {
    const categoryItems = items[category];
    const totalItems = categoryItems.length;
    currentIndex[category] =
        (direction === 'next')
            ? (currentIndex[category] + 1) % totalItems
            : (currentIndex[category] - 1 + totalItems) % totalItems;

    document.getElementById(`layer-${category}`).src = `/static/items/` + categoryItems[currentIndex[category]];
}

function initCycling() {
    document.querySelectorAll('.prev-arrow').forEach(btn => {
        btn.addEventListener('click', () => changeItem(btn.dataset.category, 'prev'));
    });
    document.querySelectorAll('.next-arrow').forEach(btn => {
        btn.addEventListener('click', () => changeItem(btn.dataset.category, 'next'));
    });
}

export { initCycling };

