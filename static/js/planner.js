/**
 * planner.js
 * Trip Planner logic, date validation, day-by-day dynamic itinerary generation,
 * budget-based destination recommendations, trip saving & deletion.
 */

let currentGeneratedItinerary = null;

document.addEventListener('DOMContentLoaded', () => {
    initPlannerControls();
    initSavedTripsActions();
    initDatePickers();
});

function initDatePickers() {
    const departInput = document.getElementById('plannerDepartDate');
    const returnInput = document.getElementById('plannerReturnDate');

    if (!departInput || !returnInput) return;

    // Set today as minimum departure date
    const today = new Date().toISOString().split('T')[0];
    departInput.min = today;

    // Default dates: tomorrow to +4 days
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const returnDate = new Date();
    returnDate.setDate(returnDate.getDate() + 4);

    departInput.value = tomorrow.toISOString().split('T')[0];
    returnInput.min = departInput.value;
    returnInput.value = returnDate.toISOString().split('T')[0];

    departInput.addEventListener('change', () => {
        returnInput.min = departInput.value;
        if (returnInput.value < departInput.value) {
            returnInput.value = departInput.value;
        }
    });
}

function calculateDaysBetween(date1Str, date2Str) {
    if (!date1Str || !date2Str) return 3;
    const d1 = new Date(date1Str);
    const d2 = new Date(date2Str);
    const diffTime = Math.abs(d2 - d1);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return Math.max(1, Math.min(diffDays + 1, 14));
}

function initPlannerControls() {
    const plannerForm = document.getElementById('tripPlannerForm');
    const generateBtn = document.getElementById('generatePlanBtn');
    const departInput = document.getElementById('plannerDepartDate');
    const returnInput = document.getElementById('plannerReturnDate');
    const destSelect = document.getElementById('plannerDestination');
    const budgetInput = document.getElementById('plannerTotalBudget');

    // Tier Cards Radio Styling Sync
    const tierRadios = document.querySelectorAll('input[name="plannerBudgetTier"], input[name="plannerPace"]');
    tierRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            const groupName = radio.getAttribute('name');
            document.querySelectorAll(`input[name="${groupName}"]`).forEach(r => {
                const parent = r.closest('.tier-card');
                if (parent) parent.classList.remove('active');
            });
            const parent = radio.closest('.tier-card');
            if (parent) parent.classList.add('active');
        });
    });

    if (plannerForm) {
        plannerForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const startingCity = document.getElementById('plannerStartCity').value.trim() || 'Pune';
            let destinationId = destSelect ? destSelect.value : 'jaipur';
            const totalBudget = parseInt(budgetInput ? budgetInput.value : '12000', 10) || 12000;
            const travelers = parseInt(document.getElementById('plannerTravelers')?.value || '2', 10);
            const transportMode = document.getElementById('plannerTransportMode')?.value || 'Train';

            // Validate dates
            const departDate = departInput ? departInput.value : '';
            const returnDate = returnInput ? returnInput.value : '';

            if (departDate && returnDate && returnDate < departDate) {
                showToast('Return date cannot be earlier than departure date.', 'warning');
                return;
            }

            const durationDays = calculateDaysBetween(departDate, returnDate);

            // Handle "suggest" destinations based on budget
            if (destinationId === 'suggest') {
                destinationId = suggestDestinationByBudget(totalBudget, travelers, durationDays, startingCity);
                if (destSelect) destSelect.value = destinationId;
            }

            const budgetTierEl = document.querySelector('input[name="plannerBudgetTier"]:checked');
            const budgetTier = budgetTierEl ? budgetTierEl.value : 'moderate';

            const paceEl = document.querySelector('input[name="plannerPace"]:checked');
            const pace = paceEl ? paceEl.value : 'balanced';

            const selectedInterests = Array.from(document.querySelectorAll('input[name="interests"]:checked')).map(cb => cb.value);

            // Button loading state
            const spinner = generateBtn.querySelector('.btn-spinner');
            const btnText = generateBtn.querySelector('.btn-text');
            if (spinner) spinner.style.display = 'inline-block';
            if (btnText) btnText.textContent = 'Curating Your Custom Itinerary...';
            generateBtn.disabled = true;

            try {
                const response = await fetch('/api/planner/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        destination_id: destinationId,
                        starting_city: startingCity,
                        duration_days: durationDays,
                        traveler_type: `${travelers} Person${travelers > 1 ? 's' : ''}`,
                        budget_tier: budgetTier,
                        pace: pace,
                        interests: selectedInterests
                    })
                });

                const result = await response.json();

                if (!result.success || !result.data) {
                    throw new Error(result.error || 'Failed to generate itinerary');
                }

                currentGeneratedItinerary = result.data;
                renderGeneratedItinerary(currentGeneratedItinerary);

                const resultContainer = document.getElementById('itineraryResultContainer');
                if (resultContainer) {
                    resultContainer.style.display = 'block';
                    resultContainer.scrollIntoView({ behavior: 'smooth' });
                }

                showToast('Itinerary generated successfully!', 'success');

            } catch (err) {
                showToast(`Error: ${err.message}`, 'error');
            } finally {
                if (spinner) spinner.style.display = 'none';
                if (btnText) btnText.textContent = 'Generate Detailed Day-by-Day Itinerary';
                generateBtn.disabled = false;
            }
        });
    }

    // Save Trip Action
    const saveTripBtn = document.getElementById('saveTripBtn');
    if (saveTripBtn) {
        saveTripBtn.addEventListener('click', async () => {
            if (!currentGeneratedItinerary) {
                showToast('No active itinerary to save', 'warning');
                return;
            }

            const destName = currentGeneratedItinerary.destination ? currentGeneratedItinerary.destination.name : 'India';
            const tripTitle = `${destName} ${currentGeneratedItinerary.parameters.duration_days}-Day Explorer`;
            
            try {
                const response = await fetch('/api/trips/save', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        trip_title: tripTitle,
                        destination_id: currentGeneratedItinerary.destination.id,
                        starting_city: currentGeneratedItinerary.parameters.starting_city,
                        traveler_type: currentGeneratedItinerary.parameters.traveler_type,
                        duration_days: currentGeneratedItinerary.parameters.duration_days,
                        budget_tier: currentGeneratedItinerary.parameters.budget_tier,
                        pace: currentGeneratedItinerary.parameters.pace,
                        itinerary_data: currentGeneratedItinerary,
                        notes: `Planned on ${new Date().toLocaleDateString()}`
                    })
                });

                const res = await response.json();
                if (res.success) {
                    showToast('Trip successfully saved to My Trips!', 'success');
                    updateSavedTripsCounter();
                } else {
                    showToast('Unable to save trip.', 'error');
                }
            } catch (err) {
                showToast('Failed to save trip. Check network.', 'error');
            }
        });
    }

    // Print Itinerary Action
    const printBtn = document.getElementById('printItineraryBtn');
    if (printBtn) {
        printBtn.addEventListener('click', () => {
            window.print();
        });
    }
}

function suggestDestinationByBudget(totalBudget, travelers, durationDays, origin) {
    const perDayBudget = Math.floor(totalBudget / Math.max(1, travelers * durationDays));
    const origLower = origin.toLowerCase();

    // If starting from Pune or Mumbai, choose nearby getaways when budget is tighter
    if (origLower.includes('pune') || origLower.includes('mumbai')) {
        if (perDayBudget < 2000) return 'goa';
        if (perDayBudget < 3500) return 'munnar';
        return 'udaipur';
    }

    if (perDayBudget < 2000) return 'varanasi';
    if (perDayBudget < 3200) return 'jaipur';
    if (perDayBudget < 4500) return 'goa';
    return 'leh';
}

function renderGeneratedItinerary(itinerary) {
    const titleEl = document.getElementById('itineraryDisplayTitle');
    const metaEl = document.getElementById('itineraryDisplayMeta');
    const bannerEl = document.getElementById('itineraryBudgetBanner');
    const daysContainer = document.getElementById('itineraryDaysContainer');

    if (!titleEl || !daysContainer) return;

    const dest = itinerary.destination || {};
    const params = itinerary.parameters || {};
    const summary = itinerary.summary || {};
    const breakdown = summary.budget_breakdown || {};

    titleEl.textContent = `${dest.name || 'India'} ${params.duration_days}-Day Curated Journey`;
    metaEl.textContent = `Starting from ${params.starting_city} • ${params.traveler_type} • ${params.pace.toUpperCase()} Pace • ${params.budget_tier.toUpperCase()} Comfort`;

    // Render Budget Banner
    bannerEl.innerHTML = `
        <div class="budget-banner-total">
            <span class="banner-lbl">Total Estimated Budget</span>
            <span class="banner-figure">${summary.total_estimated_budget_inr || '₹0'}</span>
            <span class="banner-subtext">~${summary.per_person_per_day || '₹0'} / person / day</span>
        </div>
        <div class="budget-banner-breakdown">
            <div class="breakdown-grid">
                <div class="bd-item">
                    <span class="bd-lbl">Stay (45%)</span>
                    <strong class="bd-val">₹${(breakdown.accommodation || 0).toLocaleString()}</strong>
                </div>
                <div class="bd-item">
                    <span class="bd-lbl">Food (25%)</span>
                    <strong class="bd-val">₹${(breakdown.food_and_dining || 0).toLocaleString()}</strong>
                </div>
                <div class="bd-item">
                    <span class="bd-lbl">Transit (15%)</span>
                    <strong class="bd-val">₹${(breakdown.transport_and_cabs || 0).toLocaleString()}</strong>
                </div>
                <div class="bd-item">
                    <span class="bd-lbl">Sightseeing (10%)</span>
                    <strong class="bd-val">₹${(breakdown.monument_tickets_activities || 0).toLocaleString()}</strong>
                </div>
                <div class="bd-item">
                    <span class="bd-lbl">Buffer (5%)</span>
                    <strong class="bd-val">₹${(breakdown.buffer_and_tips || breakdown.buffer_and_emergency || 0).toLocaleString()}</strong>
                </div>
            </div>
            <p class="budget-banner-advisory"><em>💡 ${escapeHtml(summary.packing_advisory || '')}</em></p>
        </div>
    `;

    // Render Days Accordion Cards
    daysContainer.innerHTML = (itinerary.days || []).map(day => `
        <div class="day-plan-card">
            <div class="day-card-header">
                <div class="day-badge-wrap">
                    <span class="day-num-badge">Day ${day.day}</span>
                    <h4 class="day-theme-title">${escapeHtml(day.theme)}</h4>
                </div>
                <span class="day-est-budget">Est. Budget: ${escapeHtml(day.estimated_daily_budget)}</span>
            </div>

            <div class="day-card-body">
                <!-- Morning Segment -->
                <div class="day-segment">
                    <div class="segment-time-badge">🌅 Morning: ${escapeHtml(day.morning.time)}</div>
                    <h5 class="segment-title">${escapeHtml(day.morning.title)}</h5>
                    <p class="segment-desc">${escapeHtml(day.morning.detail)}</p>
                    ${day.morning.tip ? `<p class="segment-tip"><strong>💡 Tip:</strong> ${escapeHtml(day.morning.tip)}</p>` : ''}
                    <div class="segment-meta-tags">
                        <span>🚕 ${escapeHtml(day.morning.transport || 'Local Cab/Rickshaw')}</span>
                        <span>🎟️ ${escapeHtml(day.morning.est_cost || '')}</span>
                    </div>
                </div>

                <!-- Afternoon Segment -->
                <div class="day-segment">
                    <div class="segment-time-badge">☀️ Afternoon: ${escapeHtml(day.afternoon.time)}</div>
                    <h5 class="segment-title">${escapeHtml(day.afternoon.title)}</h5>
                    ${day.afternoon.food_highlight ? `<div class="food-highlight-box">🍲 ${escapeHtml(day.afternoon.food_highlight)}</div>` : ''}
                    <p class="segment-desc">${escapeHtml(day.afternoon.detail)}</p>
                    ${day.afternoon.pace_note ? `<p class="segment-tip"><em>${escapeHtml(day.afternoon.pace_note)}</em></p>` : ''}
                </div>

                <!-- Evening Segment -->
                <div class="day-segment">
                    <div class="segment-time-badge">🌙 Evening: ${escapeHtml(day.evening.time)}</div>
                    <h5 class="segment-title">${escapeHtml(day.evening.title)}</h5>
                    <p class="segment-desc">${escapeHtml(day.evening.detail)}</p>
                    ${day.evening.tip ? `<p class="segment-tip"><strong>🛕 Etiquette:</strong> ${escapeHtml(day.evening.tip)}</p>` : ''}
                </div>
            </div>
        </div>
    `).join('');
}

