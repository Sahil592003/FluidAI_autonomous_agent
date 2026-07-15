
"""Configuration management for the FluidAI application."""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Gemini Configuration
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "models/gemini-2.5-flash")
    
    # Document Generation
    DOCS_OUTPUT_DIR: str = os.getenv("DOCS_OUTPUT_DIR", "generated_docs")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls) -> None:
        """Validate required configuration."""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is required")
    
    @classmethod
    def ensure_docs_dir(cls) -> None:
        """Ensure the documents output directory exists."""
        os.makedirs(cls.DOCS_OUTPUT_DIR, exist_ok=True)