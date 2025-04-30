// ==============================
// Module: Task Management
// ==============================
import { fetchUtils } from './fetch_utils.js';
import { uiHelpers } from './ui_helpers.js';

export const tasks = (() => {
    async function generateTask() {
        try {
            const response = await fetchUtils.fetchWithCSRF('/journal/generate-task/', {
                method: 'POST',
                body: JSON.stringify({}),
            });
            const data = await response.json();
            const taskResult = document.getElementById('task-result');
            if (taskResult && data.task) {
                taskResult.innerHTML = `<s>${data.task}</s>`;
            }
            uiHelpers.showToast('New task generated! 💖', 'success');
        } catch (error) {
            console.error('Error generating task:', error);
            uiHelpers.showToast('Error generating task.', 'error');
        }
    }

    async function completeTask(taskId) {
        try {
            const response = await fetchUtils.fetchWithCSRF(`/journal/get-task-prompt/${taskId}/`, {
                method: 'GET',
            });
            const data = await response.json();
            if (data.status === 'success' && data.task_prompt) {
                window.location.href = `/journal/new-entry/?prompt=${encodeURIComponent(data.task_prompt)}`;
            } else {
                uiHelpers.showToast('Error retrieving task prompt.', 'error');
            }
        } catch (error) {
            console.error('Error retrieving task prompt:', error);
            uiHelpers.showToast('Error retrieving task prompt.', 'error');
        }
    }

    async function failTask(taskId) {
        try {
            const response = await fetchUtils.fetchWithCSRF('/journal/fail-task/', {
                method: 'POST',
                body: JSON.stringify({
                    task_id: taskId,
                    penaltyType: 'DEDUCT_POINTS',
                    pointsToDeduct: 10,
                }),
            });
            const data = await response.json();
            if (data.status === 'success') {
                const pointsDisplay = document.getElementById('points-display');
                if (pointsDisplay) {
                    pointsDisplay.innerText = `Points: ${data.new_points}`;
                }
                uiHelpers.showToast('Points deducted.', 'success');
            } else {
                uiHelpers.showToast('Failed to deduct points.', 'error');
            }
        } catch (error) {
            console.error('Error failing task:', error);
            uiHelpers.showToast('Error failing task.', 'error');
        }
    }

    return { generateTask, completeTask, failTask };
})();
