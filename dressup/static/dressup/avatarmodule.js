// avatarModule.js

// We wrap everything in an IIFE (Immediately Invoked Function Expression)
// and return an object with a single method: changeItem.
const avatarModule = (() => {
    const items = {
        dresses: ['00.png', '01.png', '02.png'],
        skirts: ['00.png', '01.png', '02.png'],
        tops: ['00.png', '01.png', '02.png'],
        shoes: ['00.png', '01.png', '02.png'],
        accessories: ['00.png', '01.png', '02.png']
    };

    // Track the current index for each category
    const currentIndex = {
        dresses: 0,
        skirts: 0,
        tops: 0,
        shoes: 0,
        accessories: 0
    };

    /**
     * Changes the current item in the specified category.
     * @param {string} category - The category of the item (e.g., 'dresses', 'skirts').
     * @param {string} direction - The direction to change the item ('next' or 'prev').
     */
    function changeItem(category, direction) {
        // Ensure the category exists in our items dictionary
        const categoryItems = items[category];
        if (!categoryItems) {
            console.warn(`Invalid category: ${category}`);
            return;
        }

        // Update currentIndex[category] based on 'next' or 'prev'
        if (direction === 'next') {
            currentIndex[category] = (currentIndex[category] + 1) % categoryItems.length;
        } else if (direction === 'prev') {
            currentIndex[category] = (currentIndex[category] - 1 + categoryItems.length) % categoryItems.length;
        } else {
            console.warn(`Invalid direction: ${direction}. Use 'next' or 'prev'.`);
            return;
        }

        // Update the corresponding <img> element on the page
        const element = document.getElementById(category);
        if (element) {
            // Example path: /static/dressup/avatars/dresses/01.png
            element.src = `/static/dressup/avatars/${category}/${categoryItems[currentIndex[category]]}`;
        } else {
            console.warn(`Element with ID "${category}" not found in the DOM.`);
        }
    }

    // Expose public methods
    return { changeItem };
})();

// Named export so you can import { avatarModule } from "./avatarModule.js";
export { avatarModule };
