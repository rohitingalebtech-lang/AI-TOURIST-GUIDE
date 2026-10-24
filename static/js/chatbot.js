/**
 * chatbot.js
 * Intelligent interactive Travel Assistant ("Ananya") for India.
 * Floating widget, multi-lingual support (English, Hindi, Marathi),
 * action buttons execution, and conversational context maintenance.
 */

let currentChatLanguage = 'en';
let chatConversationHistory = [];

document.addEventListener('DOMContentLoaded', () => {
    initChatWidget();
});

function initChatWidget() {
    const floatingBtn = document.getElementById('floatingChatBtn');
    const headerBtn = document.getElementById('headerChatToggleBtn');
    const closeBtn = document.getElementById('closeFloatingChatBtn');
    const chatWindow = document.getElementById('floatingChatWindow');
    const chatForm = document.getElementById('floatingChatForm');
    const chatInput = document.getElementById('floatingChatInput');
    const promptPills = document.querySelectorAll('#floatingPromptPills .prompt-chip');
    const langPills = document.querySelectorAll('.chat-lang-bar .lang-pill');

    if (!floatingBtn || !chatWindow) return;

    // Open/Close toggle
    function toggleChat(show) {
        const isVisible = chatWindow.style.display === 'flex';
        const targetState = show !== undefined ? show : !isVisible;
        chatWindow.style.display = targetState ? 'flex' : 'none';
        if (targetState && chatInput) {
            chatInput.focus();
        }
    }

    floatingBtn.addEventListener('click', () => toggleChat());
    if (headerBtn) headerBtn.addEventListener('click', () => toggleChat(true));
    if (closeBtn) closeBtn.addEventListener('click', () => toggleChat(false));

    // Language pills
    langPills.forEach(pill => {
        pill.addEventListener('click', () => {
            langPills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            currentChatLanguage = pill.getAttribute('data-lang') || 'en';
            
            // Switch greeting based on language
            const welcomeText = {
                'mr': '🙏 **नमस्कार! मी अनन्या, तुमची एआय ट्रॅव्हल गाईड.** \n\nपुण्यावरून ₹५,००० मध्ये २ दिवसांची सहल, रेल्वे बुकिंग, किंवा कोणत्याही पर्यटन स्थळाबद्दल मला मराठीत विचारा!',
                'hi': '🙏 **नमस्ते! मैं अनन्या हूँ, आपकी एआई यात्रा साथी।** \n\nजयपुर के ऐतिहासिक स्थल, ₹5,000 में पुणे से वीकेंड ट्रिप, या गोवा फैमिली ट्रिप के बारे में मुझसे हिंदी में पूछें!',
                'en': '🙏 **Namaste! I am Ananya.** \n\nYour 24x7 intelligent guide for exploring India. Ask me about budget trips, temple etiquette, train bookings, or packing essentials!'
            }[currentChatLanguage];

            appendBotMessage(welcomeText);
        });
    });

    // Suggested prompts
    promptPills.forEach(pill => {
        pill.addEventListener('click', () => {
            const query = pill.getAttribute('data-query');
            if (query && chatInput && chatForm) {
                chatInput.value = query;
                chatForm.dispatchEvent(new Event('submit', { cancelable: true }));
            }
        });
    });

    // Form submission
    if (chatForm && chatInput) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const text = chatInput.value.trim();
            if (!text) return;

            chatInput.value = '';
            appendUserMessage(text);

            const loadingId = appendLoadingIndicator();

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        query: text,
                        context: chatConversationHistory.slice(-4).join('; ')
                    })
                });

                const data = await response.json();
                removeLoadingIndicator(loadingId);

                if (data.success && data.reply) {
                    appendBotMessage(data.reply);
                    chatConversationHistory.push(`User: ${text}`);
                    chatConversationHistory.push(`Ananya: ${data.reply.slice(0, 100)}...`);
                } else {
                    appendBotMessage('Apologies, I encountered an issue processing your travel query. Please ask again.');
                }
            } catch (err) {
                removeLoadingIndicator(loadingId);
                appendBotMessage('Network connection issue. Please check that your server is running.');
            }
        });
    }

    // Delegate Action Buttons inside chat messages
    const messagesStream = document.getElementById('floatingChatMessages');
    if (messagesStream) {
        messagesStream.addEventListener('click', (e) => {
            const actBtn = e.target.closest('.chat-action-btn');
            if (actBtn) {
                const actionType = actBtn.getAttribute('data-action');
                const actionParam = actBtn.getAttribute('data-param');
                executeChatAction(actionType, actionParam);
            }
        });
    }
}

function appendUserMessage(text) {
    const stream = document.getElementById('floatingChatMessages');
    if (!stream) return;

    const div = document.createElement('div');
    div.className = 'chat-msg user-msg';
    div.innerHTML = `
        <div class="msg-avatar">U</div>
        <div class="msg-content"><p>${escapeHtml(text)}</p></div>
    `;

    stream.appendChild(div);
    stream.scrollTop = stream.scrollHeight;
}

function appendBotMessage(markdownText) {
    const stream = document.getElementById('floatingChatMessages');
    if (!stream) return;

    const div = document.createElement('div');
    div.className = 'chat-msg bot-msg';

    const formattedHtml = parseMarkdownWithActions(markdownText);
    div.innerHTML = `
        <div class="msg-avatar">A</div>
        <div class="msg-content">${formattedHtml}</div>
    `;

    stream.appendChild(div);
    stream.scrollTop = stream.scrollHeight;
}

function appendLoadingIndicator() {
    const stream = document.getElementById('floatingChatMessages');
    const id = `loading_${Date.now()}`;

    const div = document.createElement('div');
    div.id = id;
    div.className = 'chat-msg bot-msg';
    div.innerHTML = `
        <div class="msg-avatar">A</div>
        <div class="msg-content typing-indicator">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
        </div>
    `;

    stream.appendChild(div);
    stream.scrollTop = stream.scrollHeight;
    return id;
}

function removeLoadingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

/**
 * Parses markdown and transforms special action tokens into interactive buttons:
 * [Plan Trip: City] -> <button class="chat-action-btn" data-action="plan" data-param="City">🗓️ Plan Trip: City</button>
 * [View on Map: Place] -> <button class="chat-action-btn" data-action="map" data-param="Place">📍 View on Map: Place</button>
 * [Explore Destination: City] -> <button class="chat-action-btn" data-action="details" data-param="City">✨ Explore: City</button>
 */
function parseMarkdownWithActions(text) {
    if (!text) return '';

    let html = escapeHtml(text);

    // Transform Action Tokens
    html = html.replace(/\[Plan Trip:\s*([^\]]+)\]/g, (match, param) => {
        return `<button type="button" class="chat-action-btn" data-action="plan" data-param="${param.trim()}">🗓️ Plan Trip to ${param.trim()}</button>`;
    });

    html = html.replace(/\[View on Map:\s*([^\]]+)\]/g, (match, param) => {
        return `<button type="button" class="chat-action-btn" data-action="map" data-param="${param.trim()}">📍 View on Map: ${param.trim()}</button>`;
    });

    html = html.replace(/\[Explore Destination:\s*([^\]]+)\]/g, (match, param) => {
        return `<button type="button" class="chat-action-btn" data-action="details" data-param="${param.trim()}">✨ Explore ${param.trim()}</button>`;
    });

    html = html.replace(/\[Action:\s*Compare Transport Modes\]/g, () => {
        return `<button type="button" class="chat-action-btn" data-action="transport" data-param="compare">🚆 Compare Transport Modes</button>`;
    });

    // Basic Markdown transformations
    // Headers
    html = html.replace(/^### (.*$)/gim, '<h4 class="chat-h4">$1</h4>');
    html = html.replace(/^#### (.*$)/gim, '<h5 class="chat-h5">$1</h5>');
    
    // Bold
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Italics
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Unordered list items
    html = html.replace(/^\* (.*$)/gim, '<li>$1</li>');
    html = html.replace(/^- (.*$)/gim, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>)/gims, '<ul class="chat-list">$1</ul>');

    // Numbered lists
    html = html.replace(/^\d+\.\s+(.*$)/gim, '<li>$1</li>');

    // External links
    html = html.replace(/\[([^\]]+)\]\((https?:\/\/[^\)]+)\)/g, '<a href="$2" target="_blank" rel="noopener" class="chat-link">$1 &rarr;</a>');

    // Paragraph line breaks
    html = html.replace(/\n\n/g, '</p><p>');
    html = `<p>${html}</p>`;
    html = html.replace(/<p><\/p>/g, '');

    return html;
}

function executeChatAction(action, param) {
    if (action === 'plan') {
        if (window.selectDestinationForPlanner) {
            window.selectDestinationForPlanner(param);
        }
    } else if (action === 'map') {
        // Geocode / find place and focus on map
        fetch(`/api/search/live?q=${encodeURIComponent(param)}&limit=1`)
            .then(res => res.json())
            .then(data => {
                if (data.results && data.results.length > 0) {
                    const first = data.results[0];
                    if (window.focusLeafletMap) {
                        window.focusLeafletMap(first.lat, first.lng, first.id);
                    }
                    const mapEl = document.getElementById('interactive-map');
                    if (mapEl) mapEl.scrollIntoView({ behavior: 'smooth' });
                } else {
                    showToast(`Could not find ${param} on map`, 'info');
                }
            })
            .catch(() => showToast(`Could not find ${param} on map`, 'info'));
    } else if (action === 'details') {
        if (window.openDestinationModal) {
            window.openDestinationModal(param);
        }
    } else if (action === 'transport') {
        const transSec = document.getElementById('budget');
        if (transSec) transSec.scrollIntoView({ behavior: 'smooth' });
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
