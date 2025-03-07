// itemCycling.js
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
    const totalItems = categoryItems.length;
    currentIndex[category] =
        direction === 'next'
            ? (currentIndex[category] + 1) % totalItems
            : (currentIndex[category] - 1 + totalItems) % totalItems;

    document.getElementById(`layer-${category}`).src = `/static/items/${categoryItems[currentIndex[category]]}`;
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