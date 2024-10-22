// Utility: Show Toast Notifications
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) return;

    const toast = document.createElement('div');
    toast.classList.add('toast', `toast-${type}`);
    toast.textContent = message;
    toastContainer.appendChild(toast);

    setTimeout(() => toastContainer.removeChild(toast), 3000);
}

// Drag-and-Drop for Desktop
function dragStart(event) {
    event.dataTransfer.setData('text/plain', event.target.id);
    event.target.classList.add('dragging');
}

function dragEnd(event) {
    event.target.classList.remove('dragging');
}

function dragOver(event) {
    event.preventDefault();
}

function drop(event) {
    event.preventDefault();
    const id = event.dataTransfer.getData('text/plain');
    const draggable = document.getElementById(id);
    const avatarArea = document.getElementById('avatar-area');

    if (draggable && avatarArea) {
        avatarArea.appendChild(draggable);
        showToast("Item placed on avatar!", 'success');
    }
}

// Touch events for mobile
function touchStart(event) {
    const touch = event.targetTouches[0];
    const target = event.target;
    target.style.position = 'absolute';
    target.style.left = `${touch.pageX - 50}px`;
    target.style.top = `${touch.pageY - 50}px`;
    target.classList.add('dragging');
}

function touchMove(event) {
    const touch = event.targetTouches[0];
    const target = event.target;
    event.preventDefault(); // Prevent scrolling
    target.style.left = `${touch.pageX - 50}px`;
    target.style.top = `${touch.pageY - 50}px`;
}

function touchEnd(event) {
    const target = event.target;
    const avatarArea = document.getElementById('avatar-area');
    const avatarRect = avatarArea ? avatarArea.getBoundingClientRect() : null;
    const elementRect = target.getBoundingClientRect();

    if (
        avatarRect &&
        elementRect.left > avatarRect.left &&
        elementRect.right < avatarRect.right &&
        elementRect.top > avatarRect.top &&
        elementRect.bottom < avatarRect.bottom
    ) {
        avatarArea.appendChild(target);
        showToast("Item placed on avatar!", 'success');
    }
    target.classList.remove('dragging');
    target.style.position = 'static';
}

// Reset Avatar to Default
function resetAvatar() {
    const clothingPool = document.getElementById('clothing-pool');
    const clothingItems = document.querySelectorAll('.clothing-item');

    if (clothingPool && clothingItems.length > 0) {
        clothingItems.forEach(item => {
            clothingPool.appendChild(item);
        });
        showToast("Avatar reset to default.", 'info');
    }
}

// Initialize Event Listeners for Drag-and-Drop and Touch Events
document.addEventListener('DOMContentLoaded', () => {
    const clothingItems = document.querySelectorAll('.clothing-item');
    const avatarArea = document.getElementById('avatar-area');
    const resetButton = document.getElementById('reset-button');

    // Drag-and-Drop for Desktop
    clothingItems.forEach(item => {
        item.addEventListener('dragstart', dragStart);
        item.addEventListener('dragend', dragEnd);
    });

    if (avatarArea) {
        avatarArea.addEventListener('dragover', dragOver);
        avatarArea.addEventListener('drop', drop);
    }

    // Touch Events for Mobile
    clothingItems.forEach(item => {
        item.addEventListener('touchstart', touchStart);
        item.addEventListener('touchmove', touchMove);
        item.addEventListener('touchend', touchEnd);
    });

    // Reset Avatar Button
    if (resetButton) {
        resetButton.addEventListener('click', resetAvatar);
    }
});
