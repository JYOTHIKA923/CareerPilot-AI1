from ai_agent import analyze_resume, analyze_job


resume = """
I am a Computer Science Engineering student.

I know Python, SQL, Flask and Git.

I developed a Digital Footprint Tracker
using Flask and MySQL.

I also completed a machine learning project
using Python.
"""


job = """
We are looking for a Backend Developer.

Required skills:
Python, FastAPI, SQL, Git.

Preferred skills:
Docker and AWS.

Good communication skills are required.
"""


print("\n===================================")
print("        RESUME ANALYSIS")
print("===================================\n")


resume_result = analyze_resume(
    resume
)

print(resume_result)


print("\n===================================")
print("          JOB ANALYSIS")
print("===================================\n")


job_result = analyze_job(
    job
)

print(job_result)