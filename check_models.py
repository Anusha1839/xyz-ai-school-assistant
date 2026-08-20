from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

# First try .env
api_key = os.getenv("GEMINI_API_KEY")

# If .env doesn't contain it, try Streamlit secrets
if not api_key:
    try:
        import streamlit as st
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        api_key = None

if not api_key:
    print("❌ GEMINI_API_KEY not found")
    exit()

print("✅ API key found")

client = genai.Client(api_key=api_key)

print("\nModels available for generateContent:\n")

try:
    for model in client.models.list():

        supported = getattr(
            model,
            "supported_actions",
            []
        ) or []

        if "generateContent" in supported:
            print(model.name)

except Exception as e:

    print("\n❌ Error while listing models:")
    print(e)