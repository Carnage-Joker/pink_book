document.addEventListener('DOMContentLoaded', function () {
    const items = document.querySelectorAll('.item');
    const avatarCanvas = {
        body: document.getElementById('body'),
        top: document.getElementById('top'),
        bottom: document.getElementById('bottom'),
        shoes: document.getElementById('shoes'),
        accessories: document.getElementById('accessories')
    };

    items.forEach(item => {
        item.addEventListener('click', function () {
            const category = item.dataset.category;
            const name = item.dataset.name;
            avatarCanvas[category].src = `/static/avatars/${name}.png`;
        });
    });
});
