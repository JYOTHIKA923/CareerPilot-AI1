# ============================================================
# CareerPilot AI - AI Agent
# File: ai_agent.py
# ============================================================

import os
import re
import json

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


# ============================================================
# SKILL ALIASES
# ============================================================

SKILL_ALIASES = {

    # Programming Languages
    "python": ["python", "python3"],
    "java": ["java"],
    "c": ["c programming", "c language"],
    "c++": ["c++", "cpp"],
    "c#": ["c#", "c sharp"],
    "javascript": ["javascript", "js", "ecmascript"],
    "typescript": ["typescript", "ts"],
    "go": ["golang", "go language"],
    "rust": ["rust programming"],
    "kotlin": ["kotlin"],
    "swift": ["swift"],

    # Web
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "react": ["react", "reactjs", "react.js"],
    "angular": ["angular", "angularjs"],
    "vue": ["vue", "vuejs", "vue.js"],
    "next.js": ["next.js", "nextjs"],
    "node.js": ["node.js", "nodejs", "node"],
    "express": ["express", "express.js", "expressjs"],
    "flask": ["flask"],
    "django": ["django"],
    "fastapi": ["fastapi", "fast api"],
    "spring": ["spring", "spring boot"],
    "bootstrap": ["bootstrap"],
    "tailwind css": ["tailwind", "tailwind css"],

    # Databases
    "sql": ["sql"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres", "postgres sql"],
    "mongodb": ["mongodb", "mongo db"],
    "oracle": ["oracle database", "oracle"],
    "sqlite": ["sqlite"],
    "redis": ["redis"],
    "firebase": ["firebase"],

    # Data / AI / ML
    "machine learning": [
        "machine learning",
        "machine-learning",
        "ml"
    ],
    "deep learning": [
        "deep learning",
        "deep-learning"
    ],
    "artificial intelligence": [
        "artificial intelligence",
        "ai"
    ],
    "nlp": [
        "natural language processing",
        "nlp"
    ],
    "computer vision": [
        "computer vision",
        "cv"
    ],
    "data science": [
        "data science",
        "data scientist"
    ],
    "data analysis": [
        "data analysis",
        "data analytics",
        "data analyst"
    ],
    "statistics": [
        "statistics",
        "statistical analysis"
    ],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "scikit-learn": [
        "scikit-learn",
        "sklearn"
    ],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "keras": ["keras"],
    "matplotlib": ["matplotlib"],
    "power bi": [
        "power bi",
        "powerbi"
    ],
    "tableau": ["tableau"],
    "excel": [
        "excel",
        "microsoft excel"
    ],

    # Cloud
    "aws": [
        "aws",
        "amazon web services"
    ],
    "azure": [
        "azure",
        "microsoft azure"
    ],
    "gcp": [
        "gcp",
        "google cloud",
        "google cloud platform"
    ],
    "cloud computing": [
        "cloud computing",
        "cloud technology"
    ],

    # DevOps
    "git": ["git"],
    "github": ["github", "git hub"],
    "gitlab": ["gitlab", "git lab"],
    "docker": ["docker"],
    "kubernetes": [
        "kubernetes",
        "k8s"
    ],
    "terraform": ["terraform"],
    "jenkins": ["jenkins"],
    "ci/cd": [
        "ci/cd",
        "cicd",
        "continuous integration",
        "continuous deployment",
        "continuous delivery"
    ],
    "linux": [
        "linux",
        "ubuntu",
        "unix"
    ],

    # Networking
    "networking": [
        "computer networking",
        "networking",
        "network"
    ],
    "tcp/ip": [
        "tcp/ip",
        "tcp ip"
    ],
    "rest api": [
        "rest api",
        "restful api",
        "restful services"
    ],
    "api": [
        "api",
        "apis",
        "application programming interface"
    ],

    # Mobile
    "android": ["android"],
    "ios": ["ios"],
    "flutter": ["flutter"],
    "react native": [
        "react native"
    ],

    # Design
    "figma": ["figma"],
    "ui/ux": [
        "ui/ux",
        "ui ux",
        "user interface",
        "user experience"
    ],
    "wireframing": [
        "wireframing",
        "wireframes"
    ],

    # Other common skills
    "oops": [
        "oops",
        "object oriented programming",
        "object-oriented programming"
    ],
    "data structures": [
        "data structures",
        "data structure"
    ],
    "algorithms": [
        "algorithms",
        "algorithm"
    ],
    "dbms": [
        "dbms",
        "database management system"
    ],
    "operating systems": [
        "operating systems",
        "operating system",
        "os"
    ],
    "microcontrollers": [
        "microcontrollers",
        "microcontroller"
    ],
    "embedded systems": [
        "embedded systems",
        "embedded system"
    ],
    "communication": [
        "communication skills",
        "communication"
    ],
    "leadership": ["leadership"],
    "teamwork": [
        "teamwork",
        "team work"
    ],
    "problem solving": [
        "problem solving",
        "problem-solving"
    ]
}


# ============================================================
# TRANSFERABLE SKILLS
# ============================================================

TRANSFERABLE_SKILLS = {

    "flask": [
        "fastapi",
        "django"
    ],

    "django": [
        "flask",
        "fastapi"
    ],

    "fastapi": [
        "flask",
        "django"
    ],

    "mysql": [
        "postgresql",
        "sqlite"
    ],

    "postgresql": [
        "mysql",
        "sqlite"
    ],

    "javascript": [
        "typescript"
    ],

    "typescript": [
        "javascript"
    ],

    "aws": [
        "azure",
        "gcp"
    ],

    "azure": [
        "aws",
        "gcp"
    ],

    "gcp": [
        "aws",
        "azure"
    ],

    "tensorflow": [
        "pytorch"
    ],

    "pytorch": [
        "tensorflow"
    ],

    "react": [
        "angular",
        "vue"
    ],

    "angular": [
        "react",
        "vue"
    ],

    "vue": [
        "react",
        "angular"
    ],

    "html": [
        "react",
        "angular",
        "vue"
    ],

    "git": [
        "github",
        "gitlab"
    ],

    "github": [
        "gitlab"
    ],

    "power bi": [
        "tableau"
    ],

    "tableau": [
        "power bi"
    ]
}


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):
    """
    Cleans extracted resume/JD text.
    """

    if not text:
        return ""

    text = str(text)

    # Replace unusual spaces
    text = text.replace("\xa0", " ")

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# ============================================================
# NORMALIZE SKILL
# ============================================================

def normalize_skill(skill):
    """
    Converts skill names into a standard format.
    """

    if not skill:
        return ""

    skill = skill.lower().strip()

    for canonical, aliases in SKILL_ALIASES.items():

        if skill == canonical:
            return canonical

        for alias in aliases:
            if skill == alias.lower():
                return canonical

    return skill


# ============================================================
# SKILL MATCHING HELPER
# ============================================================

def contains_skill(text, skill):
    """
    Checks whether a skill exists in text.

    Uses word boundaries to reduce false matches.
    """

    if not text or not skill:
        return False

    text = text.lower()

    aliases = SKILL_ALIASES.get(skill, [skill])

    for alias in aliases:

        alias = alias.lower().strip()

        # Special handling for very short terms
        if len(alias) <= 2:
            pattern = r"(?<![a-z0-9])" + re.escape(alias) + r"(?![a-z0-9])"
        else:
            pattern = r"(?<![a-z0-9])" + re.escape(alias) + r"(?![a-z0-9])"

        if re.search(pattern, text):
            return True

    return False


# ============================================================
# EXTRACT SKILLS
# ============================================================

def extract_skills(text):
    """
    Detects known skills dynamically from resume/JD text.
    """

    text = clean_text(text)

    if not text:
        return []

    found = []

    for canonical_skill in SKILL_ALIASES.keys():

        if contains_skill(text, canonical_skill):
            found.append(canonical_skill)

    return found


# ============================================================
# FIND SECTION
# ============================================================

def extract_section(text, headings):
    """
    Extracts text under a heading until the next heading.

    Example:
        Required Skills:
        Python, SQL, Java

        Preferred Skills:
        AWS, Docker
    """

    if not text:
        return ""

    lines = text.splitlines()

    start_index = None

    for i, line in enumerate(lines):

        line_clean = line.strip().lower()

        for heading in headings:

            if heading in line_clean:
                start_index = i + 1
                break

        if start_index is not None:
            break

    if start_index is None:
        return ""

    result = []

    possible_end_headings = [
        "preferred",
        "preference",
        "nice to have",
        "good to have",
        "bonus",
        "responsibilities",
        "responsibility",
        "requirements",
        "qualification",
        "qualifications",
        "education",
        "experience",
        "about the role",
        "about us",
        "benefits"
    ]

    for line in lines[start_index:]:

        clean_line = line.strip().lower()

        if not clean_line:
            continue

        should_stop = False

        for end_heading in possible_end_headings:

            if clean_line.startswith(end_heading):
                should_stop = True
                break

        if should_stop:
            break

        result.append(line)

    return "\n".join(result).strip()


# ============================================================
# REQUIRED SECTION
# ============================================================

def get_required_section(job_text):
    """
    Finds the required skills section.
    """

    headings = [
        "required skills",
        "required skill",
        "requirements",
        "required",
        "must have",
        "mandatory skills",
        "mandatory",
        "qualifications",
        "qualification",
        "technical requirements"
    ]

    return extract_section(job_text, headings)


# ============================================================
# PREFERRED SECTION
# ============================================================

def get_preferred_section(job_text):
    """
    Finds preferred/nice-to-have skills section.
    """

    headings = [
        "preferred skills",
        "preferred skill",
        "preferred",
        "nice to have",
        "nice-to-have",
        "good to have",
        "bonus skills",
        "bonus",
        "desired skills",
        "desired"
    ]

    return extract_section(job_text, headings)


# ============================================================
# EXTRACT REQUIRED SKILLS
# ============================================================

def extract_required_skills(job_text):
    """
    Gets required skills from the JD.

    If a specific required section exists, it uses it.
    Otherwise it detects skills from the entire JD.
    """

    job_text = clean_text(job_text)

    if not job_text:
        return []

    required_section = get_required_section(job_text)

    preferred_section = get_preferred_section(job_text)

    if required_section:

        skills = extract_skills(required_section)

        if skills:
            return skills

    # Fallback:
    # Detect skills from complete JD
    all_skills = extract_skills(job_text)

    preferred_skills = extract_skills(preferred_section)

    required_skills = [
        skill
        for skill in all_skills
        if skill not in preferred_skills
    ]

    return required_skills


# ============================================================
# EXTRACT PREFERRED SKILLS
# ============================================================

def extract_preferred_skills(job_text):
    """
    Gets preferred skills from JD.
    """

    job_text = clean_text(job_text)

    if not job_text:
        return []

    preferred_section = get_preferred_section(job_text)

    if preferred_section:
        return extract_skills(preferred_section)

    return []


# ============================================================
# RESUME ANALYSIS
# ============================================================

def analyze_resume(resume_text):
    """
    Analyze resume and return detected skills.
    """

    resume_text = clean_text(resume_text)

    skills = extract_skills(resume_text)

    return {
        "skills": skills,
        "text": resume_text
    }


# ============================================================
# JOB ANALYSIS
# ============================================================

def analyze_job(job_description):
    """
    Analyze job description.
    """

    job_description = clean_text(job_description)

    required_skills = extract_required_skills(job_description)

    preferred_skills = extract_preferred_skills(job_description)

    all_skills = extract_skills(job_description)

    return {
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "skills": all_skills,
        "text": job_description
    }


# ============================================================
# EVIDENCE EXTRACTION
# ============================================================

def get_skill_evidence(resume_text, skills):
    """
    Finds a short sentence/line from resume showing evidence
    for each detected skill.
    """

    resume_text = clean_text(resume_text)

    if not resume_text:
        return {}

    lines = resume_text.splitlines()

    evidence = {}

    for skill in skills:

        for line in lines:

            line = line.strip()

            if not line:
                continue

            if contains_skill(line, skill):

                # Keep evidence short
                if len(line) > 220:
                    line = line[:220] + "..."

                evidence[skill] = line
                break

        if skill not in evidence:

            # Fallback search over sentences
            sentences = re.split(
                r"(?<=[.!?])\s+",
                resume_text
            )

            for sentence in sentences:

                if contains_skill(sentence, skill):

                    sentence = sentence.strip()

                    if len(sentence) > 220:
                        sentence = sentence[:220] + "..."

                    evidence[skill] = sentence
                    break

    return evidence


# ============================================================
# LOCAL AI ANALYSIS
# ============================================================

def local_analysis(resume_text, job_description):
    """
    Fully local analysis.

    This is the important fallback when Gemini is unavailable.
    """

    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    resume_skills = extract_skills(resume_text)

    required_skills = extract_required_skills(job_description)

    preferred_skills = extract_preferred_skills(job_description)

    # If no required section is found,
    # use detected JD skills as requirements.
    if not required_skills:

        all_job_skills = extract_skills(job_description)

        required_skills = [
            skill
            for skill in all_job_skills
            if skill not in preferred_skills
        ]

    matched = []

    missing = []

    for skill in required_skills:

        if skill in resume_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    # Preferred skills that resume already has
    preferred_matched = [
        skill
        for skill in preferred_skills
        if skill in resume_skills
    ]

    transferable = []

    for missing_skill in missing:

        for resume_skill in resume_skills:

            related_skills = TRANSFERABLE_SKILLS.get(
                resume_skill,
                []
            )

            if missing_skill in related_skills:

                transferable.append({
                    "from": resume_skill,
                    "to": missing_skill,
                    "reason": (
                        f"{format_skill(resume_skill)} "
                        f"provides a useful foundation for "
                        f"learning {format_skill(missing_skill)}."
                    )
                })

                break

    # Evidence
    evidence = get_skill_evidence(
        resume_text,
        matched
    )

    return {
        "resume_skills": resume_skills,
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "matched": matched,
        "missing": missing,
        "preferred_matched": preferred_matched,
        "transferable": transferable,
        "evidence": evidence
    }


# ============================================================
# GEMINI OPTIONAL ANALYSIS
# ============================================================

def try_gemini(resume_text, job_description):
    """
    Optional Gemini enhancement.

    If Gemini is unavailable, this function returns None.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None

    try:

        from google import genai

        client = genai.Client(
            api_key=api_key
        )

        prompt = f"""
You are a career analysis assistant.

Analyze the following resume and job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return ONLY valid JSON.

Use this exact structure:

{{
    "resume_skills": [],
    "required_skills": [],
    "preferred_skills": [],
    "matched": [],
    "missing": [],
    "transferable": [],
    "evidence": {{}}
}}

Rules:

1. Identify skills from the resume.
2. Identify required skills from the job description.
3. Identify preferred skills.
4. Compare resume skills with required skills.
5. Identify missing required skills.
6. Identify reasonable transferable skills.
7. Evidence must contain short statements from the resume.
8. Do not invent skills that are not supported by the text.
9. Keep skill names concise.
10. Return JSON only.
"""

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        if not response:
            return None

        response_text = response.text.strip()

        # Remove markdown code fences if Gemini returns them
        response_text = re.sub(
            r"^```json\s*",
            "",
            response_text,
            flags=re.IGNORECASE
        )

        response_text = re.sub(
            r"\s*```$",
            "",
            response_text
        )

        data = json.loads(response_text)

        if not isinstance(data, dict):
            return None

        return data

    except Exception as e:

        print(
            "Gemini unavailable. "
            "Using local analysis instead."
        )

        print("Gemini error:", str(e))

        return None


# ============================================================
# FORMAT SKILL
# ============================================================

def format_skill(skill):
    """
    Makes skill names look better in UI.
    """

    if not skill:
        return ""

    special_names = {
        "python": "Python",
        "javascript": "JavaScript",
        "typescript": "TypeScript",
        "html": "HTML",
        "css": "CSS",
        "react": "React",
        "next.js": "Next.js",
        "node.js": "Node.js",
        "c++": "C++",
        "c#": "C#",
        "sql": "SQL",
        "mysql": "MySQL",
        "postgresql": "PostgreSQL",
        "mongodb": "MongoDB",
        "aws": "AWS",
        "azure": "Azure",
        "gcp": "GCP",
        "api": "API",
        "rest api": "REST API",
        "ci/cd": "CI/CD",
        "git": "Git",
        "github": "GitHub",
        "gitlab": "GitLab",
        "power bi": "Power BI",
        "ui/ux": "UI/UX",
        "nlp": "NLP",
        "oops": "OOPs",
        "dbms": "DBMS"
    }

    if skill.lower() in special_names:
        return special_names[skill.lower()]

    return skill.title()


# ============================================================
# NORMALIZE AI RESULT
# ============================================================

def normalize_ai_result(data):
    """
    Cleans Gemini/local result into predictable structure.
    """

    if not isinstance(data, dict):
        return {}

    def clean_skill_list(value):

        if not isinstance(value, list):
            return []

        result = []

        for item in value:

            if isinstance(item, str):

                normalized = normalize_skill(item)

                if normalized and normalized not in result:
                    result.append(normalized)

        return result

    resume_skills = clean_skill_list(
        data.get("resume_skills", [])
    )

    required_skills = clean_skill_list(
        data.get("required_skills", [])
    )

    preferred_skills = clean_skill_list(
        data.get("preferred_skills", [])
    )

    matched = clean_skill_list(
        data.get("matched", [])
    )

    missing = clean_skill_list(
        data.get("missing", [])
    )

    # Recalculate consistency
    if required_skills:

        matched = [
            skill
            for skill in required_skills
            if skill in resume_skills
        ]

        missing = [
            skill
            for skill in required_skills
            if skill not in resume_skills
        ]

    transferable = data.get(
        "transferable",
        []
    )

    if not isinstance(transferable, list):
        transferable = []

    clean_transferable = []

    for item in transferable:

        if isinstance(item, dict):

            source = normalize_skill(
                str(item.get("from", ""))
            )

            target = normalize_skill(
                str(item.get("to", ""))
            )

            reason = str(
                item.get("reason", "")
            ).strip()

            if source and target:

                clean_transferable.append({
                    "from": source,
                    "to": target,
                    "reason": reason
                })

    evidence = data.get(
        "evidence",
        {}
    )

    if not isinstance(evidence, dict):
        evidence = {}

    clean_evidence = {}

    for skill, statement in evidence.items():

        normalized_skill = normalize_skill(
            str(skill)
        )

        if normalized_skill:

            clean_evidence[normalized_skill] = str(
                statement
            ).strip()

    return {
        "resume_skills": resume_skills,
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "matched": matched,
        "missing": missing,
        "transferable": clean_transferable,
        "evidence": clean_evidence
    }


# ============================================================
# MAIN FUNCTION USED BY FLASK
# ============================================================

def analyze_resume_and_job(resume_text, job_description):
    """
    Main function used by app.py.

    It first tries Gemini.
    If Gemini fails, local analysis is used.
    """

    resume_text = clean_text(resume_text)

    job_description = clean_text(
        job_description
    )

    if not resume_text:
        raise ValueError(
            "Resume text is empty."
        )

    if not job_description:
        raise ValueError(
            "Job description is empty."
        )

    print("2. Understanding resume and job...")

    # --------------------------------------------------------
    # Try Gemini
    # --------------------------------------------------------

    gemini_result = try_gemini(
        resume_text,
        job_description
    )

    if gemini_result:

        result = normalize_ai_result(
            gemini_result
        )

        # Make sure missing fields are not empty
        if not result["resume_skills"]:
            result["resume_skills"] = extract_skills(
                resume_text
            )

        if not result["required_skills"]:
            result["required_skills"] = extract_required_skills(
                job_description
            )

        if not result["preferred_skills"]:
            result["preferred_skills"] = extract_preferred_skills(
                job_description
            )

        # Recalculate match/missing using actual detected skills
        result["matched"] = [
            skill
            for skill in result["required_skills"]
            if skill in result["resume_skills"]
        ]

        result["missing"] = [
            skill
            for skill in result["required_skills"]
            if skill not in result["resume_skills"]
        ]

        if not result["evidence"]:
            result["evidence"] = get_skill_evidence(
                resume_text,
                result["matched"]
            )

        return result

    # --------------------------------------------------------
    # Local fallback
    # --------------------------------------------------------

    print(
        "Using local skill analysis..."
    )

    return local_analysis(
        resume_text,
        job_description
    )


# ============================================================
# SIMPLE TEST
# ============================================================

if __name__ == "__main__":

    sample_resume = """
    Python developer with experience in Flask,
    SQL, HTML, CSS and Git.
    Worked on machine learning and NLP projects.
    """

    sample_job = """
    We are hiring a Frontend Developer.

    Required skills:
    HTML, CSS, JavaScript, React and Git.

    Preferred skills:
    TypeScript and Next.js.
    """

    print("\n===================================")
    print("      CAREERPILOT AI TEST")
    print("===================================\n")

    result = analyze_resume_and_job(
        sample_resume,
        sample_job
    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )