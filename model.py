from google import genai
import os
from dotenv import load_dotenv

#boiler plate code replace it in future
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def call_llm(system_prompt, user_prompt, temperature = 0.7):
    full_prompt = f"SYSTEM: {system_prompt} \n\n USER: {user_prompt}"
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=full_prompt,
        config={
            "temperature": temperature
        }
    )

    return response.text