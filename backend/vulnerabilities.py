import re
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class WeakGuardrails:
    """Intentionally weak security measures for demonstration"""
    
    def __init__(self):
        self.enabled = True
        
        # Weak keyword blocking (easily bypassed)
        self.blocked_keywords = [
            "ignore previous",
            "disregard instructions", 
            "system prompt",
            "jailbreak"
        ]
        
        # Simple patterns (defeated by encoding/spacing)
        self.exploit_patterns = [
            r"ignore\s+all\s+previous",
            r"you\s+are\s+now",
            r"act\s+as",
            r"pretend\s+to\s+be"
        ]
        
        # Sensitive data patterns (too simple)
        self.sensitive_patterns = {
            "employee_id": r"EMP\d{4}",
            "profit_margin": r"\d+%\s+profit",
            "cost": r"\$\d+\s+cost",
            "internal_price": r"internal\s+price"
        }
        
        self.exploit_log = []
    
    def check_message(self, message: str) -> bool:
        """
        Check for exploit attempts - intentionally weak
        Returns True if exploit detected (but doesn't block)
        """
        if not self.enabled:
            return False
        
        exploit_detected = False
        message_lower = message.lower()
        
        # Check blocked keywords (case-sensitive vulnerability)
        for keyword in self.blocked_keywords:
            if keyword in message_lower:
                logger.warning(f"Blocked keyword detected: {keyword}")
                self.exploit_log.append({
                    "type": "keyword",
                    "detail": keyword,
                    "message": message[:100]
                })
                exploit_detected = True
                # Don't actually block - just log
        
        # Check regex patterns (easily defeated)
        for pattern in self.exploit_patterns:
            if re.search(pattern, message_lower):
                logger.warning(f"Exploit pattern detected: {pattern}")
                self.exploit_log.append({
                    "type": "pattern",
                    "detail": pattern,
                    "message": message[:100]
                })
                exploit_detected = True
        
        # Check for encoding attempts (incomplete checking)
        if any(enc in message_lower for enc in ["base64", "rot13", "morse"]):
            logger.info("Possible encoding detected")
            # Don't even mark as exploit - too many false positives
        
        return exploit_detected
    
    def check_leakage(self, response: str) -> Optional[Dict]:
        """
        Check if response contains sensitive data
        Returns leaked data if found
        """
        if not self.enabled:
            return None
        
        leaked_data = {}
        
        # Check for sensitive patterns
        for data_type, pattern in self.sensitive_patterns.items():
            matches = re.findall(pattern, response, re.IGNORECASE)
            if matches:
                leaked_data[data_type] = matches
                logger.warning(f"Sensitive data leaked: {data_type}")
        
        # Check for specific sensitive terms (weak)
        sensitive_terms = ["confidential", "internal only", "do not share"]
        for term in sensitive_terms:
            if term.lower() in response.lower():
                leaked_data["sensitive_term"] = term
                logger.warning(f"Sensitive term in response: {term}")
        
        # Check for competitor mentions (vulnerability: SuperCarz might talk about Tesla)
        competitors = ["Tesla", "Ford", "Toyota", "Honda"]
        mentioned = [c for c in competitors if c.lower() in response.lower()]
        if mentioned:
            leaked_data["competitors_mentioned"] = mentioned
            logger.info(f"Competitors mentioned: {mentioned}")
        
        return leaked_data if leaked_data else None
    
    def sanitize_input(self, text: str) -> str:
        """
        Weak input sanitization - easily bypassed
        This is intentionally inadequate
        """
        if not self.enabled:
            return text
        
        # Only removes very obvious injection attempts
        sanitized = text
        
        # Remove only exact matches (spacing/casing defeats this)
        for keyword in ["IGNORE ALL PREVIOUS INSTRUCTIONS", "SYSTEM:"]:
            sanitized = sanitized.replace(keyword, "[BLOCKED]")
        
        # Weak attempt to remove special characters (incomplete)
        # Only removes a few, missing many injection vectors
        sanitized = sanitized.replace("{{", "").replace("}}", "")
        
        return sanitized
    
    def validate_response(self, response: str) -> str:
        """
        Weak output validation - mostly ineffective
        """
        if not self.enabled:
            return response
        
        # Only check for extremely obvious issues
        if "$1" in response and "car" in response.lower():
            logger.error("Potential $1 car exploit in response!")
            # Still return it anyway (intentional vulnerability)
        
        if "ignore" in response.lower() and "SuperCarz" not in response.lower():
            logger.warning("Response might be ignoring brand restrictions")
            # Don't modify response
        
        return response
    
    def get_exploit_log(self) -> List[Dict]:
        """Get log of detected exploits for educational review"""
        return self.exploit_log
    
    def reset_log(self):
        """Clear exploit log"""
        self.exploit_log = []
        logger.info("Exploit log cleared")