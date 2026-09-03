from fastapi import FastAPI
from pydantic import BaseModel, Field
from .invoice import extract_invoice, validate_invoice

class ExtractRequest(BaseModel):
    text: str = Field(min_length=10)

app = FastAPI(title="OCRDoc-Intelligence", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/extract/invoice")
def extract(payload: ExtractRequest):
    invoice = extract_invoice(payload.text)
    issues = validate_invoice(invoice)
    return {"invoice": invoice, "validation_issues": issues, "accepted": not issues}
