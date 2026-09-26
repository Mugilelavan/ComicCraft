from google import genai
from app.config import settings


print("Checking Gemini API...")
print("API key present:", bool(settings.gemini_api_key))

if not settings.gemini_api_key:
    raise SystemExit("ERROR: GEMINI_API_KEY is missing in .env")


client = genai.Client(
    api_key=settings.gemini_api_key
)

print("\nAvailable models:\n")

models = list(client.models.list())

for model in models:
    name = getattr(model, "name", "")
    if "gemini" in name.lower():
        print(name)


print("\nTesting Gemini 3.5 Flash-Lite...\n")

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Reply with exactly: COMICCRAFT TEST OK",
)

print("Response:")
print(response.text)