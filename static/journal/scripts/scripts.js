document.addEventListener("DOMContentLoaded", function () {
    // Function to fetch and display the prompt
    function generatePrompt() {
        fetch('/generate-prompt/')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                if (data.prompt) {
                    document.getElementById('generatedText').innerText = data.prompt;
                } else {
                    document.getElementById('generatedText').innerText = "Error generating prompt.";
                }
            })
            .catch(error => {
                console.error('Error generating prompt:', error);
                document.getElementById('generatedText').innerText = "Failed to fetch prompt. Please try again later.";
            });
    }

    document.getElementById('generatePrompt').addEventListener('click', generatePrompt);

    // Function to fetch and display the insight
    function generateInsight() {
        const content = document.getElementById('entryContent').value;

        fetch('/generate-insight/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content: content })
        })
            .then(response => {
                const contentType = response.headers.get('content-type');
                if (!contentType || !contentType.includes('application/json')) {
                    throw new Error('Received non-JSON response: ' + contentType);
                }
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                if (data.insight) {
                    document.getElementById('insightOutput').innerText = data.insight;
                    document.getElementById('id_insight').value = data.insight;
                } else {
                    document.getElementById('insightOutput').innerText = "Error generating insight.";
                }
            })
            .catch(error => {
                console.error('Error generating insight:', error);
                document.getElementById('insightOutput').innerText = "Failed to fetch insight. Please try again later.";
            });
    }

    document.getElementById('getInsight').addEventListener('click', generateInsight);

    // Function to fetch and display the task
    document.getElementById('generate-task').addEventListener('click', function () {
        fetch('/journal/generate-task/')
            .then(response => response.json())
            .then(data => {
                document.getElementById('task-result').innerHTML = data.task;
                showToast("New task generated! 💖", 'success');
            })
            .catch(error => console.error('Error generating task:', error));
    });

    // Function to complete the task and update points
    document.getElementById('complete-task').addEventListener('click', function () {
        fetch('/journal/complete-task/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
            .then(response => response.json())
            .then(data => {
                showToast(data.message, 'success');
                document.getElementById('points-display').innerText = `Points: ${data.points}`;
            })
            .catch(error => console.error('Error completing task:', error));
    });

    // Function to handle failed task
    document.getElementById('fail-task').addEventListener('click', function () {
        fetch('/journal/fail-task/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: new URLSearchParams({
                penaltyType: 'LOCK_CONTENT', // or 'DEDUCT_POINTS'
                pointsToDeduct: 10, // if applicable
                contentName: 'Premium Article' // if applicable
            })
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                showToast(data.message, 'error');
            })
            .catch(error => console.error('Error handling failed task:', error));
    });

    // Function to get CSRF token
    function getCookie(name) {
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
    }

    // Function to show toast notifications
    function showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            console.error('Toast container not found!');
            return;
        }

        const toast = document.createElement('div');
        toast.classList.add('toast', `toast-${type}`);
        toast.textContent = message;

        toastContainer.appendChild(toast);

        setTimeout(() => {
            toastContainer.removeChild(toast);
        }, 3000);
    }

    // Function to handle todo checkbox change
    document.querySelectorAll('.todo-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const todoId = this.getAttribute('data-id');
            if (this.checked) {
                completeTodoItem(todoId);
            }
        });
    });

    function completeTodoItem(todoId) {
        fetch(`/journal/complete-todo/${todoId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const todoItem = document.getElementById(`todo-${todoId}`);
                    todoItem.classList.add('completed');
                    setTimeout(() => {
                        todoItem.style.display = 'none';
                    }, 1000); // Adjust the delay as needed
                } else {
                    showToast(data.message, 'error');
                }
            })
            .catch(error => console.error('Error completing todo:', error));
    }

    // Function to update habit progress
    function updateProgress(habitId) {
        fetch(`/update-habit-progress/${habitId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ progress: 100 }) // Example progress value
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const progressContainer = document.querySelector(`#habit-${habitId} .progress-container .progress-bar`);
                    progressContainer.style.width = `${data.new_progress}%`;
                    showToast('Progress updated!', 'success');
                } else {
                    showToast(data.message, 'error');
                }
            })
            .catch(error => console.error('Error updating progress:', error));
    }

    // Attach event listeners to habit update buttons
    document.querySelectorAll('.update-progress-button').forEach(button => {
        button.addEventListener('click', function () {
            const habitId = this.getAttribute('data-id');
            updateProgress(habitId);
        });
    });

    // CSS for completed todos
    const style = document.createElement('style');
    style.innerHTML = `
        .completed .todo-text {
            text-decoration: line-through;
        }
    `;
    document.head.appendChild(style);
});
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        console.error('Toast container not found!');
        return;
    }

    const toast = document.createElement('div');
    toast.classList.add('toast', `toast-${type}`);
    toast.textContent = message;

    toastContainer.appendChild(toast);

    setTimeout(() => {
        toastContainer.removeChild(toast);
    }, 3000);
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', function () {
            showToast('Navigating to ' + link.textContent, 'info');
        });
    });
});
