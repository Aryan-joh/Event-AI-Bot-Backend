# 🎉 Event Estimator & Negotiation Bot (LovableBolt)

A smart and interactive AI-powered assistant that helps users **estimate** and **negotiate** costs for events — either manually or by uploading a **PDF**, **Excel**, or **Image**.

---

## 🛠️ Tech Stack

- 🧠 Google Gemini API for AI cost breakdown & negotiation
- ⚡ FastAPI (Python) for backend API
- ⚛️ React + TailwindCSS for modern frontend UI
- 📄 OCR, Excel, PDF parsing with Pytesseract, OpenPyXL & PyMuPDF

---

## ✨ Features

- Manual input-based cost estimation & negotiation
- Upload files (PDF, Excel, or images) to auto-extract event data
- Toggle between estimation-only, negotiation-only, or both
- Auto-scroll to result after processing

---

## ⚙️ Backend Setup (Python - FastAPI)

> 📝 Make sure you have **Python 3.10+** and `pip` installed. Use virtualenv for isolated environments.

### 🔧 Backend Installation Steps

```bash
# Step 1: Clone the repository
git clone https://github.com/YOUR_USERNAME/event-bot.git
cd event-bot/backend

# Step 2: Set up and activate virtual environment
python -m venv venv
venv\Scripts\activate      # On Windows
# OR
source venv/bin/activate   # On macOS/Linux

# Step 3: Install dependencies
pip install -r requirements.txt

# If requirements.txt is missing, run:
pip install fastapi uvicorn python-dotenv pydantic google-generativeai python-multipart pytesseract openpyxl PyMuPDF pillow

# Step 4: Start the backend server
uvicorn main:app --reload
