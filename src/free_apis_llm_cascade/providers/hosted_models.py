from typing import List, Dict, Optional, Union
import httpx

class HostedModelProvider:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initializes the provider for any hosted model.

        Args:
            base_url (str): The base URL of the server hosting the model.
            api_key (Optional[str]): Optional API key for authentication.
        """
        self.base_url = base_url
        self.api_key = api_key

    async def call_model(self,
                         endpoint: str,
                         payload: Dict,
                         headers: Optional[Dict[str, str]] = None) -> Dict:
        """
        Sends a request to the model server and retrieves the response.

        Args:
            endpoint (str): The specific API endpoint to call.
            payload (Dict): The payload to send in the request.
            headers (Optional[Dict[str, str]]): Additional headers for the request.

        Returns:
            Dict: The response from the server.
        """
        if not headers:
            headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/{endpoint}", json=payload, headers=headers)
            response.raise_for_status()
            return response.json()

    async def call_chat_model(self,
                              messages: List[Dict[str, str]],
                              model: Optional[str] = None,
                              max_tokens: Optional[int] = None,
                              temperature: Optional[float] = 1.0,
                              top_p: Optional[float] = 1.0,
                              n: Optional[int] = 1,
                              stop: Optional[Union[str, List[str]]] = None,
                              **kwargs) -> Dict:
        """
        A more specific method for interacting with chat-based models.

        Args:
            messages (List[Dict[str, str]]): Chat messages in the format expected by the server.
            model (Optional[str]): The model name or identifier.
            max_tokens (Optional[int]): Maximum number of tokens to generate.
            temperature (Optional[float]): Sampling temperature.
            top_p (Optional[float]): Nucleus sampling parameter.
            n (Optional[int]): Number of completions to generate.
            stop (Optional[Union[str, List[str]]]): Optional stopping sequences.
            **kwargs: Additional parameters for the API call.

        Returns:
            Dict: The response from the server.
        """
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "n": n,
            "stop": stop,
            **kwargs
        }
        return await self.call_model(endpoint="generate", payload=payload)
