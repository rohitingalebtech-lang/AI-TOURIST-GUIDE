/**
 * app.js
 * Core UI interactions, live search across India via Nominatim & Wikipedia,
 * dynamic photographic card rendering, rich modal drawers, bookmarks, and notifications.
 */

let currentSearchResults = [];
let savedBookmarks = [];

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initBookmarks();
    initLiveSearch();
    initModalHandlers();
    updateSavedTripsCounter();
});

/**
 * Toast Notification Utility
 */
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<span>${escapeHtml(message)}</span>`;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

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

/**
 * Navigation & Mobile Menu
 */
function initNavigation() {
    const mobileToggle = document.getElementById('mobileMenuToggle');
    const mainNav = document.getElementById('mainNav');

    if (mobileToggle && mainNav) {
        mobileToggle.addEventListener('click', () => {
            mainNav.classList.toggle('open');
        });

        mainNav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mainNav.classList.remove('open');
            });
        });
    }

    // Scroll spy for active navigation item
    const sections = document.querySelectorAll('section[id]');
    window.addEventListener('scroll', () => {
        const scrollY = window.pageYOffset;
        sections.forEach(current => {
            const sectionHeight = current.offsetHeight;
            const sectionTop = current.offsetTop - 130;
            const sectionId = current.getAttribute('id');

            const navMatch = document.querySelector(`.nav-links a[href*="${sectionId}"]`);
            if (navMatch) {
                if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                    navMatch.classList.add('active');
                } else {
                    navMatch.classList.remove('active');
                }
            }
        });
    });
}

/**
 * Bookmarks / Saved Places System
 */
function initBookmarks() {
    try {
        const saved = localStorage.getItem('yatra_saved_bookmarks');
        if (saved) {
            savedBookmarks = JSON.parse(saved);
        }
    } catch (e) {
        savedBookmarks = [];
    }
}

function toggleBookmark(placeId, placeName) {
    const idx = savedBookmarks.findIndex(b => b.id === placeId);
    if (idx >= 0) {
        savedBookmarks.splice(idx, 1);
        showToast(`Removed ${placeName} from saved places`, 'info');
    } else {
        savedBookmarks.push({ id: placeId, name: placeName, date: new Date().toISOString() });
        showToast(`Saved ${placeName} to your places!`, 'success');
    }

    try {
        localStorage.setItem('yatra_saved_bookmarks', JSON.stringify(savedBookmarks));
    } catch (e) {}

    updateSavedTripsCounter();
    updateBookmarkButtonStates();
}

function updateBookmarkButtonStates() {
    document.querySelectorAll('.save-place-btn').forEach(btn => {
        const id = btn.getAttribute('data-id');
        if (savedBookmarks.some(b => b.id === id)) {
            btn.classList.add('saved');
            btn.innerHTML = '❤️';
            btn.title = 'Saved to Bookmarks';
        } else {
            btn.classList.remove('saved');
            btn.innerHTML = '🔖';
            btn.title = 'Save to Bookmarks';
        }
    });
}

function updateSavedTripsCounter() {
    const counter = document.getElementById('savedTripsCount');
    if (!counter) return;

    fetch('/api/trips')
        .then(res => res.json())
        .then(data => {
            const serverTrips = (data.success && data.data) ? data.data.length : 0;
            const total = serverTrips + savedBookmarks.length;
            counter.textContent = total;
        })
        .catch(() => {
            counter.textContent = savedBookmarks.length;
        });
}

/**
 * Live Search Across India System
 */
let searchDebounceTimer = null;

function initLiveSearch() {
    const searchInput = document.getElementById('destinationSearchInput');
    const searchClearBtn = document.getElementById('searchClearBtn');
    const heroSearchBtn = document.getElementById('heroSearchActionBtn');
    const catPills = document.querySelectorAll('#quickCategoryPills .cat-pill');
    const regionTabs = document.querySelectorAll('#regionTabs .region-tab');
    const catSelect = document.getElementById('filterCategorySelect');
    const sortSelect = document.getElementById('filterSortSelect');
    const resetBtn = document.getElementById('resetSearchActionBtn');

    let currentCategory = 'all';
    let currentRegion = 'all';

    // Search input with debounce
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.trim();
            if (searchClearBtn) {
                searchClearBtn.style.display = query ? 'block' : 'none';
            }

            clearTimeout(searchDebounceTimer);
            searchDebounceTimer = setTimeout(() => {
                performLiveSearch(query, currentCategory);
            }, 350);
        });

        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                clearTimeout(searchDebounceTimer);
                performLiveSearch(searchInput.value.trim(), currentCategory);
                scrollToExplore();
            }
        });
    }

    if (searchClearBtn) {
        searchClearBtn.addEventListener('click', () => {
            if (searchInput) searchInput.value = '';
            searchClearBtn.style.display = 'none';
            performLiveSearch('', 'all');
        });
    }

    if (heroSearchBtn) {
        heroSearchBtn.addEventListener('click', () => {
            const q = searchInput ? searchInput.value.trim() : '';
            performLiveSearch(q, currentCategory);
            scrollToExplore();
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            if (searchInput) searchInput.value = '';
            if (searchClearBtn) searchClearBtn.style.display = 'none';
            catPills.forEach(p => p.classList.remove('active'));
            const allPill = document.querySelector('#quickCategoryPills .cat-pill[data-category="all"]');
            if (allPill) allPill.classList.add('active');
            performLiveSearch('', 'all');
        });
    }

    // Quick Category pills in Hero
    catPills.forEach(pill => {
        pill.addEventListener('click', () => {
            catPills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');

            currentCategory = pill.getAttribute('data-category') || 'all';
            if (catSelect) catSelect.value = currentCategory;

            const q = searchInput ? searchInput.value.trim() : '';
            performLiveSearch(q, currentCategory);
            scrollToExplore();
        });
    });

    // Category Select in filter bar
    if (catSelect) {
        catSelect.addEventListener('change', (e) => {
            currentCategory = e.target.value;
            catPills.forEach(p => {
                p.classList.toggle('active', p.getAttribute('data-category') === currentCategory);
            });
            const q = searchInput ? searchInput.value.trim() : '';
            performLiveSearch(q, currentCategory);
        });
    }

    // Sort select
    if (sortSelect) {
        sortSelect.addEventListener('change', () => {
            sortAndRenderCards();
        });
    }

    // Region Tabs
    regionTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            regionTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            currentRegion = tab.getAttribute('data-region') || 'all';
            filterLocalCardsByRegion(currentRegion);
        });
    });

    // Delegate Card Actions
    const grid = document.getElementById('destinationsGrid');
    if (grid) {
        grid.addEventListener('click', (e) => {
            const viewBtn = e.target.closest('.view-dest-btn');
            if (viewBtn) {
                const id = viewBtn.getAttribute('data-id');
                const name = viewBtn.getAttribute('data-name');
                openDestinationDetails(id || name);
                return;
            }

            const mapBtn = e.target.closest('.view-on-map-btn');
            if (mapBtn) {
                const id = mapBtn.getAttribute('data-id');
                const lat = parseFloat(mapBtn.getAttribute('data-lat'));
                const lng = parseFloat(mapBtn.getAttribute('data-lng'));
                focusMapOnLocation(id, lat, lng);
                return;
            }

            const saveBtn = e.target.closest('.save-place-btn');
            if (saveBtn) {
                const id = saveBtn.getAttribute('data-id');
                const name = saveBtn.getAttribute('data-name');
                toggleBookmark(id, name);
                return;
            }
        });
    }
}

function scrollToExplore() {
    const exploreSec = document.getElementById('explore');
    if (exploreSec) {
        exploreSec.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Fetch and render search results from `/api/search/live`
 */
async function performLiveSearch(query, category = 'all') {
    const loadingBar = document.getElementById('searchLoadingBar');
    const emptyBox = document.getElementById('emptyResultsBox');
    const grid = document.getElementById('destinationsGrid');
    const statusText = document.getElementById('filterStatusText');
    const titleEl = document.getElementById('exploreSectionTitle');

    if (!query) {
        // Reload default server-rendered destinations if empty
        if (loadingBar) loadingBar.style.display = 'none';
        if (emptyBox) emptyBox.style.display = 'none';
        if (titleEl) titleEl.textContent = 'Popular Destinations & Attractions';
        if (statusText) statusText.textContent = 'Showing popular destinations across India';
        filterCardsByCategory(category);
        return;
    }

    if (loadingBar) loadingBar.style.display = 'flex';
    if (emptyBox) emptyBox.style.display = 'none';

    try {
        const url = `/api/search/live?q=${encodeURIComponent(query)}&category=${encodeURIComponent(category)}&limit=24`;
        const resp = await fetch(url);
        const data = await resp.json();

        if (loadingBar) loadingBar.style.display = 'none';

        if (!data.success || !data.results || data.results.length === 0) {
            if (grid) grid.innerHTML = '';
            if (emptyBox) emptyBox.style.display = 'block';
            if (statusText) statusText.textContent = `No attractions found for "${query}"`;
            currentSearchResults = [];
            if (window.updateMapMarkersWithResults) {
                window.updateMapMarkersWithResults([]);
            }
            return;
        }

        currentSearchResults = data.results;
        if (emptyBox) emptyBox.style.display = 'none';
        if (titleEl) {
            titleEl.textContent = data.geocoded ? `Attractions & Sights in ${data.geocoded.name}` : `Search Results for "${query}"`;
        }
        if (statusText) {
            statusText.textContent = `Found ${data.count} destinations & attractions across India`;
        }

        renderSearchResultsCards(currentSearchResults);

        // Update map markers
        if (window.updateMapMarkersWithResults) {
            window.updateMapMarkersWithResults(currentSearchResults);
        }

    } catch (err) {
        if (loadingBar) loadingBar.style.display = 'none';
        console.error('Search failed:', err);
        showToast('Network issue while searching. Showing local destinations.', 'warning');
    }
}

function renderSearchResultsCards(results) {
    const grid = document.getElementById('destinationsGrid');
    if (!grid) return;

    grid.innerHTML = results.map(item => {
        const image = item.image || 'https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=800&q=80';
        const isSaved = savedBookmarks.some(b => b.id === item.id);
        const distBadge = item.distance_km !== undefined && item.distance_km > 0 ? 
            `<span class="badge-dist">📍 ${item.distance_km} km away</span>` : '';
        const budgetText = item.avg_daily_budget ? `~₹${item.avg_daily_budget.toLocaleString()}/d` : 'Free entry / Variable';

        return `
        <article class="dest-card" data-id="${escapeHtml(item.id)}" data-category="${escapeHtml(item.category)}" data-budget="${item.avg_daily_budget || 0}" data-lat="${item.lat || ''}" data-lng="${item.lng || ''}">
            <div class="dest-card-media">
                <img src="${escapeHtml(image)}" alt="${escapeHtml(item.name)}" loading="lazy" class="dest-card-img" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=800&q=80';">
                <div class="dest-card-badges">
                    <span class="badge-state">${escapeHtml(item.state || 'India')}</span>
                    <span class="badge-category">${escapeHtml(item.category.split('&')[0])}</span>
                </div>
                ${distBadge}
            </div>
            <div class="dest-card-body">
                <h3 class="dest-card-title">${escapeHtml(item.name)}</h3>
                <p class="dest-card-subtitle">${escapeHtml(item.description)}</p>
                
                <div class="dest-quick-meta">
                    <div class="meta-item">
                        <span class="meta-icon">💰</span>
                        <span class="meta-text">${budgetText}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-icon">🏛️</span>
                        <span class="meta-text">${escapeHtml(item.category.split('&')[0])}</span>
                    </div>
                </div>

                <div class="dest-card-actions">
                    <button type="button" class="btn btn-primary btn-sm view-dest-btn" data-id="${escapeHtml(item.id)}" data-name="${escapeHtml(item.name)}">
                        View Details
                    </button>
                    <button type="button" class="btn btn-outline btn-sm view-on-map-btn" data-id="${escapeHtml(item.id)}" data-name="${escapeHtml(item.name)}" data-lat="${item.lat || ''}" data-lng="${item.lng || ''}" title="View on map">
                        Map
                    </button>
                    <button type="button" class="btn btn-icon-sm save-place-btn ${isSaved ? 'saved' : ''}" data-id="${escapeHtml(item.id)}" data-name="${escapeHtml(item.name)}" title="Save Place" aria-label="Save Place">
                        ${isSaved ? '❤️' : '🔖'}
                    </button>
                </div>
            </div>
        </article>
        `;
    }).join('');
}

function filterCardsByCategory(category) {
    const cards = document.querySelectorAll('.dest-card');
    let visible = 0;
    cards.forEach(card => {
        const cat = card.getAttribute('data-category') || '';
        if (category === 'all' || cat.toLowerCase().includes(category.toLowerCase())) {
            card.style.display = 'flex';
            visible++;
        } else {
            card.style.display = 'none';
        }
    });

    const statusText = document.getElementById('filterStatusText');
    if (statusText) {
        statusText.textContent = `Showing ${visible} destinations`;
    }
}

function filterLocalCardsByRegion(region) {
    const cards = document.querySelectorAll('.dest-card');
    let visible = 0;
    cards.forEach(card => {
        const cardRegion = card.getAttribute('data-region') || '';
        if (region === 'all' || cardRegion.toLowerCase() === region.toLowerCase()) {
            card.style.display = 'flex';
            visible++;
        } else {
            card.style.display = 'none';
        }
    });

    const statusText = document.getElementById('filterStatusText');
    if (statusText) {
        statusText.textContent = `Showing ${visible} destinations in ${region === 'all' ? 'All India' : region}`;
    }
}

function sortAndRenderCards() {
    const sortVal = document.getElementById('filterSortSelect')?.value || 'popular';
    const grid = document.getElementById('destinationsGrid');
    if (!grid) return;

    const cards = Array.from(grid.querySelectorAll('.dest-card'));
    cards.sort((a, b) => {
        if (sortVal === 'rating') {
            const rA = parseFloat(a.getAttribute('data-rating') || '4.0');
            const rB = parseFloat(b.getAttribute('data-rating') || '4.0');
            return rB - rA;
        } else if (sortVal === 'budget_low') {
            const bA = parseInt(a.getAttribute('data-budget') || '0', 10);
            const bB = parseInt(b.getAttribute('data-budget') || '0', 10);
            return bA - bB;
        } else if (sortVal === 'budget_high') {
            const bA = parseInt(a.getAttribute('data-budget') || '0', 10);
            const bB = parseInt(b.getAttribute('data-budget') || '0', 10);
            return bB - bA;
        }
        return 0;
    });

    cards.forEach(c => grid.appendChild(c));
}

function focusMapOnLocation(placeId, lat, lng) {
    if (!lat || !lng) {
        showToast('Coordinates not available for this landmark', 'warning');
        return;
    }

    const mapElement = document.getElementById('interactive-map');
    if (mapElement) {
        mapElement.scrollIntoView({ behavior: 'smooth' });
    }

    if (window.focusLeafletMap) {
        window.focusLeafletMap(lat, lng, placeId);
    }
}

/**
 * Rich Destination Details Modal
 */
function initModalHandlers() {
    const modal = document.getElementById('destinationModal');
    const closeBtn = document.getElementById('modalCloseBtn');

    if (closeBtn && modal) {
        closeBtn.addEventListener('click', () => {
            modal.style.display = 'none';
            modal.setAttribute('aria-hidden', 'true');
        });

        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
                modal.setAttribute('aria-hidden', 'true');
            }
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.style.display === 'block') {
                modal.style.display = 'none';
                modal.setAttribute('aria-hidden', 'true');
            }
        });
    }
}

async function openDestinationDetails(idOrName) {
    const modal = document.getElementById('destinationModal');
    const titleEl = document.getElementById('modalDestTitle');
    const stateTag = document.getElementById('modalStateTag');
    const bodyEl = document.getElementById('modalBodyContent');

    if (!modal || !bodyEl) return;

    modal.style.display = 'block';
    modal.setAttribute('aria-hidden', 'false');

    if (titleEl) titleEl.textContent = 'Loading Destination...';
    if (stateTag) stateTag.textContent = 'India';
    bodyEl.innerHTML = `
        <div class="modal-loading-skeleton">
            <div class="spinner-ring" style="margin: 2rem auto;"></div>
            <p style="text-align:center; color:var(--text-muted);">Consulting verified tourist and geographic records...</p>
        </div>
    `;

    try {
        const resp = await fetch(`/api/place/details?id=${encodeURIComponent(idOrName)}`);
        const data = await resp.json();

        if (!data.success) {
            throw new Error(data.error || 'Destination not found');
        }

        renderDestinationModalBody(data);
    } catch (err) {
        bodyEl.innerHTML = `
            <div class="modal-error-box">
                <p>⚠️ Could not load destination details: ${escapeHtml(err.message)}</p>
                <button type="button" class="btn btn-primary btn-sm" onclick="document.getElementById('destinationModal').style.display='none'">Close</button>
            </div>
        `;
    }
}

function renderDestinationModalBody(data) {
    const titleEl = document.getElementById('modalDestTitle');
    const stateTag = document.getElementById('modalStateTag');
    const bodyEl = document.getElementById('modalBodyContent');

    if (titleEl) titleEl.textContent = data.name;
    if (stateTag) stateTag.textContent = data.state || 'India';

    const gallery = data.gallery && data.gallery.length > 0 ? data.gallery : [
        { url: 'https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=1000&q=80', attribution: 'Travel Archive', title: data.name }
    ];

    const weatherBadge = data.weather && data.weather.temperature !== undefined ? `
        <div class="modal-weather-card">
            <span class="weather-icon">${data.weather.icon || '☀️'}</span>
            <div class="weather-text">
                <strong>${data.weather.temperature}°C</strong>
                <span>${escapeHtml(data.weather.condition || 'Pleasant')}</span>
            </div>
        </div>
    ` : '';

    const highlightsList = data.highlights && data.highlights.length > 0 ? `
        <div class="modal-info-block">
            <h4>🌟 Key Highlights & Activities</h4>
            <div class="modal-pills-list">
                ${data.highlights.map(h => `<span class="detail-pill">${escapeHtml(h)}</span>`).join('')}
            </div>
        </div>
    ` : '';

    const foodsList = data.famous_foods && data.famous_foods.length > 0 ? `
        <div class="modal-info-block">
            <h4>🍛 Must-Try Local Delicacies</h4>
            <ul class="modal-bullet-list">
                ${data.famous_foods.map(f => `<li><strong>${escapeHtml(f.dish)}:</strong> ${escapeHtml(f.desc)}</li>`).join('')}
            </ul>
        </div>
    ` : '';

    const tipsList = data.culture_tips && data.culture_tips.length > 0 ? `
        <div class="modal-info-block">
            <h4>🛕 Local Cultural Etiquette & Tips</h4>
            <ul class="modal-bullet-list">
                ${data.culture_tips.map(t => `<li>${escapeHtml(t)}</li>`).join('')}
            </ul>
        </div>
    ` : '';

    const nearbyList = data.nearby_attractions && data.nearby_attractions.length > 0 ? `
        <div class="modal-info-block">
            <h4>📍 Nearby Sights to Explore</h4>
            <div class="modal-nearby-grid">
                ${data.nearby_attractions.map(n => `
                    <div class="nearby-mini-card" onclick="openDestinationDetails('${escapeHtml(n.name)}')">
                        <img src="${escapeHtml(n.image)}" alt="${escapeHtml(n.name)}" class="nearby-mini-img">
                        <div class="nearby-mini-body">
                            <strong>${escapeHtml(n.name)}</strong>
                            <span>${n.distance_km ? `${n.distance_km} km away` : escapeHtml(n.category)}</span>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    ` : '';

    bodyEl.innerHTML = `
        <div class="modal-detail-layout">
            <!-- Main Photo Gallery -->
            <div class="modal-gallery-wrap">
                <div class="gallery-main-img-wrap">
                    <img src="${escapeHtml(gallery[0].url)}" alt="${escapeHtml(data.name)}" id="galleryMainImg" class="gallery-main-img">
                    <span class="gallery-caption" id="galleryCaption">${escapeHtml(gallery[0].attribution || 'Wikimedia Commons')}</span>
                </div>
                ${gallery.length > 1 ? `
                <div class="gallery-thumbs-row">
                    ${gallery.map((g, idx) => `
                        <img src="${escapeHtml(g.url)}" alt="${escapeHtml(g.title || '')}" class="gallery-thumb ${idx === 0 ? 'active' : ''}" onclick="switchModalGalleryImage('${escapeHtml(g.url)}', '${escapeHtml(g.attribution || '')}', this)">
                    `).join('')}
                </div>
                ` : ''}
            </div>

            <!-- Quick Specs Header -->
            <div class="modal-specs-bar">
                <div class="spec-col">
                    <span class="spec-label">Category</span>
                    <span class="spec-val">${escapeHtml(data.category)}</span>
                </div>
                <div class="spec-col">
                    <span class="spec-label">Ideal Days</span>
                    <span class="spec-val">${escapeHtml(data.ideal_days || '1-2 Days')}</span>
                </div>
                <div class="spec-col">
                    <span class="spec-label">Best Season</span>
                    <span class="spec-val">${escapeHtml(data.best_season ? data.best_season.split('(')[0] : 'Year-round')}</span>
                </div>
                ${weatherBadge}
            </div>

            <!-- Verified Pricing & Timings Notice -->
            <div class="modal-verification-alert">
                <div class="alert-icon">ℹ️</div>
                <div class="alert-text">
                    <strong>Verified Visitor Advisory:</strong>
                    <p>${escapeHtml(data.entry_fee_note || 'Please check ASI ticketing portal for verified entry fees.')} ${escapeHtml(data.opening_hours || '')}</p>
                </div>
            </div>

            <!-- Short Introduction Description -->
            <div class="modal-description-box">
                <p>${escapeHtml(data.description)}</p>
            </div>

            ${highlightsList}
            ${foodsList}
            ${tipsList}
            ${nearbyList}

            <!-- Action Buttons Footer -->
            <div class="modal-actions-footer">
                <button type="button" class="btn btn-primary" onclick="selectDestinationForPlanner('${escapeHtml(data.id || data.name)}'); document.getElementById('destinationModal').style.display='none';">
                    Plan Trip Here
                </button>
                <a href="${data.google_maps_url || '#'}" target="_blank" rel="noopener" class="btn btn-outline">
                    🧭 Directions (Google Maps)
                </a>
                <button type="button" class="btn btn-outline" onclick="toggleBookmark('${escapeHtml(data.id || data.name)}', '${escapeHtml(data.name)}')">
                    🔖 Save Place
                </button>
            </div>
        </div>
    `;
}

function switchModalGalleryImage(url, attr, thumbEl) {
    const mainImg = document.getElementById('galleryMainImg');
    const cap = document.getElementById('galleryCaption');
    if (mainImg) mainImg.src = url;
    if (cap) cap.textContent = attr || 'Wikimedia Commons';

    document.querySelectorAll('.gallery-thumb').forEach(t => t.classList.remove('active'));
    if (thumbEl) thumbEl.classList.add('active');
}

// Global hook for selecting destination into planner
window.selectDestinationForPlanner = function(destIdOrName) {
    const destSelect = document.getElementById('plannerDestination');
    if (destSelect) {
        let matched = false;
        for (let opt of destSelect.options) {
            if (opt.value.toLowerCase() === destIdOrName.toLowerCase() || opt.text.toLowerCase().includes(destIdOrName.toLowerCase())) {
                destSelect.value = opt.value;
                matched = true;
                break;
            }
        }
        if (!matched) {
            // Append as new option
            const newOpt = document.createElement('option');
            newOpt.value = destIdOrName.toLowerCase();
            newOpt.textContent = destIdOrName;
            destSelect.appendChild(newOpt);
            destSelect.value = destIdOrName.toLowerCase();
        }
    }

    const plannerSec = document.getElementById('planner');
    if (plannerSec) {
        plannerSec.scrollIntoView({ behavior: 'smooth' });
    }
};

window.openDestinationModal = function(id) {
    openDestinationDetails(id);
};
