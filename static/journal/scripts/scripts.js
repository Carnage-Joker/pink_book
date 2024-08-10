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
            if (taskResult) {
                taskResult.innerHTML = `<s>${data.task}</s>`; // Cross out the generated task
            }
            showToast("New task generated! 💖", 'success');
        })
        .catch(error => {
            console.error('Error generating task:', error);
            showToast("Error generating task.", 'error');
        });
}

    function completeTask(taskId) {
        fetch(`/journal/get-task-prompt/${taskId}/`, {  // Fetch the task prompt
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Redirect to the new_entry.html with the task prompt
                    window.location.href = `/journal/new-entry/?prompt=${encodeURIComponent(data.task_prompt)}`;
                } else {
                    alert('Error retrieving task prompt: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error retrieving task prompt:', error);
            });
    }

    function failTask(taskId) {
        fetch('/journal/fail-task/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                task_id: taskId,
                penaltyType: 'DEDUCT_POINTS', // Example penalty type
                pointsToDeduct: 10 // Deduct 10 points
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Update the points display
                    document.getElementById('points-display').innerText = `Points: ${data.new_points}`;
                    showToast("Points deducted.", 'success');
                } else {
                    showToast(data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error failing task:', error);
                showToast("Error failing task.", 'error');
            });
    }

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
                    todoItem.classList.add('completed');
                    setTimeout(() => {
                        todoItem.style.display = 'none';
                    }, 1000);
                } else {
                    showToast(data.message, 'error');
                }
            })
            .catch(error => console.error('Error completing todo:', error));
    }


document.getElementById('generate-task').addEventListener('click', generateTask);
document.getElementById('complete-task').addEventListener('click', completeTask);
document.getElementById('fail-task').addEventListener('click', failTask);
document.querySelectorAll('.todo-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', function () {
        const todoId = this.getAttribute('data-id');
        if (this.checked) {
            completeTodoItem(todoId);
        }
    });
});
function incrementHabitCounter(habitId) {
    fetch(`/increment-habit-counter/${habitId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                const habitCount = document.getElementById(`habit-count-${habitId}`);
                habitCount.innerText = data.new_count;

                // Update insights
                const insightContainer = document.getElementById(`insight-${habitId}`);
                if (insightContainer) {
                    insightContainer.innerText = data.insight;
                }

                showToast('Habit counter incremented!', 'success');
            } else {
                showToast(data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error incrementing habit counter:', error);
            showToast("Error incrementing habit counter: " + error.message, 'error');
        });
}


    function showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.classList.add('toast', `toast-${type}`);
        toast.textContent = message;
        toastContainer.appendChild(toast);

        setTimeout(() => {
            toastContainer.removeChild(toast);
        }, 3000);
    }
    document.querySelectorAll('.habit-counter').forEach(counter => {
        counter.addEventListener('click', function () {
            const habitId = this.getAttribute('data-id');
            incrementHabitCounter(habitId);
        });
    });
