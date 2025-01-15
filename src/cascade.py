from typing import List, Dict, Optional, Union
import asyncio
import os
from dotenv import load_dotenv
from .providers.groq import GroqProvider
from .providers.googleai import GoogleaiProvider
from .providers.sambanova import SambanovaProvider
from .providers.openrouter import OpenrouterProvider

class LLMCascade:
    def __init__(self, 
                 groq_key: Optional[str] = None,
                 googleai_key: Optional[str] = None,
                 sambanova_key: Optional[str] = None,
                 openrouter_key: Optional[str] = None,
                 load_from_env: bool = True):
        """
        Initialize LLM cascade with API keys. Keys can be provided directly or loaded from environment.
        
        Args:
            groq_key: Groq API key (optional if using environment variable)
            anthropic_key: Anthropic API key (optional if using environment variable)
            cohere_key: Cohere API key (optional if using environment variable)
            load_from_env: Whether to load missing keys from environment variables (default True)
        """
        # Load environment variables if requested
        if load_from_env:
            load_dotenv()
        
        # Store API keys with environment variable fallbacks
        self.api_keys = {
            "groq": groq_key or os.getenv("GROQ_API_KEY"),
            "googleai": googleai_key or os.getenv("GOOGLE_API_KEY"),
            "sambanova": sambanova_key or os.getenv("SAMBANOVA_API_KEY"),
            "openrouter": openrouter_key or os.getenv("OPENROUTER_API_KEY")
        }
        
        # Track which providers are available
        self.available_providers = [
            provider for provider, key in self.api_keys.items() 
            if key is not None
        ]
        
        if not self.available_providers:
            raise ValueError("No API keys provided. Please provide at least one API key.")
            
        # Default order - can be changed later
        self.provider_order = self.available_providers.copy()
        print(self.available_providers)

    async def create(self,
                    vendor: str,
                    model: str,
                    messages: List[Dict[str, str]],
                    max_tokens: Optional[int] = None,
                    temperature: Optional[float] = 1.0,
                    top_p: Optional[float] = 1.0,
                    n: Optional[int] = 1,
                    stream: Optional[bool] = False,
                    stop: Optional[Union[str, List[str]]] = None,
                    presence_penalty: Optional[float] = 0,
                    frequency_penalty: Optional[float] = 0,
                    **kwargs) -> Dict:
        """
        OpenAI-compatible interface for generating completions.
        Falls back through providers while maintaining the same interface.
        """
        print('here')
        last_error = None

        raise Exception(f"Complete failure - contact developers for help.")
    
    async def run_test(self, vendor, model, messages):
        # may have to edit the role/system/user whatever and json strucutre to pass in correctly
        try:
            # Create the Groq provider instance
            result = None
            if vendor == 'groq':
                groq_provider = GroqProvider(self.api_keys['groq'])
                result = await groq_provider.call_groq(model=model, messages=messages)
            elif vendor == 'googleai':
                googleai_provider = GoogleaiProvider(self.api_keys['googleai'])
                result = await googleai_provider.call_googleai(model=model, messages=messages)
            elif vendor == 'sambanova':
                sambanova_provider = SambanovaProvider(self.api_keys['sambanova'])
                result = await sambanova_provider.call_sambanova(model=model, messages=messages)
            elif vendor == 'openrouter':
                openrouter_provider = OpenrouterProvider(self.api_keys['openrouter'])
                result = await openrouter_provider.call_openrouter(model=model, messages=messages)
            
            # Return the result if successful
            return result

        except Exception as e:
            last_error = str(e)
            print(f"Error occurred: {last_error}") 
        #return await self.create(vendor="groq", model=model, messages=messages)
    
