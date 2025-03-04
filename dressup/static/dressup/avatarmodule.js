// ==============================
// Module: Avatar Customization
// ==============================
const avatarModule = () => {
    const items = {
        dresses: ['00.png', '01.png', '02.png'],
        skirts: ['00.png', '01.png', '02.png'],
        tops: ['00.png', '01.png', '02.png'],
        shoes: ['00.png', '01.png', '02.png'],
        accessories: ['00.png', '01.png', '02.png']
    };

    let currentIndex = {
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
     * @returns {void}
     */
    function changeItem(category, direction) {
        const categoryItems = items[category];
        if (!categoryItems) {
            console.warn(`Invalid category: ${category}`);
            return;
        }
        } else if (direction === 'prev') {
            currentIndex[category] = (currentIndex[category] - 1 + categoryItems.length) % categoryItems.length;
        }
        } else {
            currentIndex[category] = (currentIndex[category] - 1 + categoryItems.length) % categoryItems.length;
        }

        const element = document.getElementById(category);
        if (element) {
            element.src = `/static/dressup/avatars/${categoryItems[currentIndex[category]]}`;
        } else {
            console.warn(`Element with ID ${category} not found.`);
        }
    }

    return { changeItem };
};

export const avatarModule = avatarModule();
