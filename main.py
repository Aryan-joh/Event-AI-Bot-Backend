from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware  # ✅ Added for CORS
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai
from utils import (
    calculate_total_cost,
    extract_text_from_pdf,
    extract_text_from_excel,
    extract_text_from_image,
    parse_event_details_from_text
)
from prompt_builder import build_prompt, build_estimation_prompt

# Load environment variables
load_dotenv()

# Configure Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize FastAPI app
app = FastAPI()

# ✅ Enable CORS for frontend on localhost:5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 👈 your Vite React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for manual input
class EventRequest(BaseModel):
    event_type: str
    guest_count: int
    services: list[str]
    budget: int

# Route: Manual Estimation
@app.post("/estimate")
def estimate_with_ai(data: EventRequest):
    total_cost = calculate_total_cost(data.event_type, data.guest_count, data.services)
    prompt = build_estimation_prompt(data.event_type, data.guest_count, data.services, total_cost)

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return {
        "total_cost": total_cost,
        "ai_estimate_explanation": response.text
    }

# Route: Manual Negotiation
@app.post("/negotiate")
def negotiate(data: EventRequest):
    total_cost = calculate_total_cost(data.event_type, data.guest_count, data.services)
    prompt = build_prompt(data.event_type, data.guest_count, data.services, data.budget, total_cost)

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return {
        "total_cost": total_cost,
        "bot_reply": response.text
    }

# Route: File Upload for Estimation
@app.post("/upload-estimate")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename.lower()
    contents = await file.read()

    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(contents)
    elif filename.endswith(".xlsx"):
        text = extract_text_from_excel(contents)
    elif filename.endswith((".jpg", ".jpeg", ".png")):
        text = extract_text_from_image(contents)
    else:
        return {"error": "Unsupported file format"}

    event_data = parse_event_details_from_text(text)

    total_cost = calculate_total_cost(
        event_data["event_type"],
        event_data["guest_count"],
        event_data["services"]
    )

    prompt = build_estimation_prompt(
        event_data["event_type"],
        event_data["guest_count"],
        event_data["services"],
        total_cost
    )

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return {
        "event_data": event_data,
        "total_cost": total_cost,
        "ai_estimate_explanation": response.text,
        "raw_text": text
    }

# ✅ New Route: File Upload for Negotiation
@app.post("/upload-negotiate")
async def upload_file_and_negotiate(file: UploadFile = File(...)):
    filename = file.filename.lower()
    contents = await file.read()

    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(contents)
    elif filename.endswith(".xlsx"):
        text = extract_text_from_excel(contents)
    elif filename.endswith((".jpg", ".jpeg", ".png")):
        text = extract_text_from_image(contents)
    else:
        return {"error": "Unsupported file format"}

    event_data = parse_event_details_from_text(text)

    total_cost = calculate_total_cost(
        event_data["event_type"],
        event_data["guest_count"],
        event_data["services"]
    )

    prompt = build_prompt(
        event_data["event_type"],
        event_data["guest_count"],
        event_data["services"],
        event_data["budget"],
        total_cost
    )

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return {
        "event_data": event_data,
        "total_cost": total_cost,
        "bot_reply": response.text,
        "raw_text": text
    }

# Root Route
@app.get("/")
def read_root():
    return {"message": "Welcome to the Event Estimation and Negotiation Bot API"}
