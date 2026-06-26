import re


def extract_education(text: str):

    education = []

    lines = text.split("\n")

    keywords = [
        "b.tech",
        "btech",
        "b.e",
        "be",
        "m.tech",
        "mtech",
        "bachelor",
        "master",
        "computer science",
        "engineering",
        "college",
        "university"
    ]

    for line in lines:

        clean = line.strip()

        if len(clean) < 5:
            continue

        lower = clean.lower()

        for keyword in keywords:
            if keyword in lower:
                education.append(clean)
                break

    return list(dict.fromkeys(education))