// ==============================
// Main Script for Journal App
// ==============================
import { tasks } from './tasks.js';
import { habits } from './habits.js';
import { points } from './points.js';
import { uiHelpers } from './ui_helpers.js';

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('generate-task')?.addEventListener('click', tasks.generateTask);
    document.getElementById('complete-task')?.addEventListener('click', (event) => {
        tasks.completeTask(event.target.dataset.taskId);
    });
    
    document.getElementById('fail-task')?.addEventListener('click', (event) => {
        tasks.failTask(event.target.dataset.taskId);
    });

    document.addEventListener('change', function (e) {
        if (e.target.classList.contains('todo-checkbox') && e.target.checked) {
            habits.incrementHabit(e.target.dataset.id);
        }
    });
});
const showToast = (message, type = 'info', duration = 3000) => {
    }, duration);
