import { fetchUtils } from "./fetch_utils.js";

async function incrementHabit(habitId) {
    try {
        const habitCounter = document.getElementById(`habit-count-${habitId}`);
        const iconsContainer = document.getElementById(`icons-${habitId}`);

        // Optimistic UI update before API response
        if (habitCounter) {
            habitCounter.textContent = parseInt(habitCounter.textContent) + 1;
        }

        const response = await fetchUtils.fetchWithCSRF(`/journal/habits/${habitId}/increment/`, {
            method: "POST",
        });

        if (!response.ok) {
            let errorMessage = `HTTP error! status: ${response.status}`;
            try {
                const errorData = await response.json();
                errorMessage = errorData.error || errorMessage;
            } catch {
                const errorText = await response.text();
                errorMessage = errorText || errorMessage;
            }
            throw new Error(errorMessage);
        }

        const data = await response.json();
        console.log("Habit incremented successfully:", data);

        // Update UI dynamically
        if (habitCounter) {
            habitCounter.textContent = data.new_count;
        }

        if (iconsContainer) {
            iconsContainer.innerHTML = "";
            for (let i = 0; i < data.new_count; i++) {
                const heartIcon = document.createElement("span");
                heartIcon.className = "icon";
                heartIcon.textContent = "❤️";
                iconsContainer.appendChild(heartIcon);
            }
        }

        showToast("Habit incremented!", "success");
        return data;
    } catch (error) {
        console.error("Error incrementing habit counter:", error);
        showToast(error.message || "Error incrementing habit counter.", "error");
        throw error;
    }
}

// Ensure global access
window.incrementHabit = incrementHabit;
