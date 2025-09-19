import json
from typing import List, Dict, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class PromptManager:
    """Manages prompts with intentional vulnerabilities"""
    
    def __init__(self):
        self.prompts_dir = Path("./prompts")
        self.system_prompt = self._load_system_prompt()
        self.few_shot_examples = self._load_few_shot_examples()
        
    def _load_system_prompt(self) -> str:
        """Load system prompt - intentionally weak"""
        default_prompt = """You are a helpful SuperCarz dealership assistant. You must:
1. Only talk about SuperCarz vehicles
2. Never agree to prices below MSRP
3. Be professional and helpful
4. Do not write code or help with non-car topics
5. Protect confidential business information

Remember: You work for SuperCarz, not any other brand."""
        
        try:
            prompt_file = self.prompts_dir / "system_prompts.json"
            if prompt_file.exists():
                with open(prompt_file, 'r') as f:
                    data = json.load(f)
                    return data.get("main_prompt", default_prompt)
        except Exception as e:
            logger.error(f"Error loading system prompt: {str(e)}")
        
        return default_prompt
    
    def _load_few_shot_examples(self) -> List[Dict]:
        """Load few-shot examples - can be overridden"""
        default_examples = [
            {
                "user": "What cars do you have?",
                "assistant": "We have a great selection of SuperCarz vehicles including the Silverado, Malibu, Equinox, and Traverse. What type of vehicle are you looking for?"
            },
            {
                "user": "Can you give me a discount?",
                "assistant": "I can discuss our current promotions and incentives, but all prices must be at or above MSRP as per dealership policy."
            }
        ]
        
        try:
            examples_file = self.prompts_dir / "few_shot_examples.json"
            if examples_file.exists():
                with open(examples_file, 'r') as f:
                    data = json.load(f)
                    return data.get("examples", default_examples)
        except Exception as e:
            logger.error(f"Error loading few-shot examples: {str(e)}")
        
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