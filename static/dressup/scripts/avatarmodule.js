// avatarModule.js patch
// Add an init() method so avatarModule.init() works as expected
const avatarModule = (() => {
    const items = {
        dresses: ['00.png', '01.png', '02.png'],
        skirts: ['00.png', '01.png', '02.png'],
        tops: ['00.png', '01.png', '02.png'],
        shoes: ['00.png', '01.png', '02.png'],
        accessories: ['00.png', '01.png', '02.png']
    };

    const currentIndex = {
        dresses: 0,
        skirts: 0,
        tops: 0,
        shoes: 0,
        accessories: 0
    };

    function changeItem(category, direction) {
        const categoryItems = items[category];
        if (!categoryItems) {
            console.warn(`Invalid category: ${category}`);
            return;
        }
        if (direction === 'next') {
            currentIndex[category] = (currentIndex[category] + 1) % categoryItems.length;
        } else if (direction === 'prev') {
            currentIndex[category] = (currentIndex[category] - 1 + categoryItems.length) % categoryItems.length;
        } else {
            console.warn(`Invalid direction: ${direction}. Use 'next' or 'prev'.`);
            return;
        }
        const element = document.getElementById(category);
        if (element) {
            element.src = `/static/dressup/avatars/${category}/${categoryItems[currentIndex[category]]}`;
        }
    }

    // No-op init for consistency; can wire up controls if needed
    function init() {
        // e.g. attach event listeners to buttons if you have them
        console.log('avatarModule initialized');
    }

    return { init, changeItem };
})();

export { avatarModule };  