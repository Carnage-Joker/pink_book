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
                const generatedText = document.getElementById('generatedText');
                if (generatedText) {
                    generatedText.innerText = data.prompt ? data.prompt : "Error generating prompt.";
                }
            })
            .catch(error => {
                console.error('Error generating prompt:', error);
                const generatedText = document.getElementById('generatedText');
                if (generatedText) {
                    generatedText.innerText = "Failed to fetch prompt. Please try again later.";
                }
            });
    }

    // Function to fetch and display the insight
    function generateInsight() {
        const content = document.getElementById('entryContent') ? document.getElementById('entryContent').value : '';

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
                const insightOutput = document.getElementById('insightOutput');
                if (insightOutput) {
                    insightOutput.innerText = data.insight ? data.insight : "Error generating insight.";
                    if (data.insight) {
                        const insightInput = document.getElementById('id_insight');
                        if (insightInput) {
                            insightInput.value = data.insight;
                        }
                    }
                }
            })
            .catch(error => {
                console.error('Error generating insight:', error);
                const insightOutput = document.getElementById('insightOutput');
                if (insightOutput) {
                    insightOutput.innerText = "Failed to fetch insight. Please try again later.";
                }
            });
    }

    // Attach event listeners
    const generatePromptButton = document.getElementById('generatePrompt');
    if (generatePromptButton) {
        generatePromptButton.addEventListener('click', generatePrompt);
    }

    const getInsightButton = document.getElementById('getInsight');
    if (getInsightButton) {
        getInsightButton.addEventListener('click', generateInsight);
    }

    const generateTaskButton = document.getElementById('generate-task');
    if (generateTaskButton) {
        generateTaskButton.addEventListener('click', function () {
            fetch('/journal/generate-task/')
                .then(response => response.json())
                .then(data => {
                    const taskResult = document.getElementById('task-result');
                    if (taskResult) {
                        taskResult.innerHTML = data.task;
                    }
                    showToast("New task generated! 💖", 'success');
                })
                .catch(error => console.error('Error generating task:', error));
        });
    }

    const completeTaskButton = document.getElementById('complete-task');
    if (completeTaskButton) {
        completeTaskButton.addEventListener('click', function () {
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
                    const pointsDisplay = document.getElementById('points-display');
                    if (pointsDisplay) {
                        pointsDisplay.innerText = `Points: ${data.points}`;
                    }
                })
                .catch(error => console.error('Error completing task:', error));
        });
    }

    const failTaskButton = document.getElementById('fail-task');
    if (failTaskButton) {
        failTaskButton.addEventListener('click', function () {
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
                    if (todoItem) {
                        todoItem.classList.add('completed');
                        setTimeout(() => {
                            todoItem.style.display = 'none';
                        }, 1000); // Adjust the delay as needed
                    }
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
                    if (progressContainer) {
                        progressContainer.style.width = `${data.new_progress}%`;
                        showToast('Progress updated!', 'success');
                    }
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

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', function () {
            showToast('Navigating to ' + link.textContent, 'info');
        });
    });
});
