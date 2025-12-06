import pytesseract
from pypdf import PdfReader
from pdf2image import convert_from_bytes
from io import BytesIO


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Attempts normal text extraction first.
    If that fails (scanned PDF), use OCR.
    Returns full extracted text.
    """
    # 1️⃣ Try normal text extraction
    try:
        pdf = PdfReader(BytesIO(pdf_bytes))

        text = ""
        for page in pdf.pages:
        
            extracted = page.extract_text() or ""
            print(extracted)
            text += extracted

        if text.strip():  # if real text found
            return " ".join(text.split()) 
    except:
        pass

    # 2️⃣ OCR fallback (image-based PDF)
    images = convert_from_bytes(pdf_bytes)
    ocr_text = ""

    for img in images:
        page_text = pytesseract.image_to_string(img)
        ocr_text += page_text + "\n"

    return ocr_text
