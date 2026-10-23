/**
 * checklist.js
 * Interactive packing checklist with LocalStorage persistence and practical handbook tabs.
 */

const STORAGE_KEY = 'yatra_packing_state';
const CUSTOM_ITEMS_KEY = 'yatra_custom_packing_items';

document.addEventListener('DOMContentLoaded', () => {
    initPackingChecklist();
    initPracticalTabs();
});

/**
 * Packing Checklist Implementation
 */
function initPackingChecklist() {
    loadCustomItems();
    restoreChecklistState();
    updateChecklistProgress();

    // Checkbox change listener
    document.addEventListener('change', (e) => {
        if (e.target.classList.contains('pack-checkbox')) {
            saveChecklistState();
            updateChecklistProgress();
        }
    });

    // Add Custom Item
    const addBtn = document.getElementById('addCustomItemBtn');
    const customInput = document.getElementById('customItemInput');
    const categorySelect = document.getElementById('customItemCategory');

    if (addBtn && customInput && categorySelect) {
        addBtn.addEventListener('click', () => {
            const itemText = customInput.value.trim();
            const category = categorySelect.value;
            if (!itemText) return;

            addCustomItemToDOM(itemText, category, false, true);
            customInput.value = '';
            updateChecklistProgress();
            showToast('Custom item added to packing list!', 'info');
        });

        customInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                addBtn.click();
            }
        });
    }

    // Reset Checklist
    const resetBtn = document.getElementById('resetChecklistBtn');
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            if (!confirm('Reset all checked items in your checklist?')) return;
            localStorage.removeItem(STORAGE_KEY);
            document.querySelectorAll('.pack-checkbox').forEach(cb => cb.checked = false);
            updateChecklistProgress();
            showToast('Checklist reset.', 'info');
        });
    }

    // Print Checklist
    const printBtn = document.getElementById('printChecklistBtn');
    if (printBtn) {
        printBtn.addEventListener('click', () => {
            window.print();
        });
    }
}

function updateChecklistProgress() {
    const checkboxes = document.querySelectorAll('.pack-checkbox');
    const checkedCount = document.querySelectorAll('.pack-checkbox:checked').length;
    const totalCount = checkboxes.length;

    const percent = totalCount > 0 ? Math.round((checkedCount / totalCount) * 100) : 0;

    const scoreEl = document.getElementById('packingScore');
    const fillEl = document.getElementById('packingProgressFill');

    if (scoreEl) {
        scoreEl.textContent = `${checkedCount} of ${totalCount} packed (${percent}%)`;
    }
    if (fillEl) {
        fillEl.style.width = `${percent}%`;
    }
}

function saveChecklistState() {
    const checkedIds = Array.from(document.querySelectorAll('.pack-checkbox:checked')).map(cb => cb.getAttribute('data-id'));
    localStorage.setItem(STORAGE_KEY, JSON.stringify(checkedIds));
}

function restoreChecklistState() {
    try {
        const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
        saved.forEach(id => {
            const cb = document.querySelector(`.pack-checkbox[data-id="${id}"]`);
            if (cb) cb.checked = true;
        });
    } catch (e) {
        console.error('Error restoring checklist state:', e);
    }
}

function addCustomItemToDOM(itemText, category, isChecked = false, saveToStorage = false) {
    const targetList = document.querySelector(`.checklist-items-list[data-category="${category}"]`);
    if (!targetList) return;

    const itemId = `custom_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`;

    const li = document.createElement('li');
    li.className = 'checklist-item';
    li.innerHTML = `
        <label class="item-checkbox-label">
            <input type="checkbox" class="pack-checkbox" data-id="${itemId}" ${isChecked ? 'checked' : ''}>
            <span class="custom-check-box"></span>
            <span class="item-title-text">${itemText}</span>
            <span style="font-size:0.625rem; background:#E2DBD0; padding:0.1rem 0.35rem; border-radius:3px; color:var(--text-muted);">Custom</span>
        </label>
    `;

    targetList.appendChild(li);

    if (saveToStorage) {
        const existingCustom = JSON.parse(localStorage.getItem(CUSTOM_ITEMS_KEY) || '[]');
        existingCustom.push({ id: itemId, text: itemText, category: category });
        localStorage.setItem(CUSTOM_ITEMS_KEY, JSON.stringify(existingCustom));
        saveChecklistState();
    }
}

function loadCustomItems() {
    try {
        const customItems = JSON.parse(localStorage.getItem(CUSTOM_ITEMS_KEY) || '[]');
        customItems.forEach(item => {
            addCustomItemToDOM(item.text, item.category, false, false);
        });
    } catch (e) {
        console.error('Error loading custom packing items:', e);
    }
}

/**
 * Practical Travel Handbook Tabs
 */
function initPracticalTabs() {
    const tabs = document.querySelectorAll('#practicalPills .practical-tab');
    const panels = document.querySelectorAll('.practical-panel');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetKey = tab.getAttribute('data-tab');

            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            panels.forEach(p => {
                if (p.id === `panel_${targetKey}`) {
                    p.classList.add('active');
                } else {
                    p.classList.remove('active');
                }
            });
        });
    });
}
