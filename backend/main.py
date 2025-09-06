import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import google.generativeai as genai

# ✅ Load environment variables
load_dotenv()

# ✅ Configure Gemini API key safely (fallback only for testing, not recommended in prod)
API_KEY = os.getenv("GEMINI_API_KEY", "your-fallback-api-key-here")
genai.configure(api_key=API_KEY)

# ✅ Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ Initialize FastAPI
app = FastAPI(title="AgroBot", version="1.0")

# ✅ Enable CORS (allow frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request body schema
class UserInput(BaseModel):
    description: str

# ✅ Health check / Root endpoint
@app.get("/")
def read_root():
    return {"message": "🌱 AgroBot connected with Gemini AI!"}

# ✅ Chat endpoint
@app.post("/chat")
def chat_ai(user_input: UserInput):
    try:
        prompt = (
            f"A farmer reports: '{user_input.description}'. "
            f"As an agriculture expert, identify the plant disease "
            f"and provide preventive measures and remedies in 2–3 sentences."
        )
        response = model.generate_content(prompt)
        return {"reply": response.text}
    except Exception as e:
        return {"reply": f"⚠️ Error: {str(e)}"}
