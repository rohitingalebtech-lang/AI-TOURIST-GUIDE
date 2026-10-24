/**
 * map.js
 * Interactive Leaflet.js map with custom category markers,
 * two-way card synchronisation, bounds fitting, and directions links.
 */

let indiaMap = null;
let currentMarkers = [];
let markerClusterGroup = null;

document.addEventListener('DOMContentLoaded', () => {
    initLeafletMap();
});

function initLeafletMap() {
    const mapElement = document.getElementById('indiaLeafletMap');
    if (!mapElement) return;

    try {
        // Center of India coordinates: [21.5, 78.9]
        indiaMap = L.map('indiaLeafletMap', {
            scrollWheelZoom: false,
            zoomControl: true
        }).setView([21.8, 79.5], 5);

        // OpenStreetMap clean carto tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 18,
            minZoom: 4
        }).addTo(indiaMap);

        loadInitialDestinations();
        initMapControls();
    } catch (err) {
        console.error('Leaflet initialization failed:', err);
        mapElement.innerHTML = `
            <div style="display:flex; align-items:center; justify-content:center; height:100%; color:var(--text-muted); text-align:center; padding:1rem;">
                <p>🗺️ Interactive map is running in offline mode. Map tiles could not be fetched.</p>
            </div>
        `;
    }
}

async function loadInitialDestinations() {
    try {
        const response = await fetch('/api/destinations');
        const json = await response.json();
        if (json.success && json.data) {
            renderMapMarkers(json.data);
        }
    } catch (e) {
        console.warn('Initial map load error:', e);
    }
}

function initMapControls() {
    const fitBtn = document.getElementById('fitMapBoundsBtn');
    if (fitBtn) {
        fitBtn.addEventListener('click', fitMapBounds);
    }

    const pills = document.querySelectorAll('#mapCategoryPills .pill-filter');
    pills.forEach(pill => {
        pill.addEventListener('click', () => {
            if (pill.id === 'fitMapBoundsBtn') return;

            pills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');

            const cat = pill.getAttribute('data-map-cat') || 'all';
            filterMapMarkersByCategory(cat);
        });
    });
}

function getMarkerColor(category) {
    const cat = (category || '').toLowerCase();
    if (cat.includes('heritage') || cat.includes('historical') || cat.includes('fort')) return '#8B263E'; // Crimson Maroon
    if (cat.includes('spiritual') || cat.includes('sacred') || cat.includes('temple')) return '#D97706'; // Warm Saffron
    if (cat.includes('beach') || cat.includes('coastal')) return '#0284C7'; // Ocean Blue
    if (cat.includes('mountain') || cat.includes('hill') || cat.includes('nature')) return '#166534'; // Forest Green
    if (cat.includes('wildlife')) return '#B45309'; // Amber Gold
    return '#4F46E5'; // Indigo default
}

function renderMapMarkers(items) {
    if (!indiaMap) return;

    // Clear existing
    currentMarkers.forEach(m => indiaMap.removeLayer(m.marker));
    currentMarkers = [];

    const bounds = L.latLngBounds();
    let hasCoords = false;

    items.forEach(dest => {
        let lat = dest.lat !== undefined ? dest.lat : (dest.coordinates ? dest.coordinates[0] : null);
        let lng = dest.lng !== undefined ? dest.lng : (dest.coordinates ? dest.coordinates[1] : null);

        if (!lat || !lng) return;

        hasCoords = true;
        bounds.extend([lat, lng]);

        const markerColor = getMarkerColor(dest.category);
        const customIcon = L.divIcon({
            className: 'custom-map-pin',
            html: `
                <div style="
                    background: ${markerColor};
                    width: 22px;
                    height: 22px;
                    border-radius: 50%;
                    border: 2px solid #FFFFFF;
                    box-shadow: 0 3px 8px rgba(0,0,0,0.35);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 10px;
                    cursor: pointer;
                    transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
                ">●</div>
            `,
            iconSize: [22, 22],
            iconAnchor: [11, 11]
        });

        const marker = L.marker([lat, lng], { icon: customIcon });

        const image = dest.image || 'https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=400&q=80';
        const popupContent = `
            <div class="map-popup-card">
                <img src="${escapeHtml(image)}" alt="${escapeHtml(dest.name)}" class="popup-img" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=400&q=80';">
                <div class="popup-body">
                    <span class="popup-category">${escapeHtml(dest.category || 'Sightseeing')}</span>
                    <h4 class="popup-title">${escapeHtml(dest.name)}</h4>
                    <p class="popup-desc">${escapeHtml(dest.description || dest.title || '')}</p>
                    <div class="popup-actions">
                        <button type="button" class="btn btn-primary btn-sm" onclick="selectDestinationForPlanner('${escapeHtml(dest.id || dest.name)}')">
                            Plan Trip
                        </button>
                        <button type="button" class="btn btn-outline btn-sm" onclick="openDestinationModal('${escapeHtml(dest.id || dest.name)}')">
                            Details
                        </button>
                    </div>
                </div>
            </div>
        `;

        marker.bindPopup(popupContent, { maxWidth: 260 });

        // Two-way sync: clicking marker highlights card
        marker.on('click', () => {
            highlightCardForMarker(dest.id || dest.name);
        });

        marker.addTo(indiaMap);

        currentMarkers.push({
            id: dest.id || dest.name,
            name: dest.name,
            category: dest.category || '',
            marker: marker,
            lat: lat,
            lng: lng
        });
    });

    if (hasCoords && items.length > 1) {
        indiaMap.fitBounds(bounds, { padding: [40, 40], maxZoom: 12 });
    }
}

function filterMapMarkersByCategory(cat) {
    currentMarkers.forEach(m => {
        if (cat === 'all' || m.category.toLowerCase().includes(cat.toLowerCase())) {
            m.marker.addTo(indiaMap);
        } else {
            indiaMap.removeLayer(m.marker);
        }
    });
}

function fitMapBounds() {
    if (!indiaMap || currentMarkers.length === 0) return;
    const bounds = L.latLngBounds();
    currentMarkers.forEach(m => bounds.extend([m.lat, m.lng]));
    indiaMap.fitBounds(bounds, { padding: [40, 40] });
}

function highlightCardForMarker(placeId) {
    const card = document.querySelector(`.dest-card[data-id="${placeId}"]`);
    if (card) {
        document.querySelectorAll('.dest-card').forEach(c => c.classList.remove('highlighted-card'));
        card.classList.add('highlighted-card');
        card.scrollIntoView({ behavior: 'smooth', block: 'center' });
        setTimeout(() => card.classList.remove('highlighted-card'), 3000);
    }
}

// Global hooks for app.js
window.updateMapMarkersWithResults = function(results) {
    renderMapMarkers(results);
};

window.focusLeafletMap = function(lat, lng, placeId) {
    if (!indiaMap) return;
    indiaMap.setView([lat, lng], 13, { animate: true });

    const m = currentMarkers.find(item => item.id === placeId || (Math.abs(item.lat - lat) < 0.001 && Math.abs(item.lng - lng) < 0.001));
    if (m && m.marker) {
        m.marker.openPopup();
    }
};

function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>'"]/g, tag => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        "'": '&#39;',
        '"': '&quot;'
    }[tag] || tag));
}
