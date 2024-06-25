document.addEventListener("DOMContentLoaded", function () {
    const panels = document.querySelectorAll('.panel');
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

    panels.forEach(panel => {
        panel.addEventListener('click', function () {
            const featureType = this.getAttribute('data-type');
            const featureValue = this.getAttribute('data-value');

            fetch("{% url 'update_avatar_feature' %}", {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ feature_type: featureType, feature_value: featureValue })
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        // Update avatar display based on selected feature
                        let imgElement = avatarDisplay.querySelector(`.${featureType}`);
                        imgElement.src = `/static/virtual_try_on/avatars/${featureType}/${featureValue}.png`;

                        // Adjust size if it's hair
                        if (featureType === 'hair') {
                            imgElement.style.width = '80%';
                            imgElement.style.top = '0';
                            imgElement.style.left = '10%';
                        }
                    }
                })
                .catch(error => console.error('There was a problem with the fetch operation:', error));
        });
    });
});
