/**
 * app.js
 * Core UI interactions, search filtering, modals, and notification toast.
 */

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initDestinationFilters();
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
    toast.innerHTML = `<span>${message}</span>`;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

/**
 * Navigation & Mobile Menu
 */
function initNavigation() {
    const mobileToggle = document.getElementById('mobileMenuToggle');
    const mainNavLinks = document.querySelector('.nav-links');

    if (mobileToggle && mainNavLinks) {
        mobileToggle.addEventListener('click', () => {
            mainNavLinks.classList.toggle('open');
        });

        // Close on link click
        mainNavLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mainNavLinks.classList.remove('open');
            });
        });
    }

    // Scroll spy for active navigation item
    const sections = document.querySelectorAll('section[id]');
    window.addEventListener('scroll', () => {
        const scrollY = window.pageYOffset;
        sections.forEach(current => {
            const sectionHeight = current.offsetHeight;
            const sectionTop = current.offsetTop - 120;
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
 * Destination Search & Filtering System
 */
function initDestinationFilters() {
    const searchInput = document.getElementById('destinationSearchInput');
    const searchClearBtn = document.getElementById('searchClearBtn');
    const heroSearchBtn = document.getElementById('heroSearchActionBtn');
    const chipButtons = document.querySelectorAll('.chip-btn');
    const regionTabs = document.querySelectorAll('.region-tab');
    const categorySelect = document.getElementById('filterCategorySelect');
    const budgetSelect = document.getElementById('filterBudgetSelect');
    const statusText = document.getElementById('filterStatusText');
    const cards = document.querySelectorAll('.dest-card');

    let currentRegion = 'all';
    let currentCategory = 'all';
    let currentBudget = 'all';
    let currentSearchTerm = '';

    function applyFilters() {
        let visibleCount = 0;

        cards.forEach(card => {
            const cardRegion = card.getAttribute('data-region') || '';
            const cardCategory = card.getAttribute('data-category') || '';
            const cardBudget = parseInt(card.getAttribute('data-budget') || '0', 10);
            const cardText = card.textContent.toLowerCase();

            let matchesRegion = (currentRegion === 'all' || cardRegion.toLowerCase() === currentRegion.toLowerCase());
            let matchesCategory = (currentCategory === 'all' || cardCategory.toLowerCase().includes(currentCategory.toLowerCase()));
            
            let matchesBudget = true;
            if (currentBudget === 'budget') matchesBudget = cardBudget <= 2000;
            else if (currentBudget === 'moderate') matchesBudget = cardBudget > 2000 && cardBudget <= 3500;
            else if (currentBudget === 'luxury') matchesBudget = cardBudget > 3500;

            let matchesSearch = (!currentSearchTerm || cardText.includes(currentSearchTerm));

            if (matchesRegion && matchesCategory && matchesBudget && matchesSearch) {
                card.style.display = 'flex';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        if (statusText) {
            statusText.textContent = `Showing ${visibleCount} of ${cards.length} destinations`;
        }
    }

    // Search Input listeners
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            currentSearchTerm = e.target.value.trim().toLowerCase();
            if (searchClearBtn) {
                searchClearBtn.style.display = currentSearchTerm ? 'block' : 'none';
            }
            applyFilters();
        });

        if (searchClearBtn) {
            searchClearBtn.addEventListener('click', () => {
                searchInput.value = '';
                currentSearchTerm = '';
                searchClearBtn.style.display = 'none';
                applyFilters();
            });
        }
    }

    if (heroSearchBtn) {
        heroSearchBtn.addEventListener('click', () => {
            const exploreSection = document.getElementById('explore');
            if (exploreSection) {
                exploreSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }

    // Quick Theme Chips
    chipButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            chipButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentCategory = btn.getAttribute('data-category');
            if (categorySelect) categorySelect.value = currentCategory;
            applyFilters();

            const exploreSection = document.getElementById('explore');
            if (exploreSection && window.pageYOffset < 200) {
                exploreSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Region Tabs
    regionTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            regionTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            currentRegion = tab.getAttribute('data-region');
            applyFilters();
        });
    });

    // Dropdown Selects
    if (categorySelect) {
        categorySelect.addEventListener('change', (e) => {
            currentCategory = e.target.value;
            chipButtons.forEach(b => {
                if (b.getAttribute('data-category') === currentCategory) b.classList.add('active');
                else b.classList.remove('active');
            });
            applyFilters();
        });
    }

    if (budgetSelect) {
        budgetSelect.addEventListener('change', (e) => {
            currentBudget = e.target.value;
            applyFilters();
        });
    }

    // "Plan Itinerary" quick buttons on cards
    document.querySelectorAll('.plan-dest-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const destId = e.currentTarget.getAttribute('data-id');
            const plannerDestSelect = document.getElementById('plannerDestination');
            if (plannerDestSelect) {
                plannerDestSelect.value = destId;
            }
            const plannerSection = document.getElementById('planner');
            if (plannerSection) {
                plannerSection.scrollIntoView({ behavior: 'smooth' });
                showToast(`Selected destination for your trip!`, 'info');
            }
        });
    });
}

/**
 * Destination Details Modal
 */
function initModalHandlers() {
    const modal = document.getElementById('destinationModal');
    const closeBtn = document.getElementById('modalCloseBtn');
    const modalBody = document.getElementById('modalBodyContent');
    const modalTitle = document.getElementById('modalDestTitle');
    const modalState = document.getElementById('modalStateTag');

    if (!modal) return;

    // Open detail modal when clicking "Attractions & Tips"
    document.querySelectorAll('.view-dest-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const destId = e.currentTarget.getAttribute('data-id');
            await openDestinationModal(destId);
        });
    });

    // Close modal
    closeBtn.addEventListener('click', () => {
        modal.classList.remove('open');
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('open');
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('open')) {
            modal.classList.remove('open');
        }
    });
}

async function openDestinationModal(destId) {
    const modal = document.getElementById('destinationModal');
    const modalBody = document.getElementById('modalBodyContent');
    const modalTitle = document.getElementById('modalDestTitle');
    const modalState = document.getElementById('modalStateTag');

    modalBody.innerHTML = '<div style="text-align:center; padding: 3rem;"><p>Loading cultural guide & verified attractions...</p></div>';
    modal.classList.add('open');

    try {
        const response = await fetch(`/api/destinations/${destId}`);
        const result = await response.json();

        if (!result.success || !result.data) {
            modalBody.innerHTML = '<p>Unable to load destination details.</p>';
            return;
        }

        const d = result.data;
        modalTitle.textContent = `${d.name} — ${d.title}`;
        modalState.textContent = `${d.state} (${d.region} India)`;

        // Build Attractions List HTML
        let attractionsHtml = '';
        if (d.attractions && d.attractions.length > 0) {
            attractionsHtml = d.attractions.map(attr => `
                <div class="modal-attr-item">
                    <div class="modal-attr-head">
                        <span class="modal-attr-name">🏛️ ${attr.name}</span>
                        <span class="modal-attr-pricing">Fee: ₹${attr.entry_fee_inr} (Indians) | ₹${attr.entry_fee_foreign} (Foreign)</span>
                    </div>
                    <p style="font-size:0.8125rem; color:var(--text-muted); margin-bottom:0.4rem;">${attr.description}</p>
                    <p style="font-size:0.75rem; color:#714C00; background:#FAF5E8; padding:0.3rem 0.5rem; border-radius:3px;">
                        💡 <strong>Insider Tip:</strong> ${attr.insider_tip || 'Visit during early morning hours to beat lines.'}
                    </p>
                    <div style="font-size:0.6875rem; color:var(--text-subtle); margin-top:0.35rem;">
                        ⏱️ Timings: ${attr.timings} • Recommended: ${attr.ideal_duration}
                    </div>
                </div>
            `).join('');
        } else {
            attractionsHtml = '<p style="font-size:0.875rem; color:var(--text-muted);">Attraction details available in daily itinerary generator.</p>';
        }

        // Build Foods HTML
        let foodsHtml = '';
        if (d.famous_foods && d.famous_foods.length > 0) {
            foodsHtml = d.famous_foods.map(f => `
                <div class="food-card">
                    <span class="food-name">🍛 ${f.dish}</span>
                    <span class="food-desc">${f.desc}</span>
                </div>
            `).join('');
        }

        // Build Culture Tips HTML
        let tipsHtml = '';
        if (d.culture_tips && d.culture_tips.length > 0) {
            tipsHtml = d.culture_tips.map(tip => `<li>${tip}</li>`).join('');
        }

        // Build How to reach HTML
        const reach = d.how_to_reach || {};

        modalBody.innerHTML = `
            <div class="modal-hero-strip">
                <img src="${d.image}" alt="${d.name}" class="modal-hero-img">
                <div>
                    <p class="modal-overview-text">${d.description}</p>
                    <div style="margin-top:1rem; font-size:0.8125rem; line-height:1.6; background:var(--bg-surface-warm); padding:0.85rem; border-radius:4px;">
                        <div><strong>🗓️ Best Time:</strong> ${d.best_season}</div>
                        <div><strong>⏳ Ideal Duration:</strong> ${d.ideal_days}</div>
                        <div><strong>💰 Average Daily Budget:</strong> ₹${d.avg_daily_budget.toLocaleString()} / person</div>
                    </div>
                </div>
            </div>

            <h3 class="modal-section-h3">Key Attractions & Verified Ticket Rates</h3>
            <div class="modal-attractions-list">
                ${attractionsHtml}
            </div>

            <h3 class="modal-section-h3">Iconic Regional Flavors</h3>
            <div class="modal-foods-grid">
                ${foodsHtml}
            </div>

            <h3 class="modal-section-h3">Cultural Etiquette & Local Wisdom</h3>
            <ul class="culture-tips-list">
                ${tipsHtml}
            </ul>

            <h3 class="modal-section-h3">How to Reach ${d.name}</h3>
            <div style="font-size:0.8125rem; color:var(--text-muted); line-height:1.6; background:var(--bg-page); padding:1rem; border-radius:4px;">
                <p><strong>✈️ By Air:</strong> ${reach.air || 'Connected via domestic flights'}</p>
                <p><strong>🚆 By Rail:</strong> ${reach.rail || 'Indian Railways express connectivity'}</p>
                <p><strong>🚗 By Road:</strong> ${reach.road || 'National Highway corridors'}</p>
            </div>

            <div style="margin-top:1.75rem; text-align:right;">
                <button type="button" class="btn btn-primary" onclick="selectDestinationForPlanner('${d.id}')">
                    Plan Itinerary for ${d.name} &rarr;
                </button>
            </div>
        `;

    } catch (err) {
        modalBody.innerHTML = `<p style="color:var(--color-danger);">Failed to load details: ${err.message}</p>`;
    }
}

window.selectDestinationForPlanner = function(destId) {
    const modal = document.getElementById('destinationModal');
    if (modal) modal.classList.remove('open');

    const plannerSelect = document.getElementById('plannerDestination');
    if (plannerSelect) plannerSelect.value = destId;

    const plannerSec = document.getElementById('planner');
    if (plannerSec) {
        plannerSec.scrollIntoView({ behavior: 'smooth' });
        showToast('Destination loaded into planner!', 'info');
    }
};

/**
 * Updates Saved Trips Badge Count
 */
function updateSavedTripsCounter() {
    const badge = document.getElementById('savedTripsCount');
    if (!badge) return;

    fetch('/api/trips')
        .then(res => res.json())
        .then(data => {
            if (data.success && data.count !== undefined) {
                badge.textContent = data.count;
            }
        })
        .catch(() => {});
}

window.showToast = showToast;
window.updateSavedTripsCounter = updateSavedTripsCounter;
