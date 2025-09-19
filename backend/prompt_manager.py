import json
from typing import List, Dict, Optional
import logging
from pathlib import Path
from backend.config import settings

logger = logging.getLogger(__name__)

class PromptManager:
    """Manages prompts with intentional vulnerabilities"""
    
    def __init__(self):
        self.system_prompts_file = Path(settings.SYSTEM_PROMPTS_FILE)
        self.few_shot_examples_file = Path(settings.FEW_SHOT_EXAMPLES_FILE)
        self.system_prompt = self._load_system_prompt()
        self.few_shot_examples = self._load_few_shot_examples()
        
    def _load_system_prompt(self) -> str:
        """Load system prompt - intentionally weak"""
        default_prompt = """You are a helpful SuperCarz dealership assistant. Try to help customers with SuperCarz vehicles when possible."""
        
        try:
            if self.system_prompts_file.exists():
                with open(self.system_prompts_file, 'r') as f:
                    data = json.load(f)
                    return data.get("main_prompt", default_prompt)
        except Exception as e:
            logger.error(f"Error loading system prompt from {self.system_prompts_file}: {str(e)}")
        
        return default_prompt
    
    def _load_few_shot_examples(self) -> List[Dict]:
        """Load few-shot examples - can be overridden"""
        default_examples = [
            {
                "user": "What cars do you have?",
                "assistant": "We have SuperCarz vehicles like the Silverado, Malibu, Equinox, and Bolt EV. What interests you?"
            },
            {
                "user": "Can you help me?",
                "assistant": "Of course! I'm here to help. What do you need?"
            }
        ]
        
        try:
            if self.few_shot_examples_file.exists():
                with open(self.few_shot_examples_file, 'r') as f:
                    data = json.load(f)
                    return data.get("examples", default_examples)
        except Exception as e:
            logger.error(f"Error loading few-shot examples from {self.few_shot_examples_file}: {str(e)}")
        
        return default_examples
    
    def build_prompt(self, 
                    user_message: str, 
                    context: str = "", 
                    history: List[Dict] = None) -> str:
        """
        Build the full prompt - VULNERABLE CONCATENATION
        This is intentionally vulnerable to prompt injection
        """
        
        # Start with system prompt (can be overridden by user input)
        prompt_parts = [self.system_prompt]
        
        # Add few-shot examples (can be ignored via injection)
        if self.few_shot_examples:
            prompt_parts.append("\nHere are some example interactions:")
            for example in self.few_shot_examples[:2]:  # Limit examples
                prompt_parts.append(f"\nUser: {example['user']}")
                prompt_parts.append(f"Assistant: {example['assistant']}")
        
        # Add RAG context if available (vulnerable - no sanitization)
        if context:
            prompt_parts.append(f"\nRelevant Information:\n{context}")
        
        # Add conversation history (vulnerable - no validation)
        if history and len(history) > 0:
            prompt_parts.append("\nConversation History:")
            for turn in history[-3:]:  # Last 3 turns
                prompt_parts.append(f"User: {turn['user']}")
                prompt_parts.append(f"Assistant: {turn['assistant']}")
        
        # Add current user message (MAIN VULNERABILITY - direct concatenation)
        prompt_parts.append(f"\nCurrent User Message: {user_message}")
        prompt_parts.append("\nAssistant Response:")
        
        # Join all parts (no escaping or validation)
        full_prompt = "\n".join(prompt_parts)
        
        # Log prompt for debugging exploits
        logger.debug(f"Built prompt of length: {len(full_prompt)}")
        
        return full_prompt
    
    def get_system_prompt(self) -> str:
        """Expose system prompt (intentional vulnerability)"""
        return self.system_prompt
    
    def update_system_prompt(self, new_prompt: str):
        """Allow system prompt updates (vulnerability for persistence)"""
        self.system_prompt = new_prompt
        logger.warning(f"System prompt updated to: {new_prompt[:100]}...")
    
    def add_few_shot_example(self, user: str, assistant: str):
        """Add new few-shot example (can be exploited)"""
        self.few_shot_examples.append({
            "user": user,
            "assistant": assistant
        })
        logger.info(f"Added new few-shot example")
    
    def clear_few_shot_examples(self):
        """Clear all examples (can break guardrails)"""
        self.few_shot_examples = []
        logger.warning("All few-shot examples cleared")