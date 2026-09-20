import re


ALIASES = {

    "python programming": "python",
    "python": "python",

    "java programming": "java",
    "java": "java",

    "javascript": "javascript",
    "js": "javascript",

    "typescript": "typescript",
    "ts": "typescript",

    "react.js": "react",
    "reactjs": "react",
    "react": "react",

    "node.js": "node.js",
    "nodejs": "node.js",

    "express.js": "express",
    "expressjs": "express",

    "nextjs": "next.js",
    "next.js": "next.js",

    "html5": "html",
    "html": "html",

    "css3": "css",
    "css": "css",

    "sql": "sql",

    "mysql": "mysql",
    "my sql": "mysql",

    "postgres": "postgresql",
    "postgresql": "postgresql",

    "mongodb": "mongodb",
    "mongo db": "mongodb",

    "git": "git",
    "github": "github",

    "docker": "docker",

    "kubernetes": "kubernetes",

    "terraform": "terraform",

    "jenkins": "jenkins",

    "aws": "aws",
    "amazon web services": "aws",

    "azure": "azure",

    "gcp": "gcp",
    "google cloud": "gcp",

    "flask": "flask",

    "django": "django",

    "fastapi": "fastapi",
    "fast api": "fastapi",

    "machine learning": "machine learning",
    "ml": "machine learning",

    "deep learning": "deep learning",
    "dl": "deep learning",

    "artificial intelligence":
        "artificial intelligence",

    "ai":
        "artificial intelligence",

    "nlp":
        "nlp",

    "natural language processing":
        "nlp",

    "tensorflow":
        "tensorflow",

    "pytorch":
        "pytorch",

    "excel":
        "excel",

    "power bi":
        "power bi",

    "tableau":
        "tableau",

    "figma":
        "figma",

    "ui/ux":
        "ui/ux",

    "rest api":
        "rest api",

    "api":
        "api",

    "json":
        "json",

    "linux":
        "linux",

    "networking":
        "networking"
}


TRANSFERABLE = {

    ("flask", "fastapi"):
        "Both are Python frameworks used for building web APIs.",

    ("django", "fastapi"):
        "Both are Python frameworks used for web and API development.",

    ("javascript", "typescript"):
        "TypeScript extends JavaScript with additional type support.",

    ("mysql", "postgresql"):
        "Both are relational database systems.",

    ("aws", "azure"):
        "Both are major cloud computing platforms.",

    ("aws", "gcp"):
        "Both are major cloud computing platforms.",

    ("azure", "aws"):
        "Both are major cloud computing platforms.",

    ("react", "angular"):
        "Both are frontend technologies used to build web applications.",

    ("tensorflow", "pytorch"):
        "Both are deep learning frameworks.",

    ("html", "react"):
        "HTML knowledge provides a foundation for building React interfaces.",

    ("javascript", "react"):
        "JavaScript is the main programming language used with React."
}


def normalize(skill):

    skill = str(skill).lower().strip()

    skill = re.sub(
        r"[^\w\s.+/#-]",
        "",
        skill
    )

    return ALIASES.get(
        skill,
        skill
    )


def normalize_skills(skills):

    result = []

    for skill in skills:

        normalized = normalize(skill)

        if (
            normalized and
            normalized not in result
        ):
            result.append(normalized)

    return result


def find_evidence(
    resume_text,
    skill
):

    skill_lower = skill.lower()

    sentences = re.split(
        r'(?<=[.!?])\s+',
        resume_text
    )

    aliases = [
        skill_lower
    ]

    for alias, normalized in ALIASES.items():

        if normalized == skill_lower:

            aliases.append(alias)


    for sentence in sentences:

        sentence_lower = sentence.lower()

        for alias in aliases:

            if alias in sentence_lower:

                return sentence.strip()


    return None


def calculate_skill_gap(
    resume_data,
    job_data
):

    resume_skills = normalize_skills(
        resume_data.get(
            "skills",
            []
        )
    )

    required_skills = normalize_skills(
        job_data.get(
            "required_skills",
            []
        )
    )

    preferred_skills = normalize_skills(
        job_data.get(
            "preferred_skills",
            []
        )
    )


    matched = []

    missing = []


    for skill in required_skills:

        if skill in resume_skills:

            matched.append(skill)

        else:

            missing.append(skill)


    transferable = []


    for missing_skill in missing:

        for resume_skill in resume_skills:

            pair = (
                resume_skill,
                missing_skill
            )

            if pair in TRANSFERABLE:

                transferable.append({

                    "from":
                        resume_skill,

                    "to":
                        missing_skill,

                    "reason":
                        TRANSFERABLE[pair]
                })


    preferred_matched = []


    for skill in preferred_skills:

        if skill in resume_skills:

            preferred_matched.append(
                skill
            )


    if required_skills:

        score = round(
            (
                len(matched)
                /
                len(required_skills)
            )
            * 100
        )

    else:

        score = 0


    return {

        "score": score,

        "matched": matched,

        "missing": missing,

        "transferable":
            transferable,

        "preferred_matched":
            preferred_matched
    }