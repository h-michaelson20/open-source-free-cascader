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

    def cosine_similarity_strings(self, str1: str, str2: str) -> float:
        """
        Calculate the cosine similarity between two strings.

        Args:
            str1 (str): The first string.
            str2 (str): The second string.

        Returns:
            float: The cosine similarity between the two strings (0 to 1).
        """
        # Create a CountVectorizer to convert the strings to vectors
        vectorizer = CountVectorizer().fit_transform([str1, str2])
        
        # Convert the vectorized strings to an array
        vectors = vectorizer.toarray()
        
        # Calculate the cosine similarity
        cosine_sim = cosine_similarity(vectors)
        
        # Return the cosine similarity between the two strings
        return cosine_sim[0][1]

    async def cosine_sim_two_llm_basic(self, vendors, models, input):
        if len(vendors) != len(models) or len(vendors) != 2:
            raise Exception("Vendors and models are different sizes and/or not equal to 2")
        
        results = []
        for i in range(0, len(vendors)):
            # get the result from each element in the models we are cascading together
            result = None
            if vendors[i] == 'groq':
                groq_provider = GroqProvider(self.api_keys['groq'])
                result = await groq_provider.call_groq(model=models[i], messages=input)
            elif vendors[i] == 'googleai':
                googleai_provider = GoogleaiProvider(self.api_keys['googleai'])
                result = await googleai_provider.call_googleai(model=models[i], messages=input)
            elif vendors[i] == 'sambanova':
                sambanova_provider = SambanovaProvider(self.api_keys['sambanova'])
                result = await sambanova_provider.call_sambanova(model=models[i], messages=input)
            elif vendors[i] == 'openrouter':
                openrouter_provider = OpenrouterProvider(self.api_keys['openrouter'])
                result = await openrouter_provider.call_openrouter(model=models[i], messages=input)

            results.append(result)

        cos_sim = self.cosine_similarity_strings(results[0], results[1])
        print(f"Result from {models[0]}: {results[0]}")
        print(100*"-")
        print(f"Result from {models[1]}: {results[1]}")
        print(100*"-")
        print(f"Cosine similarity between {models[0]} and {models[1]}: {cos_sim}")
        return cos_sim
    

    async def cascade_three_or_more_llm(self, vendors, models, input, cos_sim_threshold):
        if len(vendors) != len(models) or len(vendors) <= 2:
            raise Exception("Vendors and models are different sizes and/or less than 3")
        
        results = []
        cascading_index = 0
        for i in range(0, len(vendors)):
            # get the result from each element in the models we are cascading together
            result = None
            if vendors[i] == 'groq':
                groq_provider = GroqProvider(self.api_keys['groq'])
                result = await groq_provider.call_groq(model=models[i], messages=input)
            elif vendors[i] == 'googleai':
                googleai_provider = GoogleaiProvider(self.api_keys['googleai'])
                result = await googleai_provider.call_googleai(model=models[i], messages=input)
            elif vendors[i] == 'sambanova':
                sambanova_provider = SambanovaProvider(self.api_keys['sambanova'])
                result = await sambanova_provider.call_sambanova(model=models[i], messages=input)
            elif vendors[i] == 'openrouter':
                openrouter_provider = OpenrouterProvider(self.api_keys['openrouter'])
                result = await openrouter_provider.call_openrouter(model=models[i], messages=input)

            print(result)
            results.append(result)

            if i >= 1:
                cos_sim = self.cosine_similarity_strings(results[i-1], results[i])
                print(f"Cosine similiarity between answer {i-1} and answer {i}: {cos_sim}")
                if cos_sim > cos_sim_threshold:
                    return result, i+1
            
        return results[len(results)-1], len(results)
    
    #async def cascade_three_or_more_llm_basic(self, models, input, cos_sim_threshold=0.75):
    #    for model in models:
            
    #    self.cascade_three_or_more_llm_basic_internal(vendors, models, input, cos_sim_threshold)
            
    
