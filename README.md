# CareerPilot-AI1
AI-powered career assistant that analyzes resumes and job descriptions to identify skill gaps, calculate job-match scores, and generate personalized career roadmaps.
# 🚀 CareerPilot AI

**CareerPilot AI** is an AI-powered career assistant that helps students and job seekers understand how well their resume matches a target job and what skills they need to develop.

It analyzes a **resume PDF** and a **job description**, identifies matched and missing skills, finds transferable skills, calculates a match score, and generates a personalized career roadmap.

---

## ✨ Features

* 📄 Upload any resume in PDF format
* 📝 Enter any job description
* 🤖 AI-powered resume and job description analysis
* 🎯 Job match percentage
* ✅ Matched skills identification
* ❌ Missing skill identification
* 🔄 Transferable skill detection
* 📌 Top skill-gap identification
* 🗺️ Personalized career roadmap
* 💡 Recommended project based on skill gaps
* 📊 Interactive career analysis dashboard
* 📜 Career analysis history
* ⚙️ User settings
* 🎨 Clean and responsive user interface

---

## 🔄 How CareerPilot AI Works

```text
              CAREERPILOT AI
                    │
                    ▼
          Upload Resume + Job Description
                    │
                    ▼
             AI Skill Analysis
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
     MATCHED      MISSING   TRANSFERABLE
        │           │           │
        └───────────┼───────────┘
                    ▼
               MATCH SCORE
                    │
                    ▼
                SKILL GAPS
                    │
                    ▼
             CAREER ROADMAP
                    │
                    ▼
          RECOMMENDED PROJECT
                    │
                    ▼
              CAREER REPORT
```

---

## 🛠️ Technologies Used

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* Flask

### AI

* Google Gemini API

### Resume Processing

* PyPDF

### Environment Management

* Python-dotenv

### Deployment

* Render

### Version Control

* Git
* GitHub

---

## 📁 Project Structure

```text
CareerPilot-AI/
│
├── app.py
├── ai_agent.py
├── resume_parser.py
├── skill_engine.py
├── roadmap_generator.py
├── requirements.txt
├── .gitignore
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
└── uploads/
```

> API keys, virtual environments, uploaded resumes, and other sensitive/local files are excluded using `.gitignore`.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/JYOTHIKA923/CareerPilot-AI.git
```

### 2. Open the project

```bash
cd CareerPilot-AI
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

#### Windows

```powershell
venv\Scripts\Activate.ps1
```

#### macOS/Linux

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_gemini_api_key
```

**Never upload `.env` to GitHub.**

The `.gitignore` file should contain:

```text
venv/
.env
__pycache__/
uploads/
*.pyc
careerpilot.db
```

---

## ▶️ Run Locally

Start the Flask application:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

---

## 🧪 Example Workflow

1. Open CareerPilot AI.
2. Upload your resume PDF.
3. Paste the job description.
4. Click **Analyze**.
5. CareerPilot AI analyzes both inputs.
6. View your match percentage.
7. Review matched skills.
8. Review missing skills.
9. Check transferable skills.
10. Follow the personalized career roadmap.
11. Work on the recommended project.

---

## 🎯 Problem It Solves

Students and job seekers often struggle to understand:

* Which skills a job actually requires
* Which skills they already have
* Which skills are missing
* How their existing skills can transfer to another technology
* What they should learn next
* Which projects can strengthen their profile

CareerPilot AI brings these steps together into one career analysis platform.

---

## 🔮 Future Enhancements

* 📄 Automated career report generation
* 🔗 LinkedIn profile analysis
* 💼 Job recommendation system
* 📚 Course recommendations
* 🧠 Interview question generation
* 📈 Skill progress tracking
* ☁️ Cloud-based resume storage
* 👤 User authentication
* 📊 Advanced career analytics
* 💬 AI career assistant chatbot

---

## 👥 Project Team

**CareerPilot AI**
Developed as an AI-powered career guidance and skill-gap analysis project.

---

## 📄 License

This project is developed for educational and project demonstration purposes.
