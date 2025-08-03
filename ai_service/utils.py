import re
import spacy
from PyPDF2 import PdfReader

nlp = spacy.load("en_core_web_sm")

# Simple skill list for demonstration
SKILL_KEYWORDS = [
    "python", "django", "rest", "html", "css", "javascript",
    "sql", "react", "flask", "git", "api", "docker"
]

def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_skills(text):
    doc = nlp(text.lower())
    found_skills = set()
    for token in doc:
        if token.text in SKILL_KEYWORDS:
            found_skills.add(token.text)
    return list(found_skills)
