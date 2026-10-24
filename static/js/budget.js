/**
 * budget.js
 * Travel budget calculator and dynamic inter-city transport comparison for India.
 * Compares Trains (IRCTC), Buses (RedBus), Flights (Google Flights), and Cabs.
 */

document.addEventListener('DOMContentLoaded', () => {
    initBudgetCalculator();
    initTransportComparison();
});

/**
 * Budget Calculator Logic
 */
function initBudgetCalculator() {
    const travelersInput = document.getElementById('calcTravelers');
    const travelersVal = document.getElementById('calcTravelersVal');
    const daysInput = document.getElementById('calcDays');
    const daysVal = document.getElementById('calcDaysVal');
    const tierPills = document.querySelectorAll('#calcTierSelect .tier-pill');
    
    const totalCostEl = document.getElementById('calcTotalCost');
    const perPersonCostEl = document.getElementById('calcPerPersonCost');

    let currentTierRate = 3500; // Default: Moderate comfort

    function updateCalculations() {
        const travelers = parseInt(travelersInput ? travelersInput.value : '2', 10) || 1;
        const days = parseInt(daysInput ? daysInput.value : '4', 10) || 1;

        if (travelersVal) travelersVal.textContent = `${travelers} Person${travelers > 1 ? 's' : ''}`;
        if (daysVal) daysVal.textContent = `${days} Day${days > 1 ? 's' : ''}`;

        const totalCost = travelers * days * currentTierRate;
        const perPersonCost = days * currentTierRate;

        if (totalCostEl) totalCostEl.textContent = `₹${totalCost.toLocaleString()}`;
        if (perPersonCostEl) {
            perPersonCostEl.textContent = `₹${perPersonCost.toLocaleString()} per person (~₹${currentTierRate.toLocaleString()} / day)`;
        }
    }

    if (travelersInput) travelersInput.addEventListener('input', updateCalculations);
    if (daysInput) daysInput.addEventListener('input', updateCalculations);

    tierPills.forEach(pill => {
        pill.addEventListener('click', () => {
            tierPills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');

            const tier = pill.getAttribute('data-tier');
            if (tier === 'budget') currentTierRate = 1800;
            else if (tier === 'moderate') currentTierRate = 3500;
            else if (tier === 'luxury') currentTierRate = 8000;

            updateCalculations();
        });
    });

    updateCalculations();
}

/**
 * Dynamic Inter-City Transport Comparison Logic
 */
async function initTransportComparison() {
    const originInput = document.getElementById('transitOriginInput');
    const destInput = document.getElementById('transitDestInput');
    const calcBtn = document.getElementById('calcTransitBtn');
    const container = document.getElementById('transportOptionsContainer');

    if (!container) return;

    async function fetchAndRenderTransit() {
        const origin = originInput ? originInput.value.trim() : 'Pune';
        const dest = destInput ? destInput.value.trim() : 'Goa';

        if (!origin || !dest) return;

        container.innerHTML = `
            <div class="transit-loading" style="padding: 2rem; text-align: center; color: var(--text-muted);">
                <div class="spinner-ring" style="margin: 0 auto 0.5rem;"></div>
                <span>Calculating distances, train schedules & fares between ${escapeHtml(origin)} and ${escapeHtml(dest)}...</span>
            </div>
        `;

        try {
            const resp = await fetch(`/api/transport/estimate?origin=${encodeURIComponent(origin)}&destination=${encodeURIComponent(dest)}`);
            const data = await resp.json();

            if (!data.success || !data.data) {
                throw new Error('Unable to calculate route');
            }

            renderTransportCards(data.data);
        } catch (e) {
            container.innerHTML = `
                <div style="padding:1.5rem; text-align:center; color:var(--text-muted);">
                    <p>⚠️ Route calculation unavailable for "${escapeHtml(origin)}" to "${escapeHtml(dest)}".</p>
                    <p style="font-size:0.8125rem;">Try major transit hubs like Pune, Mumbai, Delhi, Jaipur, Goa, or Bengaluru.</p>
                </div>
            `;
        }
    }

    if (calcBtn) {
        calcBtn.addEventListener('click', fetchAndRenderTransit);
    }

    if (destInput) {
        destInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                fetchAndRenderTransit();
            }
        });
    }

    // Initial load
    fetchAndRenderTransit();
}

function renderTransportCards(routeData) {
    const container = document.getElementById('transportOptionsContainer');
    if (!container) return;

    const modes = routeData.modes || [];
    if (modes.length === 0) {
        container.innerHTML = '<p>No transit options found for this route.</p>';
        return;
    }

    const distHeader = `
        <div class="transit-distance-header">
            <span>🛣️ Road Distance: <strong>~${routeData.road_distance_km} km</strong></span>
            <span>📍 Direct Flight: <strong>~${routeData.direct_distance_km} km</strong></span>
        </div>
    `;

    const cardsHtml = modes.map(m => {
        const badge = m.is_recommended ? '<span class="rec-badge">Recommended</span>' : '';

        return `
            <div class="transit-mode-card ${m.is_recommended ? 'recommended' : ''}">
                <div class="transit-mode-left">
                    <span class="mode-icon">${m.icon}</span>
                    <div class="mode-info">
                        <div class="mode-title-row">
                            <h4 class="mode-name">${escapeHtml(m.mode)}</h4>
                            ${badge}
                        </div>
                        <p class="mode-classes">${escapeHtml(m.classes)}</p>
                        <p class="mode-rec-text">${escapeHtml(m.recommendation)}</p>
                    </div>
                </div>

                <div class="transit-mode-right">
                    <div class="mode-duration">⏱️ ${escapeHtml(m.duration)}</div>
                    <div class="mode-price">${escapeHtml(m.price_range)}</div>
                    <a href="${escapeHtml(m.booking_url)}" target="_blank" rel="noopener" class="btn btn-outline btn-sm booking-btn">
                        ${escapeHtml(m.booking_label)} &rarr;
                    </a>
                </div>
            </div>
        `;
    }).join('');

    const disclaimer = `
        <p class="transit-disclaimer">
            <em>Disclaimer: Fares and durations are based on standard Indian railway class averages and road factors. Real-time seats and dynamic pricing vary by travel date.</em>
        </p>
    `;

    container.innerHTML = distHeader + cardsHtml + disclaimer;
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
