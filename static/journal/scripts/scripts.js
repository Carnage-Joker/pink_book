// scripts.js

// scripts.js

// Function to fetch and display the prompt
function generatePrompt() {
    fetch('/generate-prompt/')
        .then(response => {
            if (!response.ok) {
                // If the response status is not OK, throw an error
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            // Check if the prompt key exists in the returned data
            if (data.prompt) {
                document.getElementById('generatedText').innerText = data.prompt;
            } else {
                document.getElementById('generatedText').innerText = "Error generating prompt.";
            }
        })
        .catch(error => {
            // Log and display the error message
            console.error('Error generating prompt:', error);
            document.getElementById('generatedText').innerText = "Failed to fetch prompt. Please try again later.";
        });
}

// Attach event listener to the "Generate New Prompt" button
document.getElementById('generatePrompt').addEventListener('click', generatePrompt);

// scripts.js

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

// Attach event listener to the "Get Insight" button
document.getElementById('getInsight').addEventListener('click', generateInsight);
