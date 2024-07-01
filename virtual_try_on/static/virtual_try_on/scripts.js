document.addEventListener("DOMContentLoaded", function () {
    // Avatar Customization Functions

    // Update body type
    window.updateBodyType = function (bodyType) {
        document.getElementById('body-type').value = bodyType;
        updateAvatar();
    };

    // Reset avatar to default state
    window.resetAvatar = function () {
        document.getElementById('body-type').value = 'hourglass';
        document.getElementById('skin-tone').value = 'light';
        document.getElementById('hair-type').value = 'long_straight';
        document.getElementById('hair-color').value = 'blonde';
        resetAvatarClothing();
        updateAvatar();
    };

    // Randomize avatar features
    window.randomizeAvatar = function () {
        const bodyTypes = ['hourglass', 'slim', 'straight', 'thick'];
        const skinTones = ['light', 'brown', 'dark'];
        const hairStyles = ['long_straight', 'long_curly', 'short_straight', 'short_curly', 'bob'];
        const hairColors = ['black', 'brown', 'blonde', 'red', 'pink'];

        const randomBodyType = bodyTypes[Math.floor(Math.random() * bodyTypes.length)];
        const randomSkinTone = skinTones[Math.floor(Math.random() * skinTones.length)];
        const randomHairStyle = hairStyles[Math.floor(Math.random() * hairStyles.length)];
        const randomHairColor = hairColors[Math.floor(Math.random() * hairColors.length)];

        document.getElementById('body-type').value = randomBodyType;
        document.getElementById('skin-tone').value = randomSkinTone;
        document.getElementById('hair-type').value = randomHairStyle;
        document.getElementById('hair-color').value = randomHairColor;

        updateAvatar();
    };

    // Update avatar display
    window.updateAvatar = function () {
        const bodyType = document.getElementById('body-type').value;
        const skinTone = document.getElementById('skin-tone').value;
        const hairType = document.getElementById('hair-type').value;
        const hairColor = document.getElementById('hair-color').value;

        document.getElementById('avatar-body').src = `/static/virtual_try_on/avatars/body/${skinTone}/${bodyType}.png`;
        document.getElementById('avatar-hair').src = `/static/virtual_try_on/avatars/hair/${hairType}/${hairColor}.png`;
    };

    // Save avatar customization and redirect to dress-up game
    window.saveAvatar = function () {
        const bodyType = document.getElementById('body-type').value;
        const skinTone = document.getElementById('skin-tone').value;
        const hairType = document.getElementById('hair-type').value;
        const hairColor = document.getElementById('hair-color').value;

        updateAvatarFeature('body', `${skinTone}/${bodyType}`);
        updateAvatarFeature('hair', `${hairType}/${hairColor}`);

        alert('Avatar customization saved!');

        // Redirect to dress up game
        window.location.href = "/virtual_try_on/dress_up_game/";
    };

    // Helper function to update avatar features on the server
    function updateAvatarFeature(featureType, featureValue) {
        const csrftoken = getCookie('csrftoken');

        fetch("/update_avatar_feature/", {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ feature_type: featureType, feature_value: featureValue })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Network response was not ok, status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (!data.success) {
                    console.error('Data success was false:', data);
                }
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    }

    // Helper function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Dress Up Game Functions

    // Enable draggable elements
    interact('.draggable').draggable({
        inertia: true,
        modifiers: [
            interact.modifiers.restrictRect({
                restriction: 'parent',
                endOnly: true
            })
        ],
        autoScroll: true,
        onmove: dragMoveListener,
        onend: function (event) {
            // Reset the element's position after dragging ends
            event.target.style.transform = 'translate(0px, 0px)';
            event.target.setAttribute('data-x', 0);
            event.target.setAttribute('data-y', 0);
        }
    });

    // Enable dropzone on avatar display
    interact('#avatar-display').dropzone({
        accept: '.draggable',
        overlap: 0.75,
        ondrop: function (event) {
            const draggableElement = event.relatedTarget;
            const category = draggableElement.getAttribute('data-category');
            const src = draggableElement.getAttribute('data-src');

            updateAvatarClothing(category, src);
        }
    });

    // Helper function to handle dragging movement
    function dragMoveListener(event) {
        const target = event.target;
        const x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx;
        const y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

        target.style.transform = `translate(${x}px, ${y}px)`;
        target.setAttribute('data-x', x);
        target.setAttribute('data-y', y);
    }

    // Update avatar clothing display
    function updateAvatarClothing(category, src) {
        const imgElement = document.getElementById(`avatar-${category}`);
        imgElement.src = src;
    }

    // Reset avatar clothing to default state
    function resetAvatarClothing() {
        document.getElementById('avatar-top').src = '';
        document.getElementById('avatar-bottom').src = '';
        document.getElementById('avatar-shoes').src = '';
        document.getElementById('avatar-accessory').src = '';
    }

    // Save avatar clothing customization
    window.saveAvatar = function () {
        const top = document.getElementById('avatar-top').src;
        const bottom = document.getElementById('avatar-bottom').src;
        const shoes = document.getElementById('avatar-shoes').src;
        const accessory = document.getElementById('avatar-accessory').src;

        saveClothing('top', top);
        saveClothing('bottom', bottom);
        saveClothing('shoes', shoes);
        saveClothing('accessory', accessory);

        alert('Avatar customization saved!');
    };

    // Helper function to save clothing to the server
    function saveClothing(category, src) {
        const csrftoken = getCookie('csrftoken');

        fetch("/update_avatar_clothing/", {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ category: category, src: src })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Network response was not ok, status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (!data.success) {
                    console.error('Data success was false:', data);
                }
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    }
});
