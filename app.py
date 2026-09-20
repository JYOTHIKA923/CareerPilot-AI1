from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

import os
import threading
import webbrowser

from resume_parser import extract_text_from_pdf
from ai_agent import analyze_resume_and_job
from skill_engine import calculate_skill_gap, find_evidence
from roadmap_generator import create_career_plan


# =========================================================
# LOAD ENVIRONMENT
# =========================================================

load_dotenv()


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# HEALTH CHECK
# Useful for deployment
# =========================================================

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "application": "CareerPilot AI"
    })


# =========================================================
# ANALYZE RESUME + JOB DESCRIPTION
# =========================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        print("\n")
        print("=" * 60)
        print("             CAREERPILOT AI ANALYSIS")
        print("=" * 60)


        # -----------------------------------------------------
        # 1. GET RESUME
        # -----------------------------------------------------

        resume_file = request.files.get("resume")

        if resume_file is None:

            return jsonify({
                "error": "Please upload your resume PDF."
            }), 400


        if resume_file.filename == "":

            return jsonify({
                "error": "Please select a resume PDF."
            }), 400


        # -----------------------------------------------------
        # 2. CHECK PDF
        # -----------------------------------------------------

        original_filename = resume_file.filename

        if not original_filename.lower().endswith(".pdf"):

            return jsonify({
                "error": "Only PDF resume files are supported."
            }), 400


        # -----------------------------------------------------
        # 3. GET JOB DESCRIPTION
        # -----------------------------------------------------

        job_description = request.form.get(
            "job_description",
            ""
        ).strip()


        if not job_description:

            return jsonify({
                "error": "Please enter a job description."
            }), 400


        if len(job_description) < 20:

            return jsonify({
                "error": "Please enter a more complete job description."
            }), 400


        print("Resume:", original_filename)
        print(
            "Job description length:",
            len(job_description)
        )


        # -----------------------------------------------------
        # 4. SAVE RESUME
        # -----------------------------------------------------

        filename = secure_filename(
            original_filename
        )


        # Avoid problems when two resumes have same name

        base_name, extension = os.path.splitext(
            filename
        )

        counter = 1

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )


        while os.path.exists(file_path):

            filename = (
                base_name
                + "_"
                + str(counter)
                + extension
            )

            file_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            counter += 1


        resume_file.save(file_path)


        print(
            "Resume saved:",
            file_path
        )


        # -----------------------------------------------------
        # 5. EXTRACT RESUME TEXT
        # -----------------------------------------------------

        print("\n[1/4] Reading resume...")

        resume_text = extract_text_from_pdf(
            file_path
        )


        if not resume_text:

            return jsonify({
                "error":
                "Could not extract text from this PDF. "
                "Please upload a text-based PDF resume."
            }), 400


        resume_text = resume_text.strip()


        print(
            "Resume text length:",
            len(resume_text)
        )


        if len(resume_text) < 30:

            return jsonify({
                "error":
                "Very little text was found in the resume. "
                "Please upload a readable PDF resume."
            }), 400


        # -----------------------------------------------------
        # 6. ANALYZE RESUME + JOB
        # -----------------------------------------------------

        print("\n[2/4] Understanding resume and job...")


        analysis = analyze_resume_and_job(
            resume_text,
            job_description
        )


        resume_skills = analysis.get(
            "resume_skills",
            []
        )

        required_skills = analysis.get(
            "required_skills",
            []
        )

        preferred_skills = analysis.get(
            "preferred_skills",
            []
        )


        print("\nDetected Resume Skills:")

        print(resume_skills)


        print("\nRequired Job Skills:")

        print(required_skills)


        print("\nPreferred Job Skills:")

        print(preferred_skills)


        # -----------------------------------------------------
        # 7. CALCULATE SKILL GAP
        # -----------------------------------------------------

        print("\n[3/4] Calculating skill gap...")


        resume_data = {
            "skills": resume_skills
        }


        job_data = {

            "required_skills":
            required_skills,

            "preferred_skills":
            preferred_skills
        }


        gap = calculate_skill_gap(
            resume_data,
            job_data
        )


        matched = gap.get(
            "matched",
            []
        )


        missing = gap.get(
            "missing",
            []
        )


        transferable = gap.get(
            "transferable",
            []
        )


        score = gap.get(
            "score",
            0
        )


        # -----------------------------------------------------
        # 8. FIND EVIDENCE
        # -----------------------------------------------------

        evidence = {}


        for skill in matched:

            try:

                evidence[skill] = find_evidence(
                    resume_text,
                    skill
                )

            except Exception:

                evidence[skill] = ""


        # -----------------------------------------------------
        # 9. CREATE ROADMAP
        # -----------------------------------------------------

        print("\n[4/4] Creating career roadmap...")


        try:

            career_plan = create_career_plan(
                missing,
                resume_data,
                job_data
            )

        except Exception as roadmap_error:

            print(
                "Roadmap error:",
                roadmap_error
            )

            career_plan = {

                "top_gaps":
                missing[:3],

                "roadmap":
                [],

                "project":
                {}

            }


        # -----------------------------------------------------
        # 10. FINAL RESULT
        # -----------------------------------------------------

        result = {

            "score":
            score,

            "matched":
            matched,

            "missing":
            missing,

            "transferable":
            transferable,

            "evidence":
            evidence,

            "top_gaps":
            career_plan.get(
                "top_gaps",
                missing[:3]
            ),

            "roadmap":
            career_plan.get(
                "roadmap",
                []
            ),

            "project":
            career_plan.get(
                "project",
                {}
            ),

            "resume_skills":
            resume_skills,

            "required_skills":
            required_skills,

            "preferred_skills":
            preferred_skills

        }


        # -----------------------------------------------------
        # PRINT RESULT
        # -----------------------------------------------------

        print("\n")
        print("-" * 60)
        print("ANALYSIS COMPLETED")
        print("-" * 60)

        print(
            "Resume Skills:",
            resume_skills
        )

        print(
            "Required Skills:",
            required_skills
        )

        print(
            "Preferred Skills:",
            preferred_skills
        )

        print(
            "Matched:",
            matched
        )

        print(
            "Missing:",
            missing
        )

        print(
            "Transferable:",
            transferable
        )

        print(
            "Match Score:",
            score,
            "%"
        )

        print("-" * 60)


        return jsonify(result), 200


    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as error:

        print("\n")
        print("=" * 60)
        print("CAREERPILOT ERROR")
        print("=" * 60)

        print(
            type(error).__name__,
            ":",
            str(error)
        )

        print("=" * 60)


        return jsonify({

            "error":
            "Career analysis failed: "
            + str(error)

        }), 500


# =========================================================
# OPEN BROWSER
# =========================================================

def open_browser():

    try:

        webbrowser.open(
            "http://127.0.0.1:5000/"
        )

    except Exception:

        pass


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 60)
    print("                 CAREERPILOT AI")
    print("=" * 60)
    print("Dashboard:")
    print("http://127.0.0.1:5000/")
    print("")
    print("Health:")
    print("http://127.0.0.1:5000/health")
    print("=" * 60)
    print("\n")


    threading.Timer(
        1.5,
        open_browser
    ).start()


    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )