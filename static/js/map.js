/**
 * map.js
 * Leaflet.js interactive map with custom pins and category filters.
 */

let indiaMap = null;
let mapMarkers = [];

document.addEventListener('DOMContentLoaded', () => {
    initLeafletMap();
});

function initLeafletMap() {
    const mapElement = document.getElementById('indiaLeafletMap');
    if (!mapElement) return;

    // Center of India coordinates: [21.5, 78.9]
    indiaMap = L.map('indiaLeafletMap', {
        scrollWheelZoom: false
    }).setView([21.8, 79.5], 5);

    // OpenStreetMap Clean CartoDB Positron / OSM tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18,
        minZoom: 4
    }).addTo(indiaMap);

    loadMapDestinations();
    initMapCategoryFilters();
}

async function loadMapDestinations() {
    try {
        const response = await fetch('/api/destinations');
        const json = await response.json();

        if (!json.success || !json.data) return;

        mapMarkers.forEach(m => indiaMap.removeLayer(m.marker));
        mapMarkers = [];

        json.data.forEach(dest => {
            const coords = dest.coordinates;
            if (!coords || coords.length < 2) return;

            const markerColor = getMarkerColor(dest.category);
            
            // Custom HTML Marker Icon
            const customIcon = L.divIcon({
                className: 'custom-map-pin',
                html: `<div style="
                    background-color: ${markerColor};
                    width: 18px;
                    height: 18px;
                    border-radius: 50%;
                    border: 2px solid #FFFFFF;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.35);
                    cursor: pointer;
                    transition: transform 0.2s;
                "></div>`,
                iconSize: [18, 18],
                iconAnchor: [9, 9]
            });

            const marker = L.marker([coords[0], coords[1]], { icon: customIcon });

            // Popup HTML
            const popupContent = `
                <div class="map-popup-card">
                    <img src="${dest.image}" alt="${dest.name}" class="popup-img">
                    <div class="popup-body">
                        <span style="font-size:0.6875rem; text-transform:uppercase; font-weight:700; color:var(--color-accent);">${dest.category}</span>
                        <h4 class="popup-title">${dest.name}</h4>
                        <p class="popup-desc">${dest.title}</p>
                        <div style="font-size:0.75rem; margin-bottom:0.5rem;">
                            <strong>🗓️ ${dest.ideal_days}</strong> • <strong>~₹${dest.avg_daily_budget}/d</strong>
                        </div>
                        <div style="display:flex; gap:0.35rem;">
                            <button type="button" class="btn btn-primary btn-sm" style="flex:1; padding:0.25rem 0.5rem; font-size:0.6875rem;" onclick="selectDestinationForPlanner('${dest.id}')">
                                Plan Trip
                            </button>
                            <button type="button" class="btn btn-outline btn-sm" style="flex:1; padding:0.25rem 0.5rem; font-size:0.6875rem;" onclick="openDestinationModal('${dest.id}')">
                                Info
                            </button>
                        </div>
                    </div>
                </div>
            `;

            marker.bindPopup(popupContent, { maxWidth: 260 });
            marker.addTo(indiaMap);

            mapMarkers.push({
                marker: marker,
                category: dest.category,
                data: dest
            });
        });

    } catch (err) {
        console.error('Error loading destinations for map:', err);
    }
}

function getMarkerColor(category) {
    if (category.includes('Heritage')) return '#B83232';
    if (category.includes('Spiritual')) return '#D97706';
    if (category.includes('Hill Stations') || category.includes('Nature')) return '#166534';
    if (category.includes('Beaches')) return '#0284C7';
    if (category.includes('Adventure')) return '#4338CA';
    if (category.includes('Wildlife')) return '#15803D';
    return '#163A2E';
}

function initMapCategoryFilters() {
    const filterPills = document.querySelectorAll('#mapCategoryPills .pill-filter');

    filterPills.forEach(pill => {
        pill.addEventListener('click', () => {
            filterPills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');

            const selectedCat = pill.getAttribute('data-map-cat');

            mapMarkers.forEach(item => {
                if (selectedCat === 'all' || item.category.toLowerCase().includes(selectedCat.toLowerCase())) {
                    if (!indiaMap.hasLayer(item.marker)) {
                        item.marker.addTo(indiaMap);
                    }
                } else {
                    if (indiaMap.hasLayer(item.marker)) {
                        indiaMap.removeLayer(item.marker);
                    }
                }
            });
        });
    });
}
