# Free API-based LLM Cascade Library

A Python library for cascading LLM (Large Language Model) API calls, allowing you to leverage multiple providers for enhanced language processing capabilities.

## Features

- Supports multiple LLM providers (e.g., Groq, Google AI, SambaNova, OpenRouter).
- Easy-to-use interface for making API calls.
- Cosine similarity calculations for comparing responses.
- Environment variable management for sensitive API keys.

## Installation

To install the library, you can use pip:

```python
pip install free-apis-llm-cascade
```

### Environment Variables

Before using the library, you need to set up your API keys. Create a `.env` file in the root directory of your project and populate it with your API keys as follows:

.env
```
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
SAMBANOVA_API_KEY=your_sambanova_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Make sure to replace the placeholder values with your actual API keys.

### Usage

Here’s a quick example of how to use the `LLMCascade` class:

```python
from free_apis_llm_cascade.cascade import LLMCascade
import asyncio

async def main():
    # Instantiate the LLMCascade class
    llm_cascade = LLMCascade()
    # Prepare your messages, vendors, and models to test the cascade with as well as the cosine similarity threshold
    messages=[{ "role": "user", "content": "What is the capital of California?" }]
    vendors = ["sambanova", "openrouter", "groq", "groq"] # these are the vendors for the models below
    models = ["Meta-Llama-3.2-1B-Instruct", "meta-llama/llama-3.2-3b-instruct:free", "llama3-8b-8192", "llama-3.3-70b-versatile"] # these are the actual models that will be run
    # call the llm cascade function
    output, num_models_run = await llm_cascade.cascade_three_or_more_llm(vendors, models, messages, 0.7) # cosine threshold = 0.7 here
    print(40*"-")
    print(f"Final result: {output}")
    print(f"Models run up to: {models[num_models_run-1]}")
# Run the main function
if name == "main":
    asyncio.run(main())
```

The three functions that are usable in this library currently are:
```
get_single_model_result(self, vendor, model, messages)
cosine_sim_two_llm_basic(self, vendors, models, input)
cascade_three_or_more_llm(self, vendors, models, input, cos_sim_threshold)
```


## Contributing

Contributions are welcome! If you have suggestions for improvements or find bugs, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE.txt file for details.

## Useful reference

This [GitHub repo](https://github.com/cheahjs/free-llm-api-resources/tree/main) stores information about what free LLM APIs are available. We currently only support Groq, Google AI Studio, SambaNova, and OpenRouter, but may expand to others soon.
