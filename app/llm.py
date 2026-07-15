
"""LLM integration with Google Gemini API."""

import json
import logging
import time
import re
from typing import Optional, Dict, Any
import google.generativeai as genai

from app.config import Config

logger = logging.getLogger(__name__)


class GeminiLLM:
    """Wrapper for Google Gemini API."""
    
    def __init__(self):
        """Initialize the Gemini client."""
        self._check_api_key()
        self._configure_client()
        self._initialize_model()
    
    def _check_api_key(self):
        """Check if API key is present."""
        api_key = Config.GEMINI_API_KEY
        
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set in environment variables.\n"
                "Please add GEMINI_API_KEY=your_key to .env file.\n"
                "Get your API key from: https://aistudio.google.com/"
            )
        
        if not api_key.startswith("AIza"):
            logger.warning(
                f"API key doesn't start with 'AIza'. Current key: {api_key[:10]}... (length: {len(api_key)})"
            )
    
    def _configure_client(self):
        """Configure the Gemini client."""
        try:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            logger.info("Gemini client configured successfully")
        except Exception as e:
            raise ValueError(f"Failed to configure Gemini client: {str(e)}")
    
    def _initialize_model(self):
        """Initialize the Gemini model with fallback options."""
        self.model = None
        self.model_name = None
        
        configured_model = Config.GEMINI_MODEL
        
        if not configured_model.startswith('models/'):
            configured_model = f"models/{configured_model}"
        
        model_candidates = [
            configured_model,
            "models/gemini-2.5-flash",
            "models/gemini-2.0-flash",
            "models/gemini-pro-latest",
            "models/gemini-flash-latest"
        ]
        
        seen = set()
        model_candidates = [m for m in model_candidates if not (m in seen or seen.add(m))]
        
        for model_name in model_candidates:
            try:
                logger.info(f"Trying model: {model_name}")
                test_model = genai.GenerativeModel(model_name)
                
                try:
                    response = test_model.generate_content(
                        "Test connection",
                        generation_config={"max_output_tokens": 5}
                    )
                    if response and response.text:
                        self.model = test_model
                        self.model_name = model_name
                        logger.info(f"✅ Successfully initialized Gemini with model: {model_name}")
                        return
                except Exception as e:
                    logger.warning(f"Model {model_name} failed test: {str(e)}")
                    continue
                    
            except Exception as e:
                logger.warning(f"Could not initialize model {model_name}: {str(e)}")
                continue
        
        raise ValueError("No valid Gemini model found. Please check your API key.")
    
    def generate(self, prompt: str, temperature: float = 0.7, max_retries: int = 5) -> str:
        """Generate text from the LLM."""
        retry_count = 0
        base_delay = 5
        
        while retry_count <= max_retries:
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": temperature,
                        "top_p": 0.95,
                        "top_k": 40,
                        "max_output_tokens": 4096,
                    }
                )
                
                if not response.text:
                    raise ValueError("Empty response from Gemini")
                
                return response.text
                
            except Exception as e:
                error_msg = str(e)
                
                if "429" in error_msg or "quota" in error_msg.lower() or "rate" in error_msg.lower():
                    retry_count += 1
                    if retry_count <= max_retries:
                        delay = min(base_delay * (2 ** (retry_count - 1)), 30)
                        logger.warning(f"Rate limit hit. Retry {retry_count}/{max_retries} in {delay}s")
                        time.sleep(delay)
                        continue
                    else:
                        logger.error(f"Max retries exceeded: {error_msg}")
                        raise
                else:
                    logger.error(f"Gemini API error: {error_msg}")
                    raise
        
        raise Exception("Unexpected error in generate method")
    
    def generate_json(self, prompt: str, temperature: float = 0.3, max_retries: int = 5) -> Dict[str, Any]:
        """Generate and parse JSON from the LLM."""
        retry_count = 0
        base_delay = 5
        
        while retry_count <= max_retries:
            try:
                response_text = self.generate(prompt, temperature)
                
                # Extract JSON from response
                json_str = self._extract_json(response_text)
                
                if not json_str:
                    raise ValueError("No JSON found in response")
                
                return self._parse_json_robust(json_str)
                
            except Exception as e:
                error_msg = str(e)
                
                if "429" in error_msg or "quota" in error_msg.lower() or "rate" in error_msg.lower():
                    retry_count += 1
                    if retry_count <= max_retries:
                        delay = min(base_delay * (2 ** (retry_count - 1)), 30)
                        logger.warning(f"Rate limit hit. Retry {retry_count}/{max_retries} in {delay}s")
                        time.sleep(delay)
                        continue
                    else:
                        logger.error(f"Max retries exceeded: {error_msg}")
                        raise
                else:
                    logger.error(f"Error generating JSON: {error_msg}")
                    raise
        
        raise Exception("Unexpected error in generate_json method")
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from text with multiple strategies."""
        # Strategy 1: Find JSON object
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            return json_match.group()
        
        # Strategy 2: Find JSON array
        json_match = re.search(r'\[[\s\S]*\]', text)
        if json_match:
            return json_match.group()
        
        # Strategy 3: Look for code block with JSON
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
        if json_match:
            return json_match.group(1).strip()
        
        return None
    
    def _parse_json_robust(self, json_str: str) -> Dict[str, Any]:
        """Parse JSON with multiple strategies - ENHANCED VERSION."""
        import json
        import re
        
        # Strategy 1: Direct parse
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.debug(f"Direct parse failed: {e}")
        
        # Strategy 2: Remove trailing commas and fix common issues
        try:
            cleaned = json_str
            # Remove trailing commas in objects
            cleaned = re.sub(r',\s*}', '}', cleaned)
            # Remove trailing commas in arrays
            cleaned = re.sub(r',\s*]', ']', cleaned)
            # Remove comments
            cleaned = re.sub(r'//.*?$', '', cleaned, flags=re.MULTILINE)
            cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)
            return json.loads(cleaned)
        except:
            pass
        
        # Strategy 3: Extract sections manually with improved parsing
        try:
            # Find all section objects
            section_pattern = r'"title"\s*:\s*"([^"]*)"\s*,\s*"content"\s*:\s*"([^"]*)"'
            matches = re.findall(section_pattern, json_str)
            
            if matches:
                sections = []
                for title, content in matches:
                    # Clean up content
                    content = content.replace('\\n', '\n').replace('\\"', '"')
                    sections.append({"title": title, "content": content})
                
                if sections:
                    logger.info(f"✅ Manually extracted {len(sections)} sections")
                    return {"sections": sections}
        except:
            pass
        
        # Strategy 4: Try to fix incomplete JSON
        try:
            # If we have multiple section objects, try to parse them individually
            if 'sections' in json_str:
                # Find all section objects
                section_objects = re.findall(r'\{[^{}]*\}', json_str)
                sections = []
                for obj in section_objects:
                    try:
                        # Try to extract title and content
                        title_match = re.search(r'"title"\s*:\s*"([^"]*)"', obj)
                        content_match = re.search(r'"content"\s*:\s*"([^"]*)"', obj)
                        if title_match and content_match:
                            sections.append({
                                "title": title_match.group(1),
                                "content": content_match.group(1)
                            })
                    except:
                        continue
                
                if sections:
                    logger.info(f"✅ Recovered {len(sections)} sections from partial JSON")
                    return {"sections": sections}
        except:
            pass
        
        # Strategy 5: Check if it's already a valid object
        try:
            # Try to parse as Python literal
            import ast
            parsed = ast.literal_eval(json_str)
            if isinstance(parsed, dict) and "sections" in parsed:
                return parsed
        except:
            pass
        
        # Strategy 6: Last resort - try to extract ANY content
        try:
            # Look for any meaningful text
            text_content = re.sub(r'[{}\[\]]', '', json_str)
            if len(text_content) > 100:
                logger.warning("Using extracted text as fallback content")
                return {
                    "sections": [
                        {"title": "Document Content", "content": text_content[:5000]}
                    ]
                }
        except:
            pass
        
        # Final fallback - create a meaningful error message
        logger.error("All parsing strategies failed, returning fallback")
        return {
            "sections": [
                {"title": "Document Content", "content": "The document content could not be parsed. Please try regenerating."}
            ]
        }