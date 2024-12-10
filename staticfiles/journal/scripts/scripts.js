// Utility: Get CSRF Token from Cookie
function getCSRFToken() {
    const name = 'csrftoken=';
    const decodedCookie = decodeURIComponent(document.cookie);
    const cookies = decodedCookie.split(';');
    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name)) {
            return cookie.substring(name.length);
        }
    }
    return '';
}

// Utility: Fetch with CSRF Token
function fetchWithCSRF(url, options = {}) {
    const headers = options.headers || {};
    headers['X-CSRFToken'] = getCSRFToken();
    headers['Content-Type'] = headers['Content-Type'] || 'application/json';
    return fetch(url, { ...options, headers });
}

// Utility: Handle Fetch Errors
function handleFetchError(response) {
    if (!response.ok) {
        return response.json().catch(() => {
            throw new Error('An error occurred');
        }).then(errData => {
            throw new Error(errData.message || 'An error occurred');
        });
    }
    return response.json();
}

// Utility: Show Toast Notifications
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerText = message;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.classList.add('fade-out');
        toast.addEventListener('transitionend', () => toast.remove());
    }, 3000);
}

// Panic Mode Toggle with Local Storage
function togglePanicMode() {
    document.body.classList.toggle('neutral-theme');
    if (document.body.classList.contains('neutral-theme')) {
        localStorage.setItem('theme', 'neutral');
    } else {
        localStorage.removeItem('theme');
    }
}

// On Page Load, Check Local Storage and Initialize Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Apply Neutral Theme if Set
    if (localStorage.getItem('theme') === 'neutral') {
        document.body.classList.add('neutral-theme');
    }

    // Initialize Panic Button
    const panicButton = document.querySelector('.panic-button');
    if (panicButton) {
        panicButton.addEventListener('click', togglePanicMode);
    }

    // Initialize Generate Task Button
    document.getElementById('generate-task')?.addEventListener('click', generateTask);

    // Initialize Complete Task Button
    document.getElementById('complete-task')?.addEventListener('click', function () {
        completeTask(this.dataset.taskId);
    });

    // Initialize Fail Task Button
    document.getElementById('fail-task')?.addEventListener('click', function () {
        failTask(this.dataset.taskId);
    });

    // Initialize To-Do Checkboxes
    document.addEventListener('change', function (e) {
        if (e.target.classList.contains('todo-checkbox')) {
            if (e.target.checked) {
                completeTodoItem(e.target.dataset.id);
            }
        }
    });
});

/**
/**
 * Increment the habit counter via AJAX.
 * @param {number} habitId - The ID of the habit to increment.
 */
function incrementHabit(habitId) {
    fetchWithCSRF(`/journal/habits/${habitId}/increment/`, {
        method: 'POST',
        body: JSON.stringify({}),
    })
        .then(handleFetchError)
        .then(data => {
            if (data.status === 'success') {
                // Update the counter
                const habitCountElement = document.getElementById(`habit-count-${habitId}`);
                if (habitCountElement) {
                    habitCountElement.textContent = data.new_count; // Update count dynamically
                }

                // Update the icons (hearts)
                const iconsContainer = document.getElementById(`icons-${habitId}`);
                if (iconsContainer) {
                    // Clear existing hearts and add new ones
                    iconsContainer.innerHTML = '';
                    for (let i = 0; i < data.new_count; i++) {
                        const heartIcon = document.createElement('span');
                        heartIcon.className = 'icon';
                        heartIcon.textContent = '❤️';
                        iconsContainer.appendChild(heartIcon);
                    }
                }

                // Update the insights (if available)
                const insightElement = document.getElementById(`insight-${habitId}`);
                if (insightElement) {
                    insightElement.textContent = data.insight || ''; // Update insight text dynamically
                }

                // Show success toast
                showToast('Habit counter incremented!', 'success');
            } else {
                // Handle failure case
                showToast(data.message || 'Failed to increment habit counter.', 'error');
            }
        })
        .catch(error => {
            console.error('Error incrementing habit counter:', error);
            showToast(error.message || 'Error incrementing habit counter.', 'error');
        });
}

/**
 * Generate a new task via AJAX.
 */
function generateTask() {
    fetchWithCSRF('/journal/generate-task/', {
        method: 'POST',
        body: JSON.stringify({}),
    })
        .then(handleFetchError)
        .then(data => {
            const taskResult = document.getElementById('task-result');
            if (taskResult && data.task) {
                taskResult.innerHTML = `<s>${data.task}</s>`;
            }
            showToast('New task generated! 💖', 'success');
        })
        .catch(error => {
            console.error('Error generating task:', error);
            showToast(error.message || 'Error generating task.', 'error');
        });
}

/**
 * Complete a task and redirect to a new journal entry.
 * @param {number} taskId - The ID of the task to complete.
 */
function completeTask(taskId) {
    fetchWithCSRF(`/journal/get-task-prompt/${taskId}/`, {
        method: 'GET',
    })
        .then(handleFetchError)
        .then(data => {
            if (data.status === 'success' && data.task_prompt) {
                window.location.href = `/journal/new-entry/?prompt=${encodeURIComponent(data.task_prompt)}`;
            } else {
                showToast('Error retrieving task prompt.', 'error');
            }
        })
        .catch(error => {
            console.error('Error retrieving task prompt:', error);
            showToast(error.message || 'Error retrieving task prompt.', 'error');
        });
}

/**
 * Fail a task and deduct points.
 * @param {number} taskId - The ID of the task to fail.
 */
function failTask(taskId) {
    fetchWithCSRF('/journal/fail-task/', {
        method: 'POST',
        body: JSON.stringify({
            task_id: taskId,
            penaltyType: 'DEDUCT_POINTS',
            pointsToDeduct: 10,
        }),
    })
        .then(handleFetchError)
        .then(data => {
            if (data.status === 'success') {
                const pointsDisplay = document.getElementById('points-display');
                if (pointsDisplay) {
                    pointsDisplay.innerText = `Points: ${data.new_points}`;
                }
                showToast('Points deducted.', 'success');
            } else {
                showToast(data.message || 'Failed to deduct points.', 'error');
            }
        })
        .catch(error => {
            console.error('Error failing task:', error);
            showToast(error.message || 'Error failing task.', 'error');
        });
}

/**
 * Complete a to-do item via AJAX.
 * @param {number} todoId - The ID of the to-do item to complete.
 */
function completeTodoItem(todoId) {
    fetchWithCSRF(`/journal/complete-todo/${todoId}/`, {
        method: 'POST',
        body: JSON.stringify({ todo_id: todoId }),
    })
        .then(handleFetchError)
        .then(data => {
            if (data.status === 'success') {
                const todoItem = document.getElementById(`todo-${todoId}`);
                if (todoItem) {
                    todoItem.classList.add('completed');
                    setTimeout(() => {
                        todoItem.remove();
                    }, 2000);
                }
                showToast('To-Do item completed!', 'success');
            } else {
                showToast(data.message || 'Failed to complete To-Do item.', 'error');
            }
        })
        .catch(error => {
            console.error('Error completing To-Do item:', error);
            showToast(error.message || 'Error completing To-Do item.', 'error');
        });
}


fetch('/path/to/customize-avatar/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrftoken,  // Add CSRF token
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
});
