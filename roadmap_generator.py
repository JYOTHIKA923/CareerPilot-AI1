def create_career_plan(
    missing_skills,
    matched_skills,
    job_description
):

    missing = []

    for item in missing_skills:

        if isinstance(item, dict):

            skill = item.get(
                "skill",
                ""
            )

        else:

            skill = str(item)

        if skill and skill not in missing:

            missing.append(skill)


    # --------------------------------------------------
    # TOP GAPS
    # --------------------------------------------------

    top_gaps = missing[:3]


    # --------------------------------------------------
    # ROADMAP
    # --------------------------------------------------

    roadmap = []


    for index, skill in enumerate(
        missing[:5],
        start=1
    ):

        skill_lower = skill.lower()


        if skill_lower in [
            "html",
            "css",
            "javascript",
            "typescript",
            "react",
            "angular",
            "vue",
            "next.js"
        ]:

            action = (
                f"Learn {skill} fundamentals "
                "and build a small responsive web page."
            )

            resource = "Online course + practice"


        elif skill_lower in [
            "python",
            "java",
            "c++",
            "c"
        ]:

            action = (
                f"Strengthen {skill} programming "
                "through coding exercises and a small project."
            )

            resource = "Programming practice"


        elif skill_lower in [
            "sql",
            "mysql",
            "postgresql",
            "mongodb"
        ]:

            action = (
                f"Practice {skill} database concepts "
                "and build CRUD operations."
            )

            resource = "Database practice"


        elif skill_lower in [
            "git",
            "github"
        ]:

            action = (
                f"Practice {skill} using branches, "
                "commits, pull requests and repositories."
            )

            resource = "Git practice"


        elif skill_lower in [
            "docker",
            "kubernetes",
            "terraform",
            "jenkins",
            "ci/cd"
        ]:

            action = (
                f"Learn {skill} fundamentals "
                "and apply them to a small deployment project."
            )

            resource = "DevOps hands-on lab"


        elif skill_lower in [
            "aws",
            "azure",
            "gcp"
        ]:

            action = (
                f"Learn {skill} core services "
                "and deploy a small application."
            )

            resource = "Cloud hands-on lab"


        elif skill_lower in [
            "machine learning",
            "deep learning",
            "artificial intelligence",
            "nlp"
        ]:

            action = (
                f"Study {skill} fundamentals "
                "and implement a small practical project."
            )

            resource = "ML/AI project"


        else:

            action = (
                f"Learn {skill} fundamentals "
                "and apply the skill in a practical project."
            )

            resource = "Documentation + practical project"


        roadmap.append({

            "step": index,

            "skill": skill,

            "action": action,

            "resource_type": resource
        })


    # --------------------------------------------------
    # PROJECT
    # --------------------------------------------------

    if missing:

        technologies = missing[:5]

        title = (
            "Skill Gap Practice Project"
        )

        description = (
            "Build a practical project that uses "
            + ", ".join(technologies)
            + " so the missing job skills can be demonstrated "
              "through actual implementation."
        )

        why = (
            "This project directly focuses on the skills "
            "identified as missing from the submitted resume."
        )

    else:

        technologies = []

        title = (
            "Portfolio Enhancement Project"
        )

        description = (
            "Build a project that combines the skills "
            "already present in the resume."
        )

        why = (
            "It can provide additional practical evidence "
            "of the existing skills."
        )


    return {

        "top_gaps": top_gaps,

        "roadmap": roadmap,

        "project": {

            "title": title,

            "description":
                description,

            "technologies":
                technologies,

            "why":
                why
        }
    }