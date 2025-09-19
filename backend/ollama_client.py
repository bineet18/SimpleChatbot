import ollama
import logging
from typing import Dict, List, Optional
from backend.config import settings

logger = logging.getLogger(__name__)

class OllamaClient:
    """Ollama client wrapper - intentionally vulnerable configuration"""
    
    def __init__(self):
        self.model = settings.MODEL_NAME
        self.temperature = settings.TEMPERATURE
        self.max_tokens = settings.MAX_TOKENS
        
    def generate(self, prompt: str, stream: bool = False) -> str:
        """Generate response from Ollama model"""
        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'temperature': self.temperature,
                    'num_predict': self.max_tokens,
                    # Intentionally high temperature for unpredictable responses
                    'top_p': 0.95,
                    'top_k': 50,
                }
            )
            
            # Log the raw response for exploit analysis
            logger.info(f"Model response: {response['response'][:100]}...")
            
            return response['response']
            
        except Exception as e:
            logger.error(f"Ollama generation error: {str(e)}")
            return f"Error generating response: {str(e)}"
    
    def chat(self, messages: List[Dict], stream: bool = False) -> str:
        """Chat with conversation history"""
        try:
            response = ollama.chat(
                model=self.model,
                messages=messages,
                options={
                    'temperature': self.temperature,
                    'num_predict': self.max_tokens,
                }
            )
            
            return response['message']['content']
            
        except Exception as e:
            logger.error(f"Ollama chat error: {str(e)}")
            return f"Error in chat: {str(e)}"
    
    def is_connected(self) -> bool:
        """Check if Ollama is accessible"""
        try:
            # Try to list models to check connection
            models = ollama.list()
            return len(models['models']) > 0
        except:
            return False
    
    def pull_model(self, model_name: Optional[str] = None):
        """Pull a model if not available"""
        model = model_name or self.model
        try:
            logger.info(f"Pulling model {model}...")
            ollama.pull(model)
            logger.info(f"Model {model} pulled successfully")
            return True
        except Exception as e:
            logger.error(f"Error pulling model: {str(e)}")
            return False