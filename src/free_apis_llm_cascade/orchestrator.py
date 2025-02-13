from typing import List, Dict, Optional, Union
import asyncio
import os
from dotenv import load_dotenv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .providers.groq import GroqProvider
from .providers.googleai import GoogleaiProvider
from .providers.sambanova import SambanovaProvider
from .providers.openrouter import OpenrouterProvider

class LLMOrchestrator:
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
        print(49*"*")
        print("* LLMOrchestrator instance successfully initialized. *")
        print(49*"*")
    
    async def get_single_model_result(self, vendor, model, messages):
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

    async def ochestrator_public(self, vendors, models, prompt):
        raise NotImplementedError("please implement")

    async def orchestrator_internal(self, vendor, model, model_choices, user_prompt):
        orchestrator_prompt = f"""Given the user’s prompt below, assign a complexity rating between 1 and 5 based on how difficult you think the question is to answer:

                                User Prompt: {user_prompt}

                                Rating Scale:
                                - 1: Very simple, factual question with a clear, straightforward answer.
                                - 2: Basic question that requires general knowledge or reasoning.
                                - 3: Question that requires explanation or intermediate-level understanding.
                                - 4: Complex question involving technical or specialized knowledge.
                                - 5: Highly complex, requiring in-depth analysis or a nuanced answer.

                                Examples:

                                1. User Prompt: "What is 2 + 2?"  
                                Rating: 1

                                2. User Prompt: "What is the capital of Japan?"  
                                Rating: 2

                                3. User Prompt: "How does photosynthesis work?"  
                                Rating: 3

                                4. User Prompt: "Can you explain quantum entanglement?"  
                                Rating: 4

                                5. User Prompt: "What are the social, economic, and political effects of the Industrial Revolution?"  
                                Rating: 5

                                Just provide the rating (1-5) — nothing else."""

        #print(orchestrator_prompt)
        
        orchestrator_result = await self.get_single_model_result(vendor, model, [{ "role": "user", "content": orchestrator_prompt }])
        #print(orchestrator_result)
        return orchestrator_result
    
    #async def cascade_three_or_more_llm_basic(self, models, input, cos_sim_threshold=0.75):
    #    for model in models:
            
    #    self.cascade_three_or_more_llm_basic_internal(vendors, models, input, cos_sim_threshold)
            
    
