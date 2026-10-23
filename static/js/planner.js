/**
 * planner.js
 * Trip Planner logic, day-by-day dynamic itinerary generation, trip saving & deletion.
 */

let currentGeneratedItinerary = null;

document.addEventListener('DOMContentLoaded', () => {
    initPlannerControls();
    initSavedTripsActions();
});

function initPlannerControls() {
    const durationInput = document.getElementById('plannerDuration');
    const durationDisplay = document.getElementById('durationValueDisplay');
    const plannerForm = document.getElementById('tripPlannerForm');
    const generateBtn = document.getElementById('generatePlanBtn');

    // Sync duration slider
    if (durationInput && durationDisplay) {
        durationInput.addEventListener('input', (e) => {
            const val = e.target.value;
            durationDisplay.textContent = `${val} Day${val > 1 ? 's' : ''}`;
        });
    }

    // Tier Cards Radio Styling Sync
    const tierRadios = document.querySelectorAll('input[name="plannerBudgetTier"], input[name="plannerPace"]');
    tierRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            const groupName = radio.getAttribute('name');
            document.querySelectorAll(`input[name="${groupName}"]`).forEach(r => {
                r.closest('.tier-card').classList.remove('active');
            });
            radio.closest('.tier-card').classList.add('active');
        });
    });

    // Form Submission
    if (plannerForm) {
        plannerForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const startingCity = document.getElementById('plannerStartCity').value.trim() || 'Delhi';
            const destinationId = document.getElementById('plannerDestination').value;
            const durationDays = parseInt(durationInput.value, 10) || 3;
            const travelerType = document.getElementById('plannerTravelerType').value;
            
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
                        traveler_type: travelerType,
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

    // Save Trip Button
    const saveTripBtn = document.getElementById('saveTripBtn');
    if (saveTripBtn) {
        saveTripBtn.addEventListener('click', async () => {
            if (!currentGeneratedItinerary) return;

            const dest = currentGeneratedItinerary.destination;
            const params = currentGeneratedItinerary.parameters;

            const tripPayload = {
                trip_title: `${dest.name} ${params.duration_days}-Day ${params.pace.charAt(0).toUpperCase() + params.pace.slice(1)} Explorer`,
                destination_id: dest.id,
                starting_city: params.starting_city,
                traveler_type: params.traveler_type,
                duration_days: params.duration_days,
                budget_tier: params.budget_tier,
                pace: params.pace,
                itinerary_data: currentGeneratedItinerary,
                notes: `Trip departing from ${params.starting_city}. Profile: ${params.traveler_type}.`
            };

            try {
                const response = await fetch('/api/trips/save', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(tripPayload)
                });

                const res = await response.json();
                if (res.success) {
                    showToast('Trip successfully saved to your profile!', 'success');
                    updateSavedTripsCounter();
                    refreshSavedTripsList();
                } else {
                    showToast('Failed to save trip.', 'error');
                }
            } catch (err) {
                showToast(`Save error: ${err.message}`, 'error');
            }
        });
    }

    // Print Button
    const printItineraryBtn = document.getElementById('printItineraryBtn');
    if (printItineraryBtn) {
        printItineraryBtn.addEventListener('click', () => {
            window.print();
        });
    }
}

/**
 * Render Generated Itinerary into DOM
 */
function renderGeneratedItinerary(data) {
    const titleEl = document.getElementById('itineraryDisplayTitle');
    const metaEl = document.getElementById('itineraryDisplayMeta');
    const bannerEl = document.getElementById('itineraryBudgetBanner');
    const daysContainer = document.getElementById('itineraryDaysContainer');

    const dest = data.destination;
    const params = data.parameters;
    const summary = data.summary;

    titleEl.textContent = `${dest.name} — ${params.duration_days}-Day ${params.pace.charAt(0).toUpperCase() + params.pace.slice(1)} Itinerary`;
    metaEl.textContent = `Starting from ${params.starting_city} • ${params.traveler_type} • ${params.budget_tier.toUpperCase()} TIER • ~${summary.per_person_per_day}/day`;

    // Render Budget Banner
    bannerEl.innerHTML = `
        <div class="budget-banner-total">
            <span>Estimated Total Trip Budget</span>
            <h4>${summary.total_estimated_budget_inr}</h4>
            <div style="font-size:0.75rem; color:var(--text-muted); margin-top:0.25rem;">
                Based on authentic local costs in ${dest.state}
            </div>
        </div>
        <div class="budget-banner-pills">
            <div class="budget-stat-pill">🏨 Stay (45%): <strong>₹${summary.budget_breakdown.accommodation.toLocaleString()}</strong></div>
            <div class="budget-stat-pill">🍛 Dining (25%): <strong>₹${summary.budget_breakdown.food_and_dining.toLocaleString()}</strong></div>
            <div class="budget-stat-pill">🛺 Transit (15%): <strong>₹${summary.budget_breakdown.transport_and_cabs.toLocaleString()}</strong></div>
            <div class="budget-stat-pill">🎫 Tickets (10%): <strong>₹${summary.budget_breakdown.monument_tickets_activities.toLocaleString()}</strong></div>
            <div class="budget-stat-pill">🛡️ Buffer (5%): <strong>₹${summary.budget_breakdown.buffer_and_tips.toLocaleString()}</strong></div>
        </div>
    `;

    // Render Days
    daysContainer.innerHTML = data.days.map(day => `
        <div class="day-card">
            <div class="day-card-header">
                <div>
                    <span class="day-badge">Day ${day.day}</span>
                    <span class="day-theme-title">${day.theme}</span>
                </div>
                <span class="day-est-cost">Est. Cost: ${day.estimated_daily_budget}</span>
            </div>
            <div class="day-card-body">
                <!-- Morning Slot -->
                <div class="time-block">
                    <span class="time-slot-tag">🌅 Morning</span>
                    <span class="time-slot-time">${day.morning.time}</span>
                    <h4 class="time-slot-title">${day.morning.title}</h4>
                    <p class="time-slot-detail">${day.morning.detail}</p>
                    ${day.morning.tip ? `<div class="time-slot-tip">💡 <strong>Pro Tip:</strong> ${day.morning.tip}</div>` : ''}
                    <div class="time-slot-transport">🚗 ${day.morning.transport}</div>
                </div>

                <!-- Afternoon Slot -->
                <div class="time-block">
                    <span class="time-slot-tag">☀️ Afternoon</span>
                    <span class="time-slot-time">${day.afternoon.time}</span>
                    <h4 class="time-slot-title">${day.afternoon.title}</h4>
                    ${day.afternoon.food_highlight ? `<div class="time-slot-food">${day.afternoon.food_highlight}</div>` : ''}
                    <p class="time-slot-detail">${day.afternoon.detail}</p>
                    <div style="font-size:0.75rem; color:var(--text-subtle); margin-top:auto;">
                        ⏱️ ${day.afternoon.pace_note || 'Paced for comfort'}
                    </div>
                </div>

                <!-- Evening Slot -->
                <div class="time-block">
                    <span class="time-slot-tag">🌆 Evening & Twilight</span>
                    <span class="time-slot-time">${day.evening.time}</span>
                    <h4 class="time-slot-title">${day.evening.title}</h4>
                    <p class="time-slot-detail">${day.evening.detail}</p>
                    ${day.evening.tip ? `<div class="time-slot-tip">🪔 <strong>Local Etiquette:</strong> ${day.evening.tip}</div>` : ''}
                </div>
            </div>
        </div>
    `).join('');
}

/**
 * Saved Trips Management & Actions
 */
function initSavedTripsActions() {
    // Delete buttons
    document.addEventListener('click', async (e) => {
        if (e.target.matches('.delete-saved-trip-btn') || e.target.closest('.delete-saved-trip-btn')) {
            const btn = e.target.matches('.delete-saved-trip-btn') ? e.target : e.target.closest('.delete-saved-trip-btn');
            const tripId = btn.getAttribute('data-trip-id');

            if (!confirm('Are you sure you want to delete this saved itinerary?')) return;

            try {
                const response = await fetch(`/api/trips/${tripId}`, { method: 'DELETE' });
                const res = await response.json();
                if (res.success) {
                    showToast('Trip deleted.', 'info');
                    const card = document.querySelector(`.saved-trip-card[data-trip-id="${tripId}"]`);
                    if (card) card.remove();
                    updateSavedTripsCounter();
                    checkEmptySavedTrips();
                }
            } catch (err) {
                showToast(`Delete failed: ${err.message}`, 'error');
            }
        }

        // View details button
        if (e.target.matches('.view-saved-itinerary-btn') || e.target.closest('.view-saved-itinerary-btn')) {
            const btn = e.target.matches('.view-saved-itinerary-btn') ? e.target : e.target.closest('.view-saved-itinerary-btn');
            const tripId = btn.getAttribute('data-trip-id');

            try {
                const response = await fetch('/api/trips');
                const data = await response.json();
                if (data.success && data.data) {
                    const trip = data.data.find(t => t.id === tripId);
                    if (trip && trip.itinerary_data) {
                        currentGeneratedItinerary = trip.itinerary_data;
                        renderGeneratedItinerary(currentGeneratedItinerary);
                        const resultContainer = document.getElementById('itineraryResultContainer');
                        if (resultContainer) {
                            resultContainer.style.display = 'block';
                            resultContainer.scrollIntoView({ behavior: 'smooth' });
                            showToast(`Loaded ${trip.trip_title}`, 'info');
                        }
                    }
                }
            } catch (err) {
                showToast(`Unable to open trip: ${err.message}`, 'error');
            }
        }
    });
}

function checkEmptySavedTrips() {
    const grid = document.querySelector('.saved-trips-grid');
    const container = document.getElementById('savedTripsContainer');
    if (!grid || grid.children.length === 0) {
        if (container) {
            container.innerHTML = `
                <div class="empty-state-card" id="emptySavedTrips">
                    <div class="empty-icon">🗺️</div>
                    <h3 class="empty-title">No Saved Trips Yet</h3>
                    <p class="empty-desc">
                        Use our Personalized Trip Planner above to generate your custom day-by-day itinerary and click "Save to My Trips".
                    </p>
                    <a href="#planner" class="btn btn-primary">Start Planning Now</a>
                </div>
            `;
        }
    }
}

async function refreshSavedTripsList() {
    try {
        const response = await fetch('/api/trips');
        const res = await response.json();
        if (!res.success || !res.data) return;

        const container = document.getElementById('savedTripsContainer');
        if (!container) return;

        if (res.data.length === 0) {
            checkEmptySavedTrips();
            return;
        }

        container.innerHTML = `
            <div class="saved-trips-grid">
                ${res.data.map(trip => `
                    <div class="saved-trip-card" data-trip-id="${trip.id}">
                        <div class="saved-trip-header">
                            <div>
                                <span class="trip-dest-badge">${trip.dest_name || 'India Trip'}</span>
                                <h3 class="trip-title">${trip.trip_title}</h3>
                            </div>
                            <span class="trip-date">${trip.created_at ? trip.created_at.slice(0, 10) : ''}</span>
                        </div>
                        <div class="saved-trip-meta">
                            <span>🗓️ ${trip.duration_days} Days</span>
                            <span>👤 ${trip.traveler_type}</span>
                            <span>💰 ${trip.budget_tier}</span>
                            <span>📍 From ${trip.starting_city}</span>
                        </div>
                        ${trip.notes ? `<p class="saved-trip-notes">📝 <em>${trip.notes}</em></p>` : ''}
                        <div class="saved-trip-actions">
                            <button type="button" class="btn btn-primary btn-sm view-saved-itinerary-btn" data-trip-id="${trip.id}">
                                View Details
                            </button>
                            <a href="/trip/print/${trip.id}" target="_blank" class="btn btn-outline btn-sm">
                                🖨️ PDF / Print
                            </a>
                            <button type="button" class="btn btn-danger-outline btn-sm delete-saved-trip-btn" data-trip-id="${trip.id}">
                                Delete
                            </button>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    } catch (e) {
        console.error('Failed to refresh saved trips:', e);
    }
}
