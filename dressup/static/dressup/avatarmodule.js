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

    function changeItem(category, direction) {
        const categoryItems = items[category];
        if (!categoryItems) return;

        currentIndex[category] = (direction === 'next')
            ? (currentIndex[category] + 1) % categoryItems.length
            : (currentIndex[category] - 1 + categoryItems.length) % categoryItems.length;

        document.getElementById(category).src = `/static/dressup/avatars/${categoryItems[currentIndex[category]]}`;
    }

    return { changeItem };
})();
