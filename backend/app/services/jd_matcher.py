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


def match_resume_to_jd(
    resume_text: str,
    jd_text: str
):
    resume_text = resume_text.lower()
    jd_text = jd_text.lower()

    jd_skills = []

    for skill in SKILLS:
        if skill in jd_text:
            jd_skills.append(skill)

    matched = []

    for skill in jd_skills:
        if skill in resume_text:
            matched.append(skill)

    missing = []

    for skill in jd_skills:
        if skill not in matched:
            missing.append(skill)

    score = 0

    if len(jd_skills) > 0:
        score = int(
            len(matched) / len(jd_skills) * 100
        )

    return {
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing
    }
    