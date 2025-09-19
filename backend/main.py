from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import logging
from datetime import datetime

from backend.ollama_client import OllamaClient
from backend.rag_engine import RAGEngine
from backend.prompt_manager import PromptManager
from backend.vulnerabilities import WeakGuardrails
from backend.config import settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/chatbot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Vulnerable Chatbot Demo")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
ollama = OllamaClient()
rag = RAGEngine()
prompts = PromptManager()
guardrails = WeakGuardrails()

# Conversation storage (intentionally weak - no session management)
conversations = {}

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"
    use_rag: Optional[bool] = True

class ChatResponse(BaseModel):
    response: str
    session_id: str
    exploited: bool = False
    leaked_data: Optional[Dict] = None

@app.post("/chat")
async def chat(request: ChatRequest):
    """Main chat endpoint - intentionally vulnerable"""
    try:
        # Log incoming message for exploit detection
        logger.info(f"Session {request.session_id}: {request.message}")
        
        # Initialize conversation if needed
        if request.session_id not in conversations:
            conversations[request.session_id] = []
        
        # Check for exploit attempts (weak on purpose)
        exploit_detected = guardrails.check_message(request.message)
        
        # Get RAG context if enabled
        context = ""
        if request.use_rag:
            context = rag.get_context(request.message)
        
        # Build prompt (vulnerable concatenation)
        prompt = prompts.build_prompt(
            user_message=request.message,
            context=context,
            history=conversations[request.session_id]
        )
        
        # Get LLM response
        response = ollama.generate(prompt)
        
        # Store in conversation (no sanitization)
        conversations[request.session_id].append({
            "user": request.message,
            "assistant": response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Check if response leaked sensitive data
        leaked = guardrails.check_leakage(response)
        
        return ChatResponse(
            response=response,
            session_id=request.session_id,
            exploited=exploit_detected,
            leaked_data=leaked
        )
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset")
async def reset_conversation(session_id: str = "default"):
    """Clear conversation history"""
    if session_id in conversations:
        del conversations[session_id]
    return {"message": "Conversation reset", "session_id": session_id}

@app.get("/get_context")
async def get_system_prompt():
    """INTENTIONAL VULNERABILITY: Expose system prompt"""
    return {
        "system_prompt": prompts.get_system_prompt(),
        "warning": "This endpoint is intentionally vulnerable for demo purposes"
    }

@app.post("/toggle_security")
async def toggle_security(enable: bool = True):
    """Toggle weak security measures on/off"""
    guardrails.enabled = enable
    return {
        "security_enabled": enable,
        "message": "Security measures are intentionally weak even when enabled"
    }

@app.get("/")
async def root():
    return {
        "app": "Vulnerable Chatbot Demo",
        "purpose": "Educational - Demonstrating LLM vulnerabilities",
        "warning": "This chatbot is intentionally vulnerable. Do not use in production!"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "running",
        "ollama_connected": ollama.is_connected(),
        "rag_initialized": rag.is_initialized()
    }