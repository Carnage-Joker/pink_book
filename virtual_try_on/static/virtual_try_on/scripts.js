document.addEventListener("DOMContentLoaded", function () {
    const bodyTypeEl = document.getElementById('body-type');
    const skinToneEl = document.getElementById('skin-tone');
    const hairTypeEl = document.getElementById('hair-type');
    const hairColorEl = document.getElementById('hair-color');

    window.updateAvatar = function () {
        const bodyType = bodyTypeEl.value;
        const skinTone = skinToneEl.value;
        const hairType = hairTypeEl.value;
        const hairColor = hairColorEl.value;

        document.getElementById('avatar-body').src = `/static/virtual_try_on/avatars/body/${skinTone}/${bodyType}.png`;
        document.getElementById('avatar-hair').src = `/static/virtual_try_on/avatars/hair/${hairType}/${hairColor}.png`;

        const avatarDisplay = document.getElementById('avatar-display');
        avatarDisplay.classList.remove('hourglass', 'straight', 'thick', 'slim');
        avatarDisplay.classList.add(bodyType);
    };

    window.resetAvatar = function () {
        bodyTypeEl.value = 'hourglass';
        skinToneEl.value = 'light';
        hairTypeEl.value = 'long_straight';
        hairColorEl.value = 'blonde';
        updateAvatar();
    };

    window.randomizeAvatar = function () {
        const bodyTypes = ['hourglass', 'slim', 'straight', 'thick'];
        const skinTones = ['light', 'brown', 'dark'];
        const hairStyles = ['long_straight', 'long_curly', 'short_straight', 'short_curly', 'bob'];
        const hairColors = ['black', 'brown', 'blonde', 'red', 'pink'];

        const randomBodyType = bodyTypes[Math.floor(Math.random() * bodyTypes.length)];
        const randomSkinTone = skinTones[Math.floor(Math.random() * skinTones.length)];
        const randomHairStyle = hairStyles[Math.floor(Math.random() * hairStyles.length)];
        const randomHairColor = hairColors[Math.floor(Math.random() * hairColors.length)];

        bodyTypeEl.value = randomBodyType;
        skinToneEl.value = randomSkinTone;
        hairTypeEl.value = randomHairStyle;
        hairColorEl.value = randomHairColor;

        updateAvatar();
    };

    window.saveAvatar = function () {
        const bodyType = bodyTypeEl.value;
        const skinTone = skinToneEl.value;
        const hairType = hairTypeEl.value;
        const hairColor = hairColorEl.value;

        fetch("/save_avatar/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ body_type: bodyType, skin_tone: skinTone, hair_type: hairType, hair_color: hairColor })
        }).then(response => {
            if (response.ok) {
                window.location.href = "/dress_up_game/";
            } else {
                alert('Failed to save avatar');
            }
        });
    };

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

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
            event.target.style.transform = 'translate(0px, 0px)';
            event.target.setAttribute('data-x', 0);
            event.target.setAttribute('data-y', 0);
        }
    });

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

    function dragMoveListener(event) {
        const target = event.target;
        const x = (parseFloat(target.getAttribute('data-x')) || 0)### Complete `scripts.js`:

        ```javascript
document.addEventListener("DOMContentLoaded", function () {
    const bodyTypeEl = document.getElementById('body-type');
    const skinToneEl = document.getElementById('skin-tone');
    const hairTypeEl = document.getElementById('hair-type');
    const hairColorEl = document.getElementById('hair-color');

    window.updateAvatar = function () {
        const bodyType = bodyTypeEl.value;
        const skinTone = skinToneEl.value;
        const hairType = hairTypeEl.value;
        const hairColor = hairColorEl.value;

        document.getElementById('avatar-body').src = `/ static / virtual_try_on / avatars / body / ${ skinTone } /${bodyType}.png`;
        document.getElementById('avatar-hair').src = `/static/virtual_try_on/avatars/hair/${hairType}/${hairColor}.png`;

        const avatarDisplay = document.getElementById('avatar-display');
        avatarDisplay.classList.remove('hourglass', 'straight', 'thick', 'slim');
        avatarDisplay.classList.add(bodyType);
    };

    window.resetAvatar = function () {
        bodyTypeEl.value = 'hourglass';
        skinToneEl.value = 'light';
        hairTypeEl.value = 'long_straight';
        hairColorEl.value = 'blonde';
        updateAvatar();
    };

    window.randomizeAvatar = function () {
        const bodyTypes = ['hourglass', 'slim', 'straight', 'thick'];
        const skinTones = ['light', 'brown', 'dark'];
        const hairStyles = ['long_straight', 'long_curly', 'short_straight', 'short_curly', 'bob'];
        const hairColors = ['black', 'brown', 'blonde', 'red', 'pink'];

        const randomBodyType = bodyTypes[Math.floor(Math.random() * bodyTypes.length)];
        const randomSkinTone = skinTones[Math.floor(Math.random() * skinTones.length)];
        const randomHairStyle = hairStyles[Math.floor(Math.random() * hairStyles.length)];
        const randomHairColor = hairColors[Math.floor(Math.random() * hairColors.length)];

        bodyTypeEl.value = randomBodyType;
        skinToneEl.value = randomSkinTone;
        hairTypeEl.value = randomHairStyle;
        hairColorEl.value = randomHairColor;

        updateAvatar();
    };

    window.saveAvatar = function () {
        const bodyType = bodyTypeEl.value;
        const skinTone = skinToneEl.value;
        const hairType = hairTypeEl.value;
        const hairColor = hairColorEl.value;

        fetch("/save_avatar/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ body_type: bodyType, skin_tone: skinTone, hair_type: hairType, hair_color: hairColor })
        }).then(response => {
            if (response.ok) {
                window.location.href = "/dress_up_game/";
            } else {
                alert('Failed to save avatar');
            }
        });
    };

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

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
            event.target.style.transform = 'translate(0px, 0px)';
            event.target.setAttribute('data-x', 0);
            event.target.setAttribute('data-y', 0);
        }
    });

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

    function dragMoveListener(event) {
        const target = event.target;
        const x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx;
        const y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

        target.style.transform = `translate(${x}px, ${y}px)`;
        target.setAttribute('data-x', x);
        target.setAttribute('data-y', y);
    }

    function updateAvatarClothing(category, src) {
        const imgElement = document.getElementById(`avatar-${category}`);
        imgElement.src = src;
    }

    window.resetAvatarClothing = function () {
        document.getElementById('avatar-top').src = '/static/virtual_try_on/garmets/tops/1.png';
        document.getElementById('avatar-bottom').src = '/static/virtual_try_on/garmets/skirts/1.png';
        document.getElementById('avatar-shoes').src = '/static/virtual_try_on/garmets/shoes/1.png';
    };

    window.saveAvatarClothing = function () {
        const top = document.getElementById('avatar-top').src;
        const bottom = document.getElementById('avatar-bottom').src;
        const shoes = document.getElementById('avatar-shoes').src;

        saveClothing('top', top);
        saveClothing('bottom', bottom);
        saveClothing('shoes', shoes);

        alert('Avatar customization saved!');
    };

    function saveClothing(category, src) {
        const csrftoken = getCookie('csrftoken');

        fetch("/update_avatar_clothing/", {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ category: category, src: src })
        }).then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok, status: ${response.status}`);
            }
            return response.json();
        }).then(data => {
            if (!data.success) {
                console.error('Error updating clothing:', data);
            }
        }).catch(error => {
            console.error('Fetch error:', error);
        });
    }
});
