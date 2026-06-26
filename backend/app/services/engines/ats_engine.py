SKILLS = [
    "python",
    "java",
    "sql",
    "fastapi",
    "postgresql",
    "docker",
    "git",
    "github",
    "machine learning",
    "tensorflow",
    "pandas",
    "numpy"
]


def analyze_resume(text: str):
    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    score = min(len(found_skills) * 8, 100)

    missing_skills = []

    for skill in SKILLS:
        if skill not in found_skills:
            missing_skills.append(skill)

    return {
        "ats_score": score,
        "skills_found": found_skills,
        "missing_skills": missing_skills
    }