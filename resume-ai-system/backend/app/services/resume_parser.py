import pdfplumber
import docx
import re


def extract_text(file_path):
    text = ""

    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"

    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"

    return text


def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else "Not Found"


def extract_phone(text):
    match = re.search(r'\+?\d[\d -]{8,12}\d', text)
    return match.group(0) if match else "Not Found"


def extract_name(text):
    lines = text.strip().split("\n")
    return lines[0] if lines else "Not Found"