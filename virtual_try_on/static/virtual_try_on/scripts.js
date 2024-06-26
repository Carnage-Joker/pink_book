document.addEventListener("DOMContentLoaded", function () {
    const dropdowns = document.querySelectorAll('.feature-dropdown');
    const avatarDisplay = document.getElementById('avatar-display');

    const getCookie = (name) => {
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
    };

    const csrftoken = getCookie('csrftoken');

    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('change', function () {
            const featureType = this.getAttribute('data-type');
            const featureValue = this.value;

            console.log(`Changing feature: ${featureType}, Value: ${featureValue}`);

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
                    if (data.success) {
                        let imgElement;
                        if (featureType === 'body_skin_tone' || featureType === 'body_body_type') {
                            const skinTone = document.getElementById('skin-tone').value;
                            const bodyType = document.getElementById('body-type').value;
                            imgElement = avatarDisplay.querySelector('.body');
                            imgElement.src = `/static/virtual_try_on/avatars/body/${skinTone}/${bodyType}.png`;
                            console.log(`Updated body image to: /static/virtual_try_on/avatars/body/${skinTone}/${bodyType}.png`);
                        } else if (featureType === 'hair_hair_type' || featureType === 'hair_hair_color') {
                            const hairType = document.getElementById('hair-type').value;
                            const hairColor = document.getElementById('hair-color').value;
                            imgElement = avatarDisplay.querySelector('.hair');
                            imgElement.src = `/static/virtual_try_on/avatars/hair/${hairType}/${hairColor}.png`;
                            console.log(`Updated hair image to: /static/virtual_try_on/avatars/hair/${hairType}/${hairColor}.png`);
                        }
                    } else {
                        console.error('Data success was false:', data);
                    }
                })
                .catch(error => {
                    console.error('There was a problem with the fetch operation:', error);
                });
        });
    });

    // Define the resetAvatar function
    window.resetAvatar = function () {
        dropdowns.forEach(dropdown => {
            dropdown.value = dropdown.options[0].value; // Reset to the first option
        });
        // Optionally, reset the avatar display to default state
        avatarDisplay.querySelectorAll('img').forEach(img => {
            img.src = ''; // Set default image sources
        });
        console.log('Avatar reset to default state');
    };

    // Define the submitAvatar function
    window.submitAvatar = function () {
        // Perform actions needed to submit the avatar customization
        alert('Avatar customization submitted!');
    };
});
