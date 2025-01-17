from typing import List, Dict, Optional, Union
import asyncio
import os
from groq import Groq

class GroqProvider:
    def __init__(self,
                 groq_key):
        self.client = Groq(
            # This is the default and can be omitted
            api_key=groq_key,
        )

    async def call_groq(self,
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

        chat_completion = self.client.chat.completions.create(
            messages=messages,#[
                # {
                #     "role": "system",
                #     "content": "you are a helpful assistant."
                # },
                # {
                #     "role": "user",
                #     "content": "Explain the importance of fast language models",
                # }
            # ],
            model=model,
            # ET CETERA FOR THE REST OF THE PARAMETERS
        )

        #print(chat_completion)

        return chat_completion.choices[0].message.content