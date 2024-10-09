// static/js/scripts.js

// Function to get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (const cookie of cookies) {
            const trimmedCookie = cookie.trim();
            if (trimmedCookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(trimmedCookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to show toast notifications
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) return; // Exit if no toast container found

    const toast = document.createElement('div');
    toast.classList.add('toast', `toast-${type}`);
    toast.textContent = message;
    toastContainer.appendChild(toast);

    // Automatically remove the toast after 3 seconds
    setTimeout(() => {
        toastContainer.removeChild(toast);
    }, 3000);
}

// Function to increment habit counter via AJAX
function incrementHabitCounter(habitId) {
    fetch(`/habits/${habitId}/increment/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({})
    })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                const habitCount = document.getElementById(`habit-count-${habitId}`);
                if (habitCount) habitCount.innerText = data.new_count;

                const insightContainer = document.getElementById(`insight-${habitId}`);
                if (insightContainer && data.insight) insightContainer.innerText = data.insight;

                showToast('Habit counter incremented!', 'success');
            } else {
                showToast(data.message || 'Failed to increment habit counter.', 'error');
            }
        })
        .catch(error => {
            console.error('Error incrementing habit counter:', error);
            showToast("Error incrementing habit counter: " + error.message, 'error');
        });
}

// Function to generate a new task via AJAX
function generateTask() {
    fetch('/journal/generate-task/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({})
    })
        .then(response => response.json())
        .then(data => {
            const taskResult = document.getElementById('task-result');
            if (taskResult && data.task) {
                taskResult.innerHTML = `<s>${data.task}</s>`;
            }
            showToast("New task generated! 💖", 'success');
        })
        .catch(error => {
            console.error('Error generating task:', error);
            showToast("Error generating task.", 'error');
        });
}

// Function to complete a task by fetching its prompt and redirecting
function completeTask(taskId) {
    fetch(`/journal/get-task-prompt/${taskId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success' && data.task_prompt) {
                window.location.href = `/journal/new-entry/?prompt=${encodeURIComponent(data.task_prompt)}`;
            } else {
                alert('Error retrieving task prompt: ' + (data.message || 'Unknown error.'));
            }
        })
        .catch(error => {
            console.error('Error retrieving task prompt:', error);
            alert("Error retrieving task prompt.");
        });
}

// Function to fail a task and apply penalties via AJAX
function failTask(taskId) {
    fetch('/journal/fail-task/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            task_id: taskId,
            penaltyType: 'DEDUCT_POINTS',
            pointsToDeduct: 10
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const pointsDisplay = document.getElementById('points-display');
                if (pointsDisplay && typeof data.new_points !== 'undefined') {
                    pointsDisplay.innerText = `Points: ${data.new_points}`;
                }
                showToast("Points deducted.", 'success');
            } else {
                showToast(data.message || 'Failed to deduct points.', 'error');
            }
        })
        .catch(error => {
            console.error('Error failing task:', error);
            showToast("Error failing task.", 'error');
        });
}

// Function to complete a To-Do item via AJAX
function completeTodoItem(todoId) {
    fetch(`/journal/complete-todo/${todoId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ todo_id: todoId })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const todoItem = document.getElementById(`todo-${todoId}`);
                if (todoItem) {
                    todoItem.classList.add('completed');
                    setTimeout(() => {
                        todoItem.style.display = 'none';
                    }, 1000);
                }
                showToast("To-Do item completed!", 'success');
            } else {
                showToast(data.message || 'Failed to complete To-Do item.', 'error');
            }
        })
        .catch(error => {
            console.error('Error completing To-Do item:', error);
            showToast("Error completing To-Do item.", 'error');
        });
}

// Function to toggle panic mode
function togglePanicMode() {
    const body = document.body;
    const panicButton = document.querySelector('.panic-button');
    const isNeutral = body.classList.toggle('neutral');

    if (panicButton) {
        panicButton.classList.toggle('panic-active', isNeutral);
    }

    document.querySelectorAll('.card').forEach(card => {
        card.classList.toggle('neutral', isNeutral);
    });

    document.querySelectorAll('img').forEach(image => {
        image.style.filter = isNeutral ? 'blur(5px)' : 'none';
    });
}

// Event delegation for incrementing habits
document.addEventListener('click', function (event) {
    if (event.target.classList.contains('increment-btn')) {
        event.preventDefault();
        const habitId = event.target.dataset.habitId;
        if (habitId) {
            incrementHabitCounter(habitId);
        }
    }
});

// Event listener for generating a new task
document.addEventListener('DOMContentLoaded', () => {
    const generateTaskBtn = document.getElementById('generate-task');
    if (generateTaskBtn) {
        generateTaskBtn.addEventListener('click', generateTask);
    }

    const completeTaskBtn = document.getElementById('complete-task');
    if (completeTaskBtn) {
        completeTaskBtn.addEventListener('click', function () {
            const taskId = this.dataset.taskId;
            if (taskId) {
                completeTask(taskId);
            }
        });
    }

    const failTaskBtn = document.getElementById('fail-task');
    if (failTaskBtn) {
        failTaskBtn.addEventListener('click', function () {
            const taskId = this.dataset.taskId;
            if (taskId) {
                failTask(taskId);
            }
        });
    }

    // Event listeners for To-Do checkboxes
    document.querySelectorAll('.todo-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const todoId = this.getAttribute('data-id');
            if (this.checked && todoId) {
                completeTodoItem(todoId);
            }
        });
    });

    // Event listener for panic mode toggle button
    const panicModeBtn = document.querySelector('.panic-button');
    if (panicModeBtn) {
        panicModeBtn.addEventListener('click', togglePanicMode);
    }

    // Avatar customization: Drag-and-Drop and Touch Events
    const clothingItems = document.querySelectorAll('.clothing-item');
    const avatarArea = document.getElementById('avatar-area');
    const resetButton = document.getElementById('reset-button');

    // Drag and Drop for Desktop
    if (avatarArea && clothingItems.length > 0) {
        clothingItems.forEach(item => {
            item.addEventListener('dragstart', dragStart);
            item.addEventListener('dragend', dragEnd);
        });

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
    if (resetButton && clothingItems.length > 0) {
        resetButton.addEventListener('click', () => {
            const clothingPool = document.getElementById('clothing-pool');
            if (clothingPool) {
                clothingItems.forEach(item => {
                    clothingPool.appendChild(item);
                });
            }
            showToast("Avatar reset to default.", 'info');
        });
    }
});

// Drag and Drop event handlers
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
    }
}

// Touch event handlers for mobile
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
        if (avatarArea) {
            avatarArea.appendChild(target);
        }
        target.classList.remove('dragging');
        target.style.position = 'static';
    } else {
        target.classList.remove('dragging');
        target.style.position = 'static';
    }
}
