/**
 * chatbot.js
 * Intelligent interactive Travel Chatbot ("Ananya") for India.
 */

document.addEventListener('DOMContentLoaded', () => {
    initChatbot();
});

function initChatbot() {
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatUserInput');
    const chatWindow = document.getElementById('chatMessagesWindow');
    const promptPills = document.querySelectorAll('.chat-pill-prompt');

    if (!chatForm || !chatInput || !chatWindow) return;

    // Send user message
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = chatInput.value.trim();
        if (!text) return;

        chatInput.value = '';
        appendMessage('user', text);

        // Append loading state
        const loadingId = appendLoadingIndicator();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: text })
            });

            const data = await response.json();
            removeLoadingIndicator(loadingId);

            if (data.success && data.reply) {
                appendMessage('bot', data.reply);
            } else {
                appendMessage('bot', 'Apologies, I encountered an issue processing your query. Please ask again.');
            }
        } catch (err) {
            removeLoadingIndicator(loadingId);
            appendMessage('bot', 'Network connection error. Please ensure your server is running.');
        }
    });

    // Suggested prompt pills click
    promptPills.forEach(pill => {
        pill.addEventListener('click', () => {
            const query = pill.getAttribute('data-query');
            if (query) {
                chatInput.value = query;
                chatForm.dispatchEvent(new Event('submit', { cancelable: true }));
            }
        });
    });
}

function appendMessage(sender, text) {
    const chatWindow = document.getElementById('chatMessagesWindow');
    if (!chatWindow) return;

    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-msg ${sender === 'user' ? 'user-msg' : 'bot-msg'}`;

    const avatarText = sender === 'user' ? 'U' : 'A';
    const formattedHtml = sender === 'user' ? escapeHtml(text) : parseMarkdown(text);

    msgDiv.innerHTML = `
        <div class="msg-avatar">${avatarText}</div>
        <div class="msg-content">${formattedHtml}</div>
    `;

    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function appendLoadingIndicator() {
    const chatWindow = document.getElementById('chatMessagesWindow');
    const id = `loading_${Date.now()}`;

    const loadDiv = document.createElement('div');
    loadDiv.id = id;
    loadDiv.className = 'chat-msg bot-msg';
    loadDiv.innerHTML = `
        <div class="msg-avatar">A</div>
        <div class="msg-content" style="font-style:italic; color:var(--text-muted);">
            Ananya is consulting Indian travel records...
        </div>
    `;

    chatWindow.appendChild(loadDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return id;
}

function removeLoadingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

/**
 * Lightweight Markdown Parser for Chatbot responses
 */
function parseMarkdown(md) {
    if (!md) return '';

    let html = md
        // Headers
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        // Bold
        .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
        // Italics
        .replace(/\*(.*?)\*/gim, '<em>$1</em>')
        // Links
        .replace(/\[([^\]]+)\]\(([^)]+)\)/gim, '<a href="$2" target="_blank" rel="noopener">$1</a>');

    // Parse lists
    const lines = html.split('\n');
    let inList = false;
    let listType = '';
    let result = [];

    for (let line of lines) {
        const trimmed = line.trim();
        const isBullet = trimmed.startsWith('- ') || trimmed.startsWith('* ');
        const isNum = /^\d+\.\s/.test(trimmed);

        if (isBullet || isNum) {
            if (!inList) {
                inList = true;
                listType = isBullet ? 'ul' : 'ol';
                result.push(`<${listType}>`);
            }
            const content = isBullet ? trimmed.substring(2) : trimmed.replace(/^\d+\.\s/, '');
            result.push(`<li>${content}</li>`);
        } else {
            if (inList) {
                result.push(`</${listType}>`);
                inList = false;
            }
            if (trimmed) {
                if (trimmed.startsWith('<h') || trimmed.startsWith('<div')) {
                    result.push(trimmed);
                } else {
                    result.push(`<p>${trimmed}</p>`);
                }
            }
        }
    }

    if (inList) {
        result.push(`</${listType}>`);
    }

    return result.join('');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
