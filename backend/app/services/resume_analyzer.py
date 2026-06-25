import re

TECH_SKILLS = [
    "python",
    "java",
    "c++",
    "sql",
    "fastapi",
    "postgresql",
    "docker",
    "git",
    "github",
    "tensorflow",
    "pandas",
    "numpy",
    "machine learning",
    "react",
    "next.js"
]


def extract_skills(text: str):
    text = text.lower()

    found = []

    for skill in TECH_SKILLS:
        if skill in text:
            found.append(skill)

    return found


def extract_links(text: str):
    return re.findall(
        r'https?://\S+',
        text
    )


def extract_projects(text: str):

    projects = []

    lines = text.split("\n")

    keywords = [
        "project",
        "system",
        "application",
        "platform",
        "dashboard"
    ]

    for line in lines:

        line = line.strip()

        if len(line) < 5:
            continue

        for keyword in keywords:
            if keyword.lower() in line.lower():
                projects.append(line)
                break

    return list(set(projects))


def extract_email(text: str):

    emails = re.findall(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )

    return emails[0] if emails else None


def extract_phone(text: str):

    phones = re.findall(
        r'(\+91[- ]?)?[6-9]\d{9}',
        text
    )

    return phones[0] if phones else None


def calculate_completeness(text: str):

    score = 0

    checks = [
        "@",
        "github",
        "linkedin",
        "project",
        "education",
        "skill",
        "experience"
    ]

    for item in checks:
        if item.lower() in text.lower():
            score += 15

    return min(score, 100)