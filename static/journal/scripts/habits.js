// ==============================
// Module: Habit Tracker
// ==============================
import { fetchUtils } from './fetch_utils.js';
import { uiHelpers } from './ui_helpers.js';

export const habits = (() => {
    function incrementHabit(habitId) {
        fetchUtils.fetchWithCSRF(`/journal/habits/${habitId}/increment/`, {
            method: 'POST',
            body: JSON.stringify({}),
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    document.getElementById(`habit-count-${habitId}`).textContent = data.new_count;
                    uiHelpers.showToast('Habit counter incremented!', 'success');
                } else {
                    uiHelpers.showToast('Failed to increment habit counter.', 'error');
                }
            })
            .catch(error => uiHelpers.showToast('Error incrementing habit counter.', 'error'));
    }

    return { incrementHabit };
})();
