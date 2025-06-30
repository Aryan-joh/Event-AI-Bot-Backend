import fitz  # PyMuPDF
import openpyxl
import io
from PIL import Image
import pytesseract

def calculate_total_cost(event_type, guest_count, services):
    service_prices = {
        "catering": 500,
        "venue": 20000,
        "decoration": 10000,
        "photography": 15000,
        "entertainment": 8000
    }

    base_cost = guest_count * 300
    service_cost = sum(service_prices.get(service.lower(), 0) for service in services)

    return base_cost + service_cost

def extract_text_from_pdf(content):
    with fitz.open(stream=content, filetype="pdf") as doc:
        return "\n".join([page.get_text() for page in doc])

def extract_text_from_excel(content):
    wb = openpyxl.load_workbook(io.BytesIO(content))
    sheet = wb.active
    text = ""
    for row in sheet.iter_rows(values_only=True):
        text += " ".join([str(cell) for cell in row if cell is not None]) + "\n"
    return text

def extract_text_from_image(content):
    img = Image.open(io.BytesIO(content))
    return pytesseract.image_to_string(img)

def parse_event_details_from_text(text):
    import re
    event_type = re.search(r"event[:\- ]+(\w+)", text, re.I)
    guest_count = re.search(r"guest[s]?:[\s\-]*(\d+)", text, re.I)
    budget = re.search(r"budget[:\- ₹]*([\d]+)", text, re.I)
    services = re.findall(r"(catering|venue|decoration|photography|entertainment)", text, re.I)

    return {
        "event_type": event_type.group(1).lower() if event_type else "birthday",
        "guest_count": int(guest_count.group(1)) if guest_count else 50,
        "services": list(set([s.lower() for s in services])),
        "budget": int(budget.group(1)) if budget else 50000
    }
