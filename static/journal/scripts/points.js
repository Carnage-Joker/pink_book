
const socket = new WebSocket(
    `wss://${window.location.host}/ws/points/`
);

socket.onopen = function () {
    console.log("Connected to points WebSocket");
};

socket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    const pointsDisplay = document.querySelector("#points-display");
    if (pointsDisplay) {
        pointsDisplay.textContent = `Points: ${data.points}`;
    }
};