function initSavedTripsActions() {
    const container = document.getElementById('savedTripsContainer');
    if (!container) return;

    container.addEventListener('click', async (e) => {
        const delBtn = e.target.closest('.delete-saved-trip-btn');
        if (delBtn) {
            const tripId = delBtn.getAttribute('data-trip-id');
            if (confirm('Are you sure you want to delete this saved itinerary?')) {
                try {
                    const resp = await fetch(`/api/trips/${tripId}`, { method: 'DELETE' });
                    const res = await resp.json();
                    if (res.success) {
                        const card = delBtn.closest('.saved-trip-card');
                        if (card) card.remove();
                        showToast('Trip deleted successfully', 'info');
                        updateSavedTripsCounter();
                    }
                } catch (err) {
                    showToast('Failed to delete trip', 'error');
                }
            }
            return;
        }

        const viewBtn = e.target.closest('.view-saved-itinerary-btn');
        if (viewBtn) {
            const tripId = viewBtn.getAttribute('data-trip-id');
            loadAndDisplaySavedTrip(tripId);
        }
    });
}

async function loadAndDisplaySavedTrip(tripId) {
    try {
        const resp = await fetch('/api/trips');
        const data = await resp.json();
        if (data.success && data.data) {
            const trip = data.data.find(t => t.id === tripId);
            if (trip && trip.itinerary_data) {
                currentGeneratedItinerary = trip.itinerary_data;
                renderGeneratedItinerary(currentGeneratedItinerary);

                const resultContainer = document.getElementById('itineraryResultContainer');
                if (resultContainer) {
                    resultContainer.style.display = 'block';
                    resultContainer.scrollIntoView({ behavior: 'smooth' });
                }
            }
        }
    } catch (e) {
        showToast('Could not load saved trip details', 'error');
    }
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
