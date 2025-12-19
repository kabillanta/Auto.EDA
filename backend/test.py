
import os
from langchain_google_genai import ChatGoogleGenerativeAI

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

model = ChatGoogleGenerativeAI(model="models/gemini-flash-lite-latest", api_key=api_key)

resp = model.invoke("Who is Donald trump")
print(resp.content) 