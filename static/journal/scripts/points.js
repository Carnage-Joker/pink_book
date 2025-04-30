const socket = new WebSocket('wss://' + window.location.host + '/ws/points/');

const pointsDisplay = document.querySelector("#points-display");

socket.onopen = function () {
    console.log("Connected to points WebSocket");
};

socket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    if (pointsDisplay) {
        pointsDisplay.textContent = `Points: ${data.points}`;
    }
};

socket.onclose = function () {
    console.error("Points WebSocket closed unexpectedly");
};

socket.onerror = function (error) {
    console.error("Points WebSocket error:", error);
};

export { socket };
