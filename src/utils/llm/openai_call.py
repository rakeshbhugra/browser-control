from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def get_openai_completion(system_prompt, user_prompt, model, temperature=0, stream=False, tools=[]):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    response = client.responses.create(
        model=model,
        input=messages,
        tools=tools,
        temperature=temperature,
        stream=stream
    )
    return response.output
