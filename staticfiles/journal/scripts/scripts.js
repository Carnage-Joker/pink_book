// Toast Notification System
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

function showReward(element) {
    const sticker = document.createElement('img');
    sticker.src = '/static/journal/media/sticker.png';
    sticker.alt = 'Digital Sticker';
    element.appendChild(sticker);
    showToast("You've earned a cute digital sticker! 🌟", 'success');
}

function showAlert(message) {
    showToast(message, 'error');
}

document.addEventListener('DOMContentLoaded', function () {
    const submitProgressButton = document.getElementById('submitProgress');
    if (submitProgressButton) {
        submitProgressButton.addEventListener('click', function () {
            const todoId = getTodoId(); // You'll need to get the todoId relevant to this action
            const newProgress = document.getElementById('progressSlider').value;
            showToast(`Progress for ToDo ID ${todoId} updated to ${newProgress}%!`, 'success');
        });
    }
});

function getTodoId() {
    // Add code here to retrieve the relevant todoId
    return '123'; // Replace '123' with the actual todoId
}

function giveReward(rewardType) {
    let message = '';
    switch (rewardType) {
        case 'sticker':
            message = "You've earned a cute digital sticker! 🌟";
            break;
        case 'unlock_content':
            message = "Yay! You've unlocked new sissy content! 🎀";
            break;
    }
    showToast(message, 'success');
}

function givePenalty(penaltyType) {
    let message = '';
    switch (penaltyType) {
        case 'reminder':
            message = "Don't forget your sissy duties, darling! 💖";
            break;
        case 'lock_content':
            message = "Oops! Some content has been locked. 😢";
            break;
    }
    showToast(message, 'warning');
}

// Function to fetch and display a prompt
// Toast Notification System and other utility functions ...

// Function to fetch and display a prompt
// Toast Notification System and other utility functions ...

// Function to fetch and display a prompt
function generatePrompt() {
    const generatedTextDiv = document.getElementById('generatedText');
    if (!generatedTextDiv) {
        console.error('Generated text div not found!');
        return;
    }

    const promptMessage = "Write a cute and bubbly journal prompt for a sissy to write about. The prompt should encourage them to express their inner femininity, embrace their playful and girly side, and reflect on their journey of becoming the ultimate sissy. Include lots of girly details, sparkles, and positive affirmations!";

    // Fetch the AI-generated prompt
    fetch('http://127.0.0.1:5000/generate', { // Ensure this URL matches your Flask API endpoint
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: promptMessage })  // Sending the predefined prompt to the AI
    })
        .then(response => response.json())
        .then(data => {
            // Only display the AI-generated text, not the prompt itself
            generatedTextDiv.innerText = data.generated_text;
        })
        .catch(error => console.error('Error generating prompt:', error));
}

// Function to fetch and display an insight
function generateInsight() {
    const entry = document.getElementById('id_content').value;
    if (entry.trim() === "") {
        document.getElementById('insightOutput').innerText = "Please enter a diary entry.";
        return;
    }
    fetch('https://siss-prom-gen.herokuapp.com/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: entry }) // Use the journal entry as the prompt
    })
        .then(response => response.json())
        .then(data => {
            const insight = data.generated_text;
            document.getElementById('insightOutput').innerText = insight;
            document.getElementById('id_insight').value = insight; // Update hidden field
            showToast("Insight generated successfully!", 'success');
        })
        .catch(error => {
            console.error('Error generating insight:', error);
            showToast("Error generating insight. Please try again.", 'error');
        });
}

// Event listeners for generating prompt and insight
document.addEventListener('DOMContentLoaded', function () {
    const generatePromptButton = document.getElementById('generatePrompt');
    const generateInsightButton = document.getElementById('generateInsight');

    if (generatePromptButton) {
        generatePromptButton.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent the default form submission
            generatePrompt(); // Generate a new prompt on button click
        });
    } else {
        console.error('Generate Prompt button not found!');
    }

    if (generateInsightButton) {
        generateInsightButton.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent the default form submission
            generateInsight(); // Generate insight on button click
        });
    } else {
        console.error('Generate Insight button not found!');
    }

    // Generate the initial prompt on page load
    generatePrompt();
});

    if (generateInsightButton) {
        generateInsightButton.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent the default form submission
            generateInsight(); // Generate insight on button click
        });
    } else {
        console.error('Generate Insight button not found!');
    }

    // Generate the initial prompt on page load
    generatePrompt();


// Function to fetch and display an insight
function generateInsight() {
    const entry = document.getElementById('id_content').value;
    if (entry.trim() === "") {
        document.getElementById('insightOutput').innerText = "Please enter a diary entry.";
        return;
    }
    fetch('https://siss-prom-gen.herokuapp.com/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: entry }) // Use the journal entry as the prompt
    })
        .then(response => response.json())
        .then(data => {
            const insight = data.generated_text;
            document.getElementById('insightOutput').innerText = insight;
            document.getElementById('id_insight').value = insight; // Update hidden field
            showToast("Insight generated successfully!", 'success');
        })
        .catch(error => {
            console.error('Error generating insight:', error);
            showToast("Error generating insight. Please try again.", 'error');
        });
}

// Event listeners for generating prompt and insight
document.addEventListener('DOMContentLoaded', function () {
    const generatePromptButton = document.getElementById('generatePrompt');
    const generateInsightButton = document.getElementById('generateInsight');

    if (generatePromptButton) {
        generatePromptButton.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent the default form submission
            generatePrompt(); // Generate a new prompt on button click
        });
    } else {
        console.error('Generate Prompt button not found!');
    }

    if (generateInsightButton) {
        generateInsightButton.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent the default form submission
            generateInsight(); // Generate insight on button click
        });
    } else {
        console.error('Generate Insight button not found!');
    }

    // Generate the initial prompt on page load
    generatePrompt();
});
