document.addEventListener("DOMContentLoaded", function () {

    console.log("CareerPilot AI loaded");


    /* =====================================================
       ELEMENTS
       ===================================================== */

    const form =
        document.getElementById("analysis-form");

    const resumeInput =
        document.getElementById("resume");

    const fileName =
        document.getElementById("file-name");

    const jobDescription =
        document.getElementById("job_description");

    const analyzeButton =
        document.getElementById("analyze-btn");

    const loading =
        document.getElementById("loading");

    const results =
        document.getElementById("results");

    const toast =
        document.getElementById("toast");



    /* =====================================================
       FILE SELECTION
       ===================================================== */

    if (resumeInput) {

        resumeInput.addEventListener(
            "change",
            function () {

                if (!this.files || !this.files.length) {

                    if (fileName) {
                        fileName.textContent =
                            "No resume selected";
                    }

                    return;
                }

                const file = this.files[0];

                if (
                    file.type !== "application/pdf" &&
                    !file.name.toLowerCase().endsWith(".pdf")
                ) {

                    alert(
                        "Please select a PDF resume."
                    );

                    this.value = "";

                    if (fileName) {
                        fileName.textContent =
                            "No resume selected";
                    }

                    return;
                }

                if (fileName) {

                    fileName.textContent =
                        "✓ " + file.name;
                }

            }
        );
    }



    /* =====================================================
       FORM SUBMISSION
       ===================================================== */

    if (form) {

        form.addEventListener(
            "submit",
            async function (event) {

                event.preventDefault();

                console.log(
                    "Career analysis started"
                );


                /* Validate resume */

                if (
                    !resumeInput ||
                    !resumeInput.files ||
                    !resumeInput.files.length
                ) {

                    showToast(
                        "Please upload your resume PDF."
                    );

                    return;
                }


                /* Validate JD */

                if (
                    !jobDescription ||
                    !jobDescription.value.trim()
                ) {

                    showToast(
                        "Please enter a job description."
                    );

                    return;
                }


                /* Prepare */

                const formData =
                    new FormData(form);


                /* Loading */

                if (analyzeButton) {

                    analyzeButton.disabled = true;

                    analyzeButton.textContent =
                        "⏳ Analyzing...";
                }

                if (loading) {
                    loading.classList.remove("hidden");
                }

                if (results) {
                    results.classList.add("hidden");
                }


                try {

                    const response =
                        await fetch(
                            "/analyze",
                            {
                                method: "POST",
                                body: formData
                            }
                        );


                    const rawText =
                        await response.text();


                    console.log(
                        "Server response:",
                        rawText
                    );


                    let data;

                    try {

                        data =
                            JSON.parse(rawText);

                    } catch (jsonError) {

                        throw new Error(
                            "Server returned an invalid response."
                        );
                    }


                    if (!response.ok) {

                        throw new Error(
                            data.error ||
                            "Analysis failed."
                        );
                    }


                    if (data.error) {

                        throw new Error(
                            data.error
                        );
                    }


                    console.log(
                        "Analysis result:",
                        data
                    );


                    /* Render */

                    renderResults(data);


                    /* Show results */

                    if (loading) {
                        loading.classList.add("hidden");
                    }

                    if (results) {
                        results.classList.remove("hidden");
                    }


                    /* Save */

                    saveHistory(data);


                    /* Scroll */

                    setTimeout(function () {

                        if (results) {

                            results.scrollIntoView({
                                behavior: "smooth",
                                block: "start"
                            });

                        }

                    }, 150);


                    showToast(
                        "Analysis completed successfully!"
                    );


                } catch (error) {

                    console.error(
                        "Analysis error:",
                        error
                    );


                    if (loading) {
                        loading.classList.add("hidden");
                    }


                    showToast(
                        error.message ||
                        "Something went wrong."
                    );


                    alert(
                        error.message ||
                        "Something went wrong."
                    );


                } finally {

                    if (analyzeButton) {

                        analyzeButton.disabled =
                            false;

                        analyzeButton.textContent =
                            "🚀 Analyze Career Match";
                    }

                }

            }
        );
    }



    /* =====================================================
       RENDER RESULTS
       ===================================================== */

    function renderResults(data) {

        const scoreValue =
            document.getElementById("score-value");

        const matchedCount =
            document.getElementById("matched-count");

        const missingCount =
            document.getElementById("missing-count");

        const transferableCount =
            document.getElementById(
                "transferable-count"
            );


        const matched =
            Array.isArray(data.matched)
                ? data.matched
                : [];

        const missing =
            Array.isArray(data.missing)
                ? data.missing
                : [];

        const transferable =
            Array.isArray(data.transferable)
                ? data.transferable
                : [];


        /* Score */

        if (scoreValue) {

            scoreValue.textContent =
                String(data.score || 0) + "%";
        }


        /* Counts */

        if (matchedCount) {

            matchedCount.textContent =
                matched.length;
        }

        if (missingCount) {

            missingCount.textContent =
                missing.length;
        }

        if (transferableCount) {

            transferableCount.textContent =
                transferable.length;
        }


        /* Skills */

        renderSkills(
            "matched-skills",
            matched,
            false
        );

        renderSkills(
            "missing-skills",
            missing,
            true
        );


        /* Transferable */

        renderTransferable(
            transferable
        );


        /* Evidence */

        renderEvidence(
            data.evidence || {},
            matched
        );


        /* Top gaps */

        renderTopGaps(
            data.top_gaps || missing
        );


        /* Roadmap */

        renderRoadmap(
            data.roadmap || []
        );


        /* Project */

        renderProject(
            data.project || {}
        );
    }



    /* =====================================================
       SKILLS
       ===================================================== */

    function renderSkills(
        elementId,
        skills,
        isMissing
    ) {

        const container =
            document.getElementById(elementId);

        if (!container) {
            return;
        }


        container.innerHTML = "";


        if (!skills.length) {

            container.innerHTML =
                '<div class="empty-skill">None found</div>';

            return;
        }


        skills.forEach(function (skill) {

            const div =
                document.createElement("div");

            div.className =
                isMissing
                    ? "skill missing"
                    : "skill";

            div.textContent =
                formatSkill(skill);

            container.appendChild(div);

        });
    }



    /* =====================================================
       TRANSFERABLE
       ===================================================== */

    function renderTransferable(items) {

        const container =
            document.getElementById(
                "transferable-skills"
            );

        if (!container) {
            return;
        }


        container.innerHTML = "";


        if (!items.length) {

            container.innerHTML =
                '<div class="empty-skill">None found</div>';

            return;
        }


        items.forEach(function (item) {

            const div =
                document.createElement("div");

            div.className =
                "transferable-item";


            if (typeof item === "string") {

                div.textContent =
                    item;

            } else {

                const from =
                    item.from || "Existing skill";

                const to =
                    item.to || "Related skill";

                const reason =
                    item.reason || "";


                div.innerHTML =
                    "<strong>" +
                    escapeHtml(
                        formatSkill(from)
                    ) +
                    " → " +
                    escapeHtml(
                        formatSkill(to)
                    ) +
                    "</strong>" +
                    (
                        reason
                            ? "<br>" +
                              escapeHtml(reason)
                            : ""
                    );
            }


            container.appendChild(div);

        });
    }



    /* =====================================================
       EVIDENCE
       ===================================================== */

    function renderEvidence(
        evidence,
        matched
    ) {

        const container =
            document.getElementById(
                "evidence"
            );

        if (!container) {
            return;
        }


        container.innerHTML = "";


        let hasEvidence = false;


        matched.forEach(function (skill) {

            const text =
                evidence[skill];


            if (!text) {
                return;
            }


            hasEvidence = true;


            const div =
                document.createElement("div");

            div.className =
                "evidence-item";


            div.innerHTML =
                '<span class="evidence-skill">' +
                escapeHtml(
                    formatSkill(skill)
                ) +
                "</span>" +
                '<div class="evidence-text">' +
                escapeHtml(text) +
                "</div>";


            container.appendChild(div);

        });


        if (!hasEvidence) {

            container.innerHTML =
                '<div class="empty-skill">' +
                "No specific evidence found." +
                "</div>";
        }
    }



    /* =====================================================
       TOP GAPS
       ===================================================== */

    function renderTopGaps(gaps) {

        const container =
            document.getElementById(
                "top-gaps"
            );

        if (!container) {
            return;
        }


        container.innerHTML = "";


        if (!gaps.length) {

            container.innerHTML =
                '<div class="empty-skill">' +
                "No major skill gaps found." +
                "</div>";

            return;
        }


        gaps.forEach(function (gap, index) {

            const div =
                document.createElement("div");

            div.className =
                "gap-item";


            div.innerHTML =
                "<strong>" +
                (index + 1) +
                ". " +
                escapeHtml(
                    formatSkill(
                        typeof gap === "string"
                            ? gap
                            : gap.skill || gap.name || ""
                    )
                ) +
                "</strong>";


            container.appendChild(div);

        });
    }



    /* =====================================================
       ROADMAP
       ===================================================== */

    function renderRoadmap(steps) {

        const container =
            document.getElementById(
                "roadmap"
            );

        if (!container) {
            return;
        }


        container.innerHTML = "";


        if (!steps.length) {

            container.innerHTML =
                '<div class="empty-skill">' +
                "Roadmap will appear after analysis." +
                "</div>";

            return;
        }


        steps.forEach(function (step, index) {

            const div =
                document.createElement("div");

            div.className =
                "roadmap-step";


            let title = "";
            let description = "";


            if (typeof step === "string") {

                title =
                    "Step " + (index + 1);

                description =
                    step;

            } else {

                title =
                    step.title ||
                    step.skill ||
                    "Step " + (index + 1);

                description =
                    step.description ||
                    step.action ||
                    step.details ||
                    "";
            }


            div.innerHTML =
                '<div class="step-number">' +
                (index + 1) +
                "</div>" +

                '<div class="step-content">' +

                "<h3>" +
                escapeHtml(
                    formatSkill(title)
                ) +
                "</h3>" +

                "<p>" +
                escapeHtml(description) +
                "</p>" +

                "</div>";


            container.appendChild(div);

        });
    }



    /* =====================================================
       PROJECT
       ===================================================== */

    function renderProject(project) {

        const container =
            document.getElementById(
                "project-content"
            );

        if (!container) {
            return;
        }


        container.innerHTML = "";


        if (!project ||
            Object.keys(project).length === 0) {

            container.innerHTML =
                "<p>No project recommendation available.</p>";

            return;
        }


        const title =
            project.title ||
            project.name ||
            "Recommended Skill Gap Project";


        const description =
            project.description ||
            project.summary ||
            "";


        let html =
            "<h3>" +
            escapeHtml(title) +
            "</h3>";


        if (description) {

            html +=
                "<p>" +
                escapeHtml(description) +
                "</p>";
        }


        if (
            Array.isArray(project.skills) &&
            project.skills.length
        ) {

            html +=
                "<strong>Skills:</strong>" +
                "<ul>";


            project.skills.forEach(function (skill) {

                html +=
                    "<li>" +
                    escapeHtml(
                        formatSkill(skill)
                    ) +
                    "</li>";

            });


            html += "</ul>";
        }


        if (project.goal) {

            html +=
                "<p><strong>Goal:</strong> " +
                escapeHtml(project.goal) +
                "</p>";
        }


        container.innerHTML =
            html;
    }



    /* =====================================================
       NAVIGATION
       ===================================================== */

    const navItems =
        document.querySelectorAll(
            ".nav-item"
        );

    const sections =
        document.querySelectorAll(
            ".page-section"
        );


    navItems.forEach(function (button) {

        button.addEventListener(
            "click",
            function () {

                const sectionId =
                    this.dataset.section;


                showSection(
                    sectionId
                );

            }
        );

    });


    function showSection(sectionId) {

        sections.forEach(function (section) {

            section.classList.remove(
                "active-section"
            );

        });


        navItems.forEach(function (item) {

            item.classList.remove(
                "active"
            );

        });


        const target =
            document.getElementById(
                sectionId
            );


        if (target) {

            target.classList.add(
                "active-section"
            );
        }


        const activeButton =
            document.querySelector(
                '.nav-item[data-section="' +
                sectionId +
                '"]'
            );


        if (activeButton) {

            activeButton.classList.add(
                "active"
            );
        }


        updatePageTitle(
            sectionId
        );


        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });


        if (sectionId === "history") {

            renderHistory();
        }
    }



    /* =====================================================
       PAGE TITLES
       ===================================================== */

    function updatePageTitle(section) {

        const title =
            document.getElementById(
                "page-title"
            );

        const subtitle =
            document.getElementById(
                "page-subtitle"
            );


        const data = {

            dashboard: [
                "Dashboard",
                "Analyze your resume against any job description."
            ],

            analysis: [
                "Skill Analysis",
                "Understand your current skills and job requirements."
            ],

            roadmap: [
                "Career Roadmap",
                "Build the skills needed for your target role."
            ],

            history: [
                "Analysis History",
                "Review your previous career analyses."
            ],

            settings: [
                "Settings",
                "Manage your CareerPilot preferences."
            ]

        };


        if (data[section]) {

            title.textContent =
                data[section][0];

            subtitle.textContent =
                data[section][1];
        }
    }



    /* =====================================================
       GO DASHBOARD
       ===================================================== */

    document
        .querySelectorAll(
            "[data-go-dashboard]"
        )
        .forEach(function (button) {

            button.addEventListener(
                "click",
                function () {

                    showSection(
                        "dashboard"
                    );

                }
            );

        });



    /* =====================================================
       CLEAR RESULTS
       ===================================================== */

    const clearResults =
        document.getElementById(
            "clear-results"
        );


    if (clearResults) {

        clearResults.addEventListener(
            "click",
            function () {

                if (results) {

                    results.classList.add(
                        "hidden"
                    );
                }


                if (form) {
                    form.reset();
                }


                if (fileName) {

                    fileName.textContent =
                        "No resume selected";
                }


                showToast(
                    "Results cleared."
                );

            }
        );
    }



    /* =====================================================
       HISTORY
       ===================================================== */

    function saveHistory(data) {

        try {

            const history =
                JSON.parse(
                    localStorage.getItem(
                        "careerpilot_history"
                    ) || "[]"
                );


            history.unshift({

                id: Date.now(),

                date:
                    new Date().toLocaleString(),

                score:
                    data.score || 0,

                matched:
                    data.matched || [],

                missing:
                    data.missing || [],

                resumeSkills:
                    data.resume_skills || [],

                requiredSkills:
                    data.required_skills || []

            });


            localStorage.setItem(
                "careerpilot_history",
                JSON.stringify(
                    history.slice(0, 20)
                )
            );

        } catch (error) {

            console.error(
                "History save error:",
                error
            );
        }
    }



    function renderHistory() {

        const container =
            document.getElementById(
                "history-list"
            );

        if (!container) {
            return;
        }


        let history = [];


        try {

            history =
                JSON.parse(
                    localStorage.getItem(
                        "careerpilot_history"
                    ) || "[]"
                );

        } catch (error) {

            history = [];
        }


        container.innerHTML = "";


        if (!history.length) {

            container.innerHTML =
                '<div class="page-card">' +
                '<p>No analysis history yet.</p>' +
                "</div>";

            return;
        }


        history.forEach(function (item) {

            const div =
                document.createElement("div");

            div.className =
                "history-item";


            div.innerHTML =
                "<div>" +

                "<h3>" +
                "Career Analysis" +
                "</h3>" +

                "<p>" +
                escapeHtml(
                    item.date || ""
                ) +
                "</p>" +

                "</div>" +

                '<div class="history-score">' +
                escapeHtml(
                    String(
                        item.score || 0
                    )
                ) +
                "%" +
                "</div>" +

                '<div class="history-stats">' +
                "Matched: " +
                (
                    item.matched
                        ? item.matched.length
                        : 0
                ) +
                " · Missing: " +
                (
                    item.missing
                        ? item.missing.length
                        : 0
                ) +
                "</div>";


            container.appendChild(div);

        });
    }



    /* =====================================================
       CLEAR HISTORY
       ===================================================== */

    const clearHistory =
        document.getElementById(
            "clear-history"
        );


    if (clearHistory) {

        clearHistory.addEventListener(
            "click",
            function () {

                localStorage.removeItem(
                    "careerpilot_history"
                );

                renderHistory();

                showToast(
                    "History cleared."
                );

            }
        );
    }



    /* =====================================================
       CLEAR ALL DATA
       ===================================================== */

    const clearAllData =
        document.getElementById(
            "clear-all-data"
        );


    if (clearAllData) {

        clearAllData.addEventListener(
            "click",
            function () {

                localStorage.clear();

                renderHistory();

                showToast(
                    "Local data cleared."
                );

            }
        );
    }



    /* =====================================================
       TOAST
       ===================================================== */

    function showToast(message) {

        if (!toast) {
            return;
        }


        toast.textContent =
            message;


        toast.classList.remove(
            "hidden"
        );


        setTimeout(function () {

            toast.classList.add(
                "hidden"
            );

        }, 3000);
    }



    /* =====================================================
       FORMAT SKILL
       ===================================================== */

    function formatSkill(skill) {

        if (!skill) {
            return "";
        }


        const text =
            String(skill);


        return text
            .replace(/\bjavascript\b/gi, "JavaScript")
            .replace(/\btypescript\b/gi, "TypeScript")
            .replace(/\bhtml\b/gi, "HTML")
            .replace(/\bcss\b/gi, "CSS")
            .replace(/\breact\b/gi, "React")
            .replace(/\bnext\.?js\b/gi, "Next.js")
            .replace(/\bnode\.?js\b/gi, "Node.js")
            .replace(/\bpython\b/gi, "Python")
            .replace(/\bjava\b/gi, "Java")
            .replace(/\bsql\b/gi, "SQL")
            .replace(/\baws\b/gi, "AWS")
            .replace(/\bgcp\b/gi, "GCP")
            .replace(/\bazure\b/gi, "Azure")
            .replace(/\bgit\b/gi, "Git")
            .replace(/\bgithub\b/gi, "GitHub")
            .replace(/\bapi\b/gi, "API")
            .replace(/\bai\b/gi, "AI")
            .replace(/\bml\b/gi, "ML")
            .replace(/\bnlp\b/gi, "NLP");
    }



    /* =====================================================
       ESCAPE HTML
       ===================================================== */

    function escapeHtml(value) {

        return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }



    /* =====================================================
       INITIALIZE
       ===================================================== */

    renderHistory();

    console.log(
        "CareerPilot initialized successfully."
    );

});