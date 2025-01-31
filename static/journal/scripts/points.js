// ==============================
// Module: Points WebSocket
// ==============================
export const points = (() => {
    const socketProtocol = window.location.protocol === "https:" ? "wss" : "ws";
    const socket = new WebSocket(`${socketProtocol}://${window.location.host}/ws/points/`);

    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        const pointsDisplay = document.querySelector('.profile-stats t1 strong');
        if (pointsDisplay) {
            pointsDisplay.textContent = `Points: ${data.points}`;
        }
    };
})();
