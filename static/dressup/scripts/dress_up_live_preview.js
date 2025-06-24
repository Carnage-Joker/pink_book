export const dressUpLivePreview = createLivePreview();

function createLivePreview() {
    return (() => {
        // Function to initialize the live preview functionality
        function initializeDragAndDrop() {
            // Set up event listeners for drag and drop functionality
            setupDragAndDrop();
        }

        // Function to set up drag and drop for items onto avatar layers
        function setupDragAndDrop() {
            // Iterate over all elements with the class 'item' to enable drag-and-drop functionality
            document.querySelectorAll('.item').forEach(item => {
                item.addEventListener('dragstart', e => {
                    e.dataTransfer.setData('item-id', item.dataset.id);
                });
            });
            // Iterate over all avatar layers to enable drop functionality for drag-and-drop items
            document.querySelectorAll('.avatar-layer').forEach(layer => {
                layer.addEventListener('dragover', e => e.preventDefault());
                layer.addEventListener('drop', e => {
                    e.preventDefault();
                    const itemId = e.dataTransfer.getData('item-id');
                    fetch(`/dressup/equip_item_ajax/${itemId}/`)
                        .then(res => {
                            if (!res.ok) {
                                throw new Error(`Server error: ${res.status}`);
                            }
                            return res.json();
                        })
                        .then(data => {
                            if (data.category && data.image_url) {
                                const layerImg = document.querySelector(`.avatar-layer.${data.category}`);
                                if (layerImg && layerImg.src !== data.image_url) {
                                    layerImg.src = data.image_url;
                                }
                            }
                        })
                        .catch(error => {
                            console.error('Error fetching item data:', error);
                        });
                });
            });
        }
        return { init: initializeDragAndDrop };
    })();
}
