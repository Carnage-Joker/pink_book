// Utility: Get CSRF Token from Cookie
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') return decodeURIComponent(value);
    }
    return null;
}

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

// Habit: Increment Counter via AJAX
function incrementHabitCounter(habitId) {
    fetch(`/journal/habits/${habitId}/increment/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({}),
    })
        .then(response => response.ok ? response.json() : Promise.reject(response))
        .then(data => {
            if (data.status === 'success') {
                document.getElementById(`habit-count-${habitId}`).textContent = data.new_count;
                document.getElementById(`insight-${habitId}`).textContent = data.insight || '';
                showToast('Habit counter incremented!', 'success');
            } else {
                showToast(data.message || 'Failed to increment habit counter.', 'error');
            }
        })
        .catch(error => {
            console.error('Error incrementing habit counter:', error);
            showToast('Error incrementing habit counter.', 'error');
        });
}

// Task: Generate New Task via AJAX
function generateTask() {
    fetch('/journal/generate-task/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({}),
    })
        .then(response => response.ok ? response.json() : Promise.reject(response))
        .then(data => {
            const taskResult = document.getElementById('task-result');
            if (taskResult && data.task) {
                taskResult.innerHTML = `<s>${data.task}</s>`;
            }
            showToast('New task generated! 💖', 'success');
        })
        .catch(error => {
            console.error('Error generating task:', error);
            showToast('Error generating task.', 'error');
        });
}

// Task: Complete a Task and Redirect to New Journal Entry
function completeTask(taskId) {
    fetch(`/journal/get-task-prompt/${taskId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
    })
        .then(response => response.ok ? response.json() : Promise.reject(response))
        .then(data => {
            if (data.status === 'success' && data.task_prompt) {
                window.location.href = `/journal/new-entry/?prompt=${encodeURIComponent(data.task_prompt)}`;
            } else {
                showToast('Error retrieving task prompt.', 'error');
            }
        })
        .catch(error => {
            console.error('Error retrieving task prompt:', error);
            showToast('Error retrieving task prompt.', 'error');
        });
}

// Task: Fail Task and Deduct Points
function failTask(taskId) {
    fetch('/journal/fail-task/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({
            task_id: taskId,
            penaltyType: 'DEDUCT_POINTS',
            pointsToDeduct: 10,
        }),
    })
        .then(response => response.ok ? response.json() : Promise.reject(response))
        .then(data => {
            if (data.status === 'success') {
                const pointsDisplay = document.getElementById('points-display');
                if (pointsDisplay) pointsDisplay.innerText = `Points: ${data.new_points}`;
                showToast('Points deducted.', 'success');
            } else {
                showToast(data.message || 'Failed to deduct points.', 'error');
            }
        })
        .catch(error => {
            console.error('Error failing task:', error);
            showToast('Error failing task.', 'error');
        });
}

// To-Do: Complete via AJAX
function completeTodoItem(todoId) {
    fetch(`/journal/complete-todo/${todoId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ todo_id: todoId }),
    })
        .then(response => response.ok ? response.json() : Promise.reject(response))
        .then(data => {
            if (data.status === 'success') {
                const todoItem = document.getElementById(`todo-${todoId}`);
                if (todoItem) {
                    todoItem.classList.add('completed');
                    setTimeout(() => todoItem.style.display = 'none', 1000);
                }
                showToast('To-Do item completed!', 'success');
            } else {
                showToast(data.message || 'Failed to complete To-Do item.', 'error');
            }
        })
        .catch(error => {
            console.error('Error completing To-Do item:', error);
            showToast('Error completing To-Do item.', 'error');
        });
}

// Panic Mode Toggle
function togglePanicMode() {
    document.body.classList.toggle('neutral');
    document.querySelectorAll('.card, img').forEach(element => {
        element.classList.toggle('neutral');
        element.style.filter = element.style.filter === 'blur(5px)' ? 'none' : 'blur(5px)';
    });
}

// Initialize Event Listeners on DOM Load
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('generate-task')?.addEventListener('click', generateTask);
    document.getElementById('complete-task')?.addEventListener('click', function () {
        completeTask(this.dataset.taskId);
    });
    document.getElementById('fail-task')?.addEventListener('click', function () {
        failTask(this.dataset.taskId);
    });

    document.querySelectorAll('.todo-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            if (this.checked) completeTodoItem(this.dataset.id);
        });
    });

    document.querySelector('.panic-button')?.addEventListener('click', togglePanicMode);
});
