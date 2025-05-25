import re
from pdfminer.high_level import extract_text
import requests

# Predefined skills
predefined_skills = [
    "Python", "JavaScript", "Java", "C#", "C++", "HTML", "CSS", "React.js",
    "Node.js", "Angular", "SQL", "Docker", "Kubernetes", "Git", "AWS",
    "Azure", "Machine Learning", "TensorFlow", "Scikit-learn", "PyTorch",
    "Data Science", "Terraform", "Ansible", "Linux", "Prometheus", "Grafana",
    "CloudFormation", "Nagios", "Jenkins", "Shell Script", "Bash", "AgroCD"
]

def extract_text_from_pdf(pdf_path):
    """
    Extracts raw text from the PDF using pdfminer.
    """
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def clean_text(text):
    """
    Cleans the extracted text by removing unnecessary characters and normalizing spacing.
    """
    text = re.sub(r'\s+', ' ', text)  # Normalize multiple spaces
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII characters
    text = re.sub(r'\s*-\s*', ' ', text)  # Fix broken terms like "Shell Script - Bash"
    text = re.sub(r'\bJava\s*Script\b', 'JavaScript', text)  # Fix "Java Script"
    text = re.sub(r'\bTensor\s*Flow\b', 'TensorFlow', text)  # Fix "Tensor Flow"
    return text.strip()

def extract_matching_skills(text):
    """
    Matches predefined skills within the extracted text.
    """
    matched_skills = []
    text = re.sub(r'\s*[-,;|]\s*', ' ', text)  # Normalize delimiters
    for skill in predefined_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            matched_skills.append(skill)
    return matched_skills

def generate_questions(skills, difficulty="Medium", max_questions=5):
    """
    Sends extracted skills to the Gemini API to generate technical questions.
    """
    api_key = "AIzaSyC1SdomX-1zbJkRMKPI7nf-x3cA0Bl7Bwo"   # Replace with your real API key
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

    # Construct the difficulty-based prompt
    prompt = f"Generate up to {max_questions} technical interview questions for a {difficulty} role based on the following skills: {', '.join(skills)}."
    prompt += " The questions should be simple and clear, without any unnecessary labels, formatting, or information in parentheses. Return only the question text without references to the skills and also dont provide the question numbers"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(api_url, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()

        questions = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()

        if questions:
            # Remove unwanted text (like numbers, and extra descriptive text)

            questions_list = questions.split("\n\n")[:max_questions]
            cleaned_questions = []

            for question in questions_list:
                # Clean up questions to only return the core question without extra labels
                cleaned_question = re.sub(r"^\d+\.\s*\*\*[^*]+\*\*\s*:", "", question).strip()  # Remove numbering and labels

                cleaned_questions.append(cleaned_question)

            return cleaned_questions
        else:
            print("No questions found in the response.")
            return []

    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []

def process_resume(pdf_path, difficulty="Medium"):
    """
    Main function to process a resume, extract skills, and generate questions.
    """
    extracted_text = extract_text_from_pdf(pdf_path)
    if not extracted_text:
        raise Exception("No text extracted from the resume.")

    cleaned_text = clean_text(extracted_text)
    matched_skills = extract_matching_skills(cleaned_text)

    if not matched_skills:
        raise Exception("No skills found in the resume.")

    questions = generate_questions(matched_skills, difficulty)
    if not questions:
        raise Exception("No questions analyzed")

    return questions
