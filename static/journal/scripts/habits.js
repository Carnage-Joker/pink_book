import e from express;
import { fetchUtils } from "./fetch_utils.js";

const HABIT_INCREMENT_URL = "/journal/habits/";

async function incrementHabit(habitId) {
    try {
        const habitCounter = document.getElementById(`habit-count-${habitId}`);
        const iconsContainer = document.getElementById(`icons-${habitId}`);

        // Optimistic UI update before API response
        if (habitCounter) {
            habitCounter.textContent = parseInt(habitCounter.textContent, 10) + 1;
        }

        const response = await fetchUtils.fetchWithCSRF(`${HABIT_INCREMENT_URL}${habitId}/increment/`, {
            method: "POST",
        });

        if (!response.ok) {
            let errorMessage = `HTTP error! status: ${response.status}`;
            try {
                const errorData = await response.clone().json();
                errorMessage = errorData.error || errorMessage;
            } catch {
                const errorText = await response.text();
                errorMessage = errorText || errorMessage;
            }
            throw new Error(errorMessage);
        }

        const data = await response.clone().json();
        // Update UI dynamically
        if (habitCounter) {
            habitCounter.textContent = data.new_count;
        }

        if (iconsContainer) {
            iconsContainer.innerHTML = "";
            const fragment = document.createDocumentFragment();
            for (let i = 0; i < data.new_count; i++) {
                const heartIcon = document.createElement("span");
                heartIcon.className = "icon";
                heartIcon.textContent = "❤️";
                fragment.appendChild(heartIcon);
            }
            iconsContainer.appendChild(fragment);
        showToast(`Habit ${habitId} incremented successfully!`, "success");

        return data;
    } catch (error) {
        console.error("Error incrementing habit counter:", error);
        showToast(`Error incrementing habit counter: ${error.message}`, "error");
        throw error;
    }
}

// Ensure global access
window.incrementHabit = incrementHabit;
export { incrementHabit };
async function decrementHabit(habitId) {
    try {
        const response = await fetchUtils.fetchWithCSRF(`/api/habits/${habitId}/decrement`, {
            method: "POST",
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Failed to decrement habit.");
                }
        const data = await response.json();
        showToast("Habit decremented successfully!", "success");
        return data;
    } catch (error) {
        console.error("Error decrementing habit:", error);
        showToast(error.message || "Error decrementing habit.", "error");
        throw error;
    }
}

// Ensure global access
(window as any).decrementHabit = decrementHabit;
async function deleteHabit(habitId) {
    try {
        const response = await fetchUtils.fetchWithCSRF(`/api/habits/${habitId}/delete`, {
            method: "DELETE",
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Failed to delete habit.");
        }
        const data = await response.json();
        showToast("Habit deleted successfully!", "success");
        return data;
    } catch (error) {
        console.error("Error deleting habit:", error);
        showToast(error.message || "Error deleting habit.", "error");
        throw error;
    }
}
}

// Ensure global access
window.deleteHabit = deleteHabit;
// Ensure global access
(window as any).deleteHabit = deleteHabit;
export { deleteHabit };
