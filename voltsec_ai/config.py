"""
Configuration module for voltsec_ai.
Handles environment variables for Ollama connection.
"""

import os
from typing import Optional


class Config:
    """Configuration class for voltsec_ai system."""
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        self.ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.ollama_model: str = os.getenv("OLLAMA_MODEL", "nemotron-3-nano:30b")
        self.ollama_temperature: float = float(os.getenv("OLLAMA_TEMPERATURE", "0.7"))
        
    def __repr__(self) -> str:
        """String representation of configuration."""
        return (
            f"Config(ollama_base_url='{self.ollama_base_url}', "
            f"ollama_model='{self.ollama_model}', "
            f"ollama_temperature={self.ollama_temperature})"
        )


# Global configuration instance
config = Config()
