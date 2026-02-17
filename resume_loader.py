import os

def load_resume():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    resume_path = os.path.join(base_dir, "knowledge", "resume.txt")

    with open(resume_path, "r", encoding="utf-8") as f:
        return f.read()
