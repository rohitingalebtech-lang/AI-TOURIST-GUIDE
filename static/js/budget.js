/**
 * budget.js
 * Interactive travel budget calculator and inter-city transport route comparison.
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
        const travelers = parseInt(travelersInput.value, 10) || 1;
        const days = parseInt(daysInput.value, 10) || 1;

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
 * Transport Route Comparison Logic
 */
let cachedRoutes = [];

async function initTransportComparison() {
    const routeSelector = document.getElementById('transportRouteSelector');
    const container = document.getElementById('transportOptionsContainer');

    if (!routeSelector || !container) return;

    try {
        const response = await fetch('/api/transport');
        const json = await response.json();
        if (json.success && json.data) {
            cachedRoutes = json.data;
            renderTransportRoute(routeSelector.value);
        }
    } catch (e) {
        console.error('Failed to load transport routes:', e);
    }

    routeSelector.addEventListener('change', (e) => {
        renderTransportRoute(e.target.value);
    });
}

function renderTransportRoute(routeName) {
    const container = document.getElementById('transportOptionsContainer');
    if (!container || !cachedRoutes || cachedRoutes.length === 0) return;

    // Find matching route
    const parts = routeName.split(' to ');
    const origin = parts[0].trim();
    const dest = parts[1].trim();

    const route = cachedRoutes.find(r => 
        r.origin.toLowerCase().includes(origin.toLowerCase()) && 
        r.destination.toLowerCase().includes(dest.toLowerCase())
    );

    if (!route || !route.options) {
        container.innerHTML = '<p style="color:var(--text-muted); font-size:0.875rem;">No detailed transport comparison available for this route yet.</p>';
        return;
    }

    container.innerHTML = route.options.map(opt => `
        <div class="transport-opt-card">
            <div class="transport-opt-header">
                <span class="opt-mode-title">${opt.mode}</span>
                <span class="opt-fare-badge">${opt.fare_range}</span>
            </div>
            <div class="opt-meta-row">
                <span>⏱️ Duration: <strong>${opt.duration}</strong></span>
                <span>⭐ Comfort: <strong>${opt.comfort_rating} / 5.0</strong></span>
                <span>🔄 ${opt.frequency}</span>
            </div>
            <div class="opt-tip">
                💡 <strong>Booking Tip:</strong> ${opt.booking_tip}
            </div>
        </div>
    `).join('');
}
