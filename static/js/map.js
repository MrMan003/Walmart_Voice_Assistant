const gridMap = [
  [ "entrance", "_", "A1", "A2", "A3", "_", "B1", "B2", "B3", "_" ],
  [ "_", "_", "_", "_", "_", "_", "_", "_", "_", "_" ],
  [ "_", "_", "C1", "C2", "C3", "_", "D1", "D2", "D3", "_" ],
  [ "_", "_", "_", "_", "_", "_", "_", "_", "_", "_" ]
];

// Map grid size
const rows = gridMap.length;
const cols = gridMap[0].length;

const tileSize = 40;

const map = L.map('map', {
  crs: L.CRS.Simple,
  minZoom: -1,
});

const bounds = [[0, 0], [rows * tileSize, cols * tileSize]];
map.setView([80, 200], 1);
map.setMaxBounds(bounds);

const layer = L.layerGroup().addTo(map);

// Draw grid
for (let i = 0; i < rows; i++) {
  for (let j = 0; j < cols; j++) {
    const label = gridMap[i][j];
    const color = label === '_' ? '#eee' : '#5cacee';
    const rect = L.rectangle(
      [[i * tileSize, j * tileSize], [(i + 1) * tileSize, (j + 1) * tileSize]],
      { color, weight: 1, fillOpacity: 0.6 }
    ).addTo(layer);
    if (label !== '_') {
      L.marker([i * tileSize + 20, j * tileSize + 20])
        .addTo(layer)
        .bindTooltip(label, { permanent: true });
    }
  }
}

// 👤 User marker
let userMarker = null;

function animatePath(path) {
  if (userMarker) map.removeLayer(userMarker);

  let i = 0;

  function step() {
    if (i >= path.length) return;

    const [row, col] = path[i];
    const lat = row * tileSize + 20;
    const lng = col * tileSize + 20;

    if (userMarker) userMarker.setLatLng([lat, lng]);
    else userMarker = L.circleMarker([lat, lng], {
      radius: 10,
      color: 'red',
      fillOpacity: 1,
    }).addTo(map);

    i++;
    setTimeout(step, 800); // Delay between steps
  }

  step();
}

// Fetch and animate path
async function fetchPath(text) {
  const res = await fetch('/path_data', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ voice_text: text })
  });
  const data = await res.json();
  if (data.path) animatePath(data.path);
  else alert(data.error || "Failed to get path");
}

// Start when mic button is clicked
window.startRecording = function () {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = 'en-US';
  recognition.interimResults = false;
  recognition.start();

  recognition.onresult = function(event) {
    const spoken = event.results[0][0].transcript;
    fetchPath(spoken);
    document.getElementById('voice_text').value = spoken;
    document.getElementById('submitVoice').click();
  };

  recognition.onerror = function(event) {
    alert('Voice error: ' + event.error);
  };
};
