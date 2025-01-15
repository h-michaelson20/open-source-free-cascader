from src.cascade import LLMCascade
import asyncio

async def main():
    # Create an instance of LLMCascade
    llm_cascade = LLMCascade()
    # this should test this first
    # result = await llm_cascade.run_test( vendor="groq",
    #                                      model="llama-3.3-70b-versatile",
    #                                      messages=[{
    #                                             "role": "user",
    #                                             "content": "Explain the importance of fast language models"
    #                                      }])
    # print(result)

    # print(60*"-")
    # print(60*"-")

    # result = await llm_cascade.run_test( vendor="googleai",
    #                                      model="gemini-1.5-flash",
    #                                      messages="Explain the importance of fast language models"
    # )
    
    # print(result)

    # print(60*"-")
    # print(60*"-")

    # result = await llm_cascade.run_test( vendor="sambanova",
    #                                      model="Meta-Llama-3.1-8B-Instruct",
    #                                      messages=[{
    #                                             "role": "user",
    #                                             "content": "Explain the importance of fast language models"
    #                                      }])
    
    # print(result)

    print(60*"-")
    print(60*"-")

    result = await llm_cascade.run_test( vendor="openrouter",
                                         model="meta-llama/llama-3.2-3b-instruct:free",
                                         messages=[{
                                                "role": "user",
                                                "content": "Explain the importance of fast language models"
                                         }])
    
    print(result)

if __name__ == "__main__":
    asyncio.run(main())