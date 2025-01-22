from typing import List, Dict, Optional, Union
import asyncio
import os
import openai

class SambanovaProvider:
    def __init__(self,
                 sambanova_key):
        self.client = openai.OpenAI(
            # This is the default and can be omitted
            api_key=sambanova_key,
            base_url="https://api.sambanova.ai/v1",
        )

    async def call_sambanova(self,
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

        response = self.client.chat.completions.create(
            model=model,
            messages=messages,#[{"role":"system","content":"You are a helpful assistant"},{"role":"user","content":"Hello"}],
            temperature = temperature, #0.1,
            top_p = top_p, #0.1
        )

        return response.choices[0].message.content