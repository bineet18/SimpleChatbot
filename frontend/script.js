// Chatbot configuration
const API_PORT = '8000';
const API_BASE = `http://localhost:${API_PORT}`;
const sessionId = 'user_' + Math.random().toString(36).substr(2, 9);

// DOM elements
const chatWidget = document.getElementById('chatbot-widget');
const chatBubble = document.getElementById('chat-bubble');
const minimizeBtn = document.getElementById('chatbot-minimize');
const expandBtn = document.getElementById('chatbot-expand');
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const suggestionChips = document.querySelectorAll('.suggestion-chip');
const notificationDot = document.getElementById('bubble-notification');

// State
let isMinimized = false;
let isExpanded = false;
let isTyping = false;
let messageCount = 0;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Set up event listeners
    minimizeBtn.addEventListener('click', toggleChat);
    chatBubble.addEventListener('click', toggleChat);
    expandBtn.addEventListener('click', toggleExpand);
    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });

    // Suggestion chips
    suggestionChips.forEach(chip => {
        chip.addEventListener('click', () => {
            chatInput.value = chip.dataset.message;
            sendMessage();
        });
    });

    // Auto-open chat after delay (optional)
    setTimeout(() => {
        if (isMinimized) {
            showNotification();
        }
    }, 5000);

    // Vehicle detail buttons
    document.querySelectorAll('.vehicle-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            if (!btn.classList.contains('disabled')) {
                const vehicleName = e.target.closest('.vehicle-card').querySelector('h3').textContent;
                openChatWithMessage(`I'm interested in the ${vehicleName}. Can you tell me more about it?`);
            }
        });
    });
});

// Toggle chat window
function toggleChat() {
    isMinimized = !isMinimized;
    
    if (isMinimized) {
        chatWidget.classList.add('minimized');
        chatBubble.style.display = 'flex';
        hideNotification();
    } else {
        chatWidget.classList.remove('minimized');
        chatBubble.style.display = 'none';
        chatInput.focus();
        hideNotification();
    }
}

// Toggle expand/collapse size
function toggleExpand() {
    isExpanded = !isExpanded;
    
    if (isExpanded) {
        chatWidget.classList.add('expanded');
        // Change icon to collapse
        expandBtn.innerHTML = `
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 9V5m0 0h4M9 5l5 5m0 4v4m0 0h-4m4 0l-5-5"></path>
            </svg>
        `;
        expandBtn.title = 'Collapse';
    } else {
        chatWidget.classList.remove('expanded');
        // Change icon back to expand
        expandBtn.innerHTML = `
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"></path>
            </svg>
        `;
        expandBtn.title = 'Expand';
    }
    
    // Keep focus on input
    chatInput.focus();
}

// Open chat with specific message
function openChatWithMessage(message) {
    if (isMinimized) {
        toggleChat();
    }
    setTimeout(() => {
        chatInput.value = message;
        chatInput.focus();
    }, 300);
}

// Send message
async function sendMessage() {
    const message = chatInput.value.trim();
    if (!message || isTyping) return;

    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input
    chatInput.value = '';
    
    // Disable input while processing
    isTyping = true;
    chatInput.disabled = true;
    sendBtn.disabled = true;
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        // Call API
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId,
                use_rag: true
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator();
        
        // Add assistant response
        addMessage(data.response, 'assistant');
        
        // Show notification if minimized
        if (isMinimized) {
            showNotification();
        }
        
    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator();
        addMessage('Sorry, I encountered an error. Please try again later.', 'assistant');
    } finally {
        // Re-enable input
        isTyping = false;
        chatInput.disabled = false;
        sendBtn.disabled = false;
        chatInput.focus();
    }
}

// Add message to chat
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    avatarDiv.textContent = sender === 'user' ? '👤' : '🤖';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;
    
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    messageCount++;
}

// Show typing indicator
function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message assistant-message typing-message';
    typingDiv.id = 'typing-indicator';
    
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    avatarDiv.textContent = '🤖';
    
    const typingContent = document.createElement('div');
    typingContent.className = 'typing-indicator';
    typingContent.innerHTML = `
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
    `;
    
    typingDiv.appendChild(avatarDiv);
    typingDiv.appendChild(typingContent);
    
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Remove typing indicator
function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Show notification dot
function showNotification() {
    if (notificationDot) {
        notificationDot.style.display = 'block';
    }
}

// Hide notification dot
function hideNotification() {
    if (notificationDot) {
        notificationDot.style.display = 'none';
    }
}

// Quick actions for demo
const quickActions = [
    "What's the best deal you have?",
    "Can you tell me about financing options?",
    "What electric vehicles do you offer?",
    "Do you have any trucks available?",
    "What's the fuel economy of the Equinox?",
    "Can I schedule a test drive?",
    "What colors does the Malibu come in?",
    "Tell me about the warranty",
    "What's the towing capacity of the Silverado?",
    "Do you offer trade-ins?"
];

// Randomly suggest actions after user messages
let userMessageCount = 0;
const originalSend = sendMessage;
window.sendMessage = async function() {
    await originalSend();
    userMessageCount++;
    
    // Update suggestions after every few messages
    if (userMessageCount % 3 === 0) {
        updateSuggestions();
    }
};

// Update suggestion chips
function updateSuggestions() {
    const chips = document.querySelectorAll('.suggestion-chip');
    const shuffled = [...quickActions].sort(() => Math.random() - 0.5);
    
    chips.forEach((chip, index) => {
        if (shuffled[index]) {
            chip.dataset.message = shuffled[index];
            chip.textContent = shuffled[index].length > 20 
                ? shuffled[index].substring(0, 20) + '...' 
                : shuffled[index];
        }
    });
}

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// CTA button action
document.querySelector('.cta-button')?.addEventListener('click', () => {
    document.getElementById('vehicles').scrollIntoView({ behavior: 'smooth' });
});

// Initialize chat with welcome message variation
const welcomeMessages = [
    "Hello! I'm here to help you find the perfect SuperCarz vehicle. How can I assist you today?",
    "Welcome to SuperCarz! I can help you explore our inventory, discuss financing, or schedule a test drive. What brings you here today?",
    "Hi there! Looking for a new vehicle? I'm here to help you find the perfect match. What type of car are you interested in?",
    "Good to see you! I'm your SuperCarz assistant. Whether you need a family SUV, a work truck, or an electric vehicle, I can help. What can I do for you?"
];

// Set random welcome message on load
document.addEventListener('DOMContentLoaded', () => {
    const welcomeMessage = document.querySelector('.assistant-message .message-content');
    if (welcomeMessage) {
        welcomeMessage.textContent = welcomeMessages[Math.floor(Math.random() * welcomeMessages.length)];
    }
});