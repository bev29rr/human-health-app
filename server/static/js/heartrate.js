const canvas = document.getElementById("heartRateCanvas");
let fetchServer = true;
const chart = new SmoothieChart({
    grid: { strokeStyle: "rgba(255,255,255,0.2)", fillStyle: "black", lineWidth: 1 },
    millisPerPixel: 100,
    minValue: 40,
    maxValue: 180
});

chart.streamTo(canvas, 1000); // Update every second
const heartRateLine = new TimeSeries();

async function fetchHeartRate() {
    if (fetchServer) {
        try {
            const response = await fetch("/heartRate");
            const data = await response.json();
            if (data.bpm) {
                heartRateLine.append(new Date().getTime(), data.bpm);
            }
        } catch (error) {
            console.error("Error fetching heart rate:", error);
        }
    } else {
        heartRateLine.append(new Date().getTime(), 60 + Math.random() * 20);
    }
}

document.getElementById('toggleNetLoad').addEventListener('change', function() {
    if (this.checked) {
        fetchServer = true;
    } else {
        fetchServer = false;
    }
});

setInterval(fetchHeartRate, 1000);
chart.addTimeSeries(heartRateLine, { strokeStyle: "red", lineWidth: 2 });