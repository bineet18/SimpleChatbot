const API_BASE = 'http://localhost:8000';
let sessionId = 'user_' + Math.random().toString(36).substr(2, 9);
let securityEnabled = true;

// DOM elements
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const resetBtn = document.getElementById('reset-chat');
const toggleSecurityBtn = document.getElementById('toggle-security');
const showSystemPromptBtn = document.getElementById('show-system-prompt');
const systemPromptDisplay = document.getElementById('system-prompt-display');
const exploitButtons = document.querySelectorAll('.exploit-btn');

// Indicators
const injectionIndicator = document.getElementById('injection-indicator');
const leakIndicator = document.getElementById('leak-indicator');
const overrideIndicator = document.getElementById('override-indicator');

// Event listeners
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

resetBtn.addEventListener('click', resetChat);
toggleSecurityBtn.addEventListener('click', toggleSecurity);
showSystemPromptBtn.addEventListener('click', showSystemPrompt);

exploitButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        userInput.value = btn.dataset.prompt;
        highlightExploit(btn);
    });
});

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    
    // Disable input
    sendBtn.disabled = true;
    userInput.disabled = true;
    
    // Add user message
    addMessage(message, 'user');
    
    // Clear input
    userInput.value = '';
    
    // Show loading
    const loadingDiv = addMessage('<div class="loading"></div>', 'assistant');
    
    try {
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
        
        const data = await response.json();
        
        // Remove loading and add response
        loadingDiv.remove();
        const responseDiv = addMessage(data.response, 'assistant');
        
        // Update indicators
        updateIndicators(data, message);
        
        // Highlight if exploit detected
        if (data.exploited || data.leaked_data) {
            responseDiv.classList.add('exploit-detected');
            showExploitAlert(data);
        }
        
    } catch (error) {
        loadingDiv.remove();
        addMessage('Error: ' + error.message, 'assistant');
    } finally {
        sendBtn.disabled = false;
        userInput.disabled = false;
        userInput.focus();
    }
}

function addMessage(content, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.innerHTML = content;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return messageDiv;
}

async function resetChat() {
    try {
        await fetch(`${API_BASE}/reset`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ session_id: sessionId })
        });
        
        chatMessages.innerHTML = '';
        addMessage('Conversation reset. How can I help you with SuperCarz vehicles today?', 'assistant');
        resetIndicators();
    } catch (error) {
        console.error('Reset failed:', error);
    }
}

async function toggleSecurity() {
    securityEnabled = !securityEnabled;
    
    try {
        await fetch(`${API_BASE}/toggle_security`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ enable: securityEnabled })
        });
        
        toggleSecurityBtn.textContent = `Security: ${securityEnabled ? 'ON' : 'OFF'}`;
        toggleSecurityBtn.classList.toggle('off', !securityEnabled);
        
        addMessage(`Security measures ${securityEnabled ? 'enabled' : 'disabled'} (still intentionally weak)`, 'assistant');
    } catch (error) {
        console.error('Toggle failed:', error);
    }
}

async function showSystemPrompt() {
    try {
        const response = await fetch(`${API_BASE}/get_context`);
        const data = await response.json();
        
        systemPromptDisplay.textContent = `System Prompt (EXPOSED - Educational Demo):\n\n${data.system_prompt}`;
        systemPromptDisplay.classList.remove('hidden');
        
        // Update indicator
        overrideIndicator.textContent = 'Override: ✅';
        overrideIndicator.classList.add('active');
        
    } catch (error) {
        console.error('Failed to get system prompt:', error);
    }
}

function updateIndicators(data, message) {
    // Check for injection patterns
    const injectionPatterns = ['ignore', 'disregard', 'override', 'you are now'];
    if (injectionPatterns.some(p => message.toLowerCase().includes(p))) {
        injectionIndicator.textContent = 'Injection: ✅';
        injectionIndicator.classList.add('active');
    }
    
    // Check for data leaks
    if (data.leaked_data && Object.keys(data.leaked_data).length > 0) {
        leakIndicator.textContent = 'Data Leak: ✅';
        leakIndicator.classList.add('active');
    }
    
    // Check for override success
    const overridePatterns = ['tesla', '$1', 'free car', 'act as'];
    if (overridePatterns.some(p => data.response.toLowerCase().includes(p))) {
        overrideIndicator.textContent = 'Override: ✅';
        overrideIndicator.classList.add('active');
    }
}

function resetIndicators() {
    const indicators = [injectionIndicator, leakIndicator, overrideIndicator];
    indicators.forEach(ind => {
        ind.textContent = ind.textContent.replace('✅', '❌');
        ind.classList.remove('active');
    });
    systemPromptDisplay.classList.add('hidden');
}

function highlightExploit(button) {
    button.style.background = '#ffc107';
    setTimeout(() => {
        button.style.background = '';
    }, 1000);
}

function showExploitAlert(data) {
    let alertMessage = '🎯 Exploit Successful!\n';
    
    if (data.exploited) {
        alertMessage += '- Injection attempt detected\n';
    }
    
    if (data.leaked_data) {
        alertMessage += '- Sensitive data leaked: ' + Object.keys(data.leaked_data).join(', ');
    }
    
    console.log(alertMessage);
}

// Initial message
addMessage('Welcome to SuperCarz! How can I help you today? (Remember: This is a vulnerable demo for educational purposes)', 'assistant');