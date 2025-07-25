export const dressUpLivePreview = createLivePreview();

function createLivePreview() {
    let lastEquipped = {};

    return (() => {
        function init() {
            setupDragAndDrop();
            setupUndoButton();
        }

        function setupDragAndDrop() {
            document.querySelectorAll('.item, .thumbnail').forEach(item => {
                item.setAttribute('draggable', 'true');
                item.addEventListener('dragstart', e => {
                    e.dataTransfer.setData('item-id', item.dataset.id || item.dataset.itemId);
                    e.dataTransfer.setData('category', item.dataset.category || '');
                });
            });

            document.querySelectorAll('.avatar-layer').forEach(layer => {
                layer.addEventListener('dragover', e => e.preventDefault());
                layer.addEventListener('drop', handleDrop);
            });
        }

        function handleDrop(e) {
            e.preventDefault();
            const itemId = e.dataTransfer.getData('item-id');
            const category = e.dataTransfer.getData('category');

            if (!itemId) return;

            const currentLayer = document.getElementById(`layer-${category}`);
            if (currentLayer) lastEquipped[category] = currentLayer.src;

            const validItemIds = ['item1', 'item2', 'item3']; // Example allow-list
            if (!validItemIds.includes(itemId)) {
                console.error(`Invalid itemId: ${itemId}`);
                return;
            }

            fetch("{% url 'dressup:equip_item' 0 %}".replace('0', itemId))

                .then(res => {
                    if (!res.ok) throw new Error(`Server error: ${res.status}`);
                    return res.json();
                })
                .then(data => {
                    if (data.category && data.image_url) {
                        const layerImg = document.getElementById(`layer-${data.category}`);
                        if (layerImg && layerImg.src !== data.image_url) {
                            layerImg.src = data.image_url;
                            sparkleEffect(layerImg);
                        }
                    }
                })
                .catch(error => console.error('Error fetching item data:', error));
        }

        function sparkleEffect(target) {
            const sparkle = document.createElement('div');
            sparkle.className = 'sparkle-effect';
            sparkle.style.position = 'absolute';
            sparkle.style.inset = '0';
            sparkle.style.pointerEvents = 'none';
            sparkle.style.animation = 'sparkle 0.6s ease-out';
            sparkle.style.background = 'radial-gradient(circle, rgba(255,255,255,0.6), transparent 70%)';
            sparkle.style.zIndex = '99';
            target.parentElement.appendChild(sparkle);
            setTimeout(() => sparkle.remove(), 600);
        }

        function setupUndoButton() {
            const undoBtn = document.getElementById('undo-btn');
            if (undoBtn) {
                undoBtn.addEventListener('click', () => {
                    for (const category in lastEquipped) {
                        const layer = document.getElementById(`layer-${category}`);
                        if (layer) layer.src = lastEquipped[category];
                    }
                    lastEquipped = {};
                });
            }
        }

        return { init };
    })();
}
