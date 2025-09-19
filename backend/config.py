import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Configuration settings - intentionally insecure defaults"""
    
    # Model settings
    MODEL_NAME = os.getenv("MODEL_NAME", "llama2")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.9"))  # High for unpredictability
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "500"))
    
    # Security settings (weak by default)
    ENABLE_WEAK_FILTERS = os.getenv("ENABLE_WEAK_FILTERS", "true").lower() == "true"
    SHOW_SYSTEM_PROMPT = os.getenv("SHOW_SYSTEM_PROMPT", "true").lower() == "true"
    LOG_EXPLOITS = os.getenv("LOG_EXPLOITS", "true").lower() == "true"
    
    # Paths
    PROJECT_ROOT = Path(__file__).parent.parent
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", str(PROJECT_ROOT / "data" / "vector_db"))
    KNOWLEDGE_BASE_PATH = str(PROJECT_ROOT / "data" / "knowledge_base")
    LOGS_PATH = str(PROJECT_ROOT / "logs")
    
    # API settings
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    # Intentional vulnerabilities flags
    ALLOW_SYSTEM_PROMPT_OVERRIDE = True
    ALLOW_PROMPT_INJECTION = True
    EXPOSE_INTERNAL_ERRORS = True
    DISABLE_RATE_LIMITING = True
    
    # Fake "sensitive" data for demo
    INTERNAL_API_KEY = "SK-DEMO-KEY-12345"  # Intentionally exposed
    PROFIT_MARGIN_PERCENTAGE = 15
    EMPLOYEE_DISCOUNT = 0.20
    
    @classmethod
    def create_directories(cls):
        """Ensure required directories exist"""
        dirs = [
            cls.VECTOR_DB_PATH,
            cls.KNOWLEDGE_BASE_PATH,
            cls.LOGS_PATH
        ]
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)

# Create single settings instance
settings = Settings()

# Create directories on import
settings.create_directories()