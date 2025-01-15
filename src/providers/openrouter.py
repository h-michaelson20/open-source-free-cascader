from typing import List, Dict, Optional, Union
import asyncio
import os
import openai
import requests
import json

class OpenrouterProvider:
    def __init__(self,
                 openrouter_key):
        self.key = openrouter_key

    async def call_openrouter(self,
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

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer " + self.key,
                #"HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
                #"X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
            },
            data=json.dumps({
                "model": model,
                "messages": messages
                
            })
        )

        data = response.json()
        return data['choices'][0]['message']['content']