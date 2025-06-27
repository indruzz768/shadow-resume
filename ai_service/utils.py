# utils.py

# Known skill set
KNOWN_SKILLS = set(skill.title() for skill in {
    "Python", "Django", "Flask", "Machine Learning", "Deep Learning",
    "REST API", "Natural Language Processing", "PostgreSQL", "HTML",
    "CSS", "JavaScript", "React", "Docker", "Git", "Pandas", "NumPy",
    "Data Analysis", "Power BI", "AWS", "Linux", "Excel"
})


def extract_skills(text):
    # ✅ Lazy load spaCy
    import spacy
    nlp = spacy.load("en_core_web_sm")

    doc = nlp(text)
    found_skills = set()

    print("\n--- PHRASE MATCHING ---")
    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip().title()
        for skill in KNOWN_SKILLS:
            if skill in phrase:
                print("✅ Found skill (chunk):", skill)
                found_skills.add(skill)

    print("\n--- TOKEN MATCHING ---")
    for token in doc:
        word = token.text.strip().title()
        if word in KNOWN_SKILLS:
            print("✅ Found skill (token):", word)
            found_skills.add(word)

    return list(found_skills)


def extract_text_from_pdf(file_path):
    # ✅ Lazy load PyMuPDF
    import fitz  # PyMuPDF

    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text
