"""Lightweight, explainable career recommendation engine using a built-in starter knowledge base."""
ROLE_DATA = {
    "Data Scientist": {
        "skills": ["Python", "SQL", "Statistics", "Machine Learning", "Data Visualization", "Git"],
        "projects": [
            {"title": "Student Performance Insights", "description": "Explore a dataset, clean it, visualise patterns, and explain findings.", "level": "Beginner", "evidence": "Notebook, charts, and a concise README."},
            {"title": "End-to-End Prediction API", "description": "Train and evaluate a baseline model, then expose predictions through a small app.", "level": "Intermediate", "evidence": "Metrics, limitations, API demo, and reproducible code."},
            {"title": "Career Skills Dashboard", "description": "Create a dashboard that compares role requirements with a user's skill profile.", "level": "Intermediate", "evidence": "Interactive dashboard and documented assumptions."},
        ],
    },
    "Machine Learning Engineer": {
        "skills": ["Python", "SQL", "Machine Learning", "Git", "APIs", "Model Evaluation", "Deployment"],
        "projects": [
            {"title": "Model Evaluation Workbench", "description": "Compare baseline models with cross-validation and clear error analysis.", "level": "Intermediate", "evidence": "Experiment table, plots, and reproducible notebook."},
            {"title": "Prediction Service", "description": "Wrap a trained model in an API with input validation and tests.", "level": "Intermediate", "evidence": "Working endpoint, tests, and deployment notes."},
            {"title": "Data Drift Monitor", "description": "Compare reference and incoming feature distributions with a simple alert report.", "level": "Advanced", "evidence": "Monitoring report and documented thresholds."},
        ],
    },
    "Python Developer": {
        "skills": ["Python", "SQL", "Git", "APIs", "Testing", "Deployment"],
        "projects": [
            {"title": "Student Records API", "description": "Build CRUD endpoints with validation, tests, and structured errors.", "level": "Beginner", "evidence": "API documentation and automated tests."},
            {"title": "Task Tracker", "description": "Create a small application with persistent data and a clean interface.", "level": "Beginner", "evidence": "Deployed app, source code, and setup instructions."},
            {"title": "Service Health Dashboard", "description": "Track service status and latency using a small monitoring interface.", "level": "Intermediate", "evidence": "Metrics, failure states, and test notes."},
        ],
    },
    "Data Analyst": {
        "skills": ["SQL", "Data Visualization", "Statistics", "Excel", "Python", "Communication"],
        "projects": [
            {"title": "Business KPI Dashboard", "description": "Turn a clean dataset into a dashboard with KPIs and actionable insights.", "level": "Beginner", "evidence": "Dashboard, metric definitions, and insight summary."},
            {"title": "Customer Cohort Analysis", "description": "Use SQL or Python to compare retention across customer groups.", "level": "Intermediate", "evidence": "Queries, charts, and business recommendations."},
            {"title": "Data Quality Audit", "description": "Detect missing values, duplicates, outliers, and inconsistent categories.", "level": "Beginner", "evidence": "Audit report and repeatable cleaning steps."},
        ],
    },
    "Cloud / DevOps Engineer": {
        "skills": ["Linux", "Git", "Networking", "Cloud Fundamentals", "Docker", "CI/CD", "Monitoring"],
        "projects": [
            {"title": "Automated App Deployment", "description": "Package a small app and document a repeatable deployment pipeline.", "level": "Intermediate", "evidence": "Pipeline configuration and deployment run."},
            {"title": "Cloud Cost Review", "description": "Create a resource inventory, identify idle resources, and propose cost controls.", "level": "Beginner", "evidence": "Cost assumptions, recommendations, and risk notes."},
            {"title": "Service Monitoring Lab", "description": "Track health checks, logs, and response times for a sample service.", "level": "Intermediate", "evidence": "Dashboard and incident walkthrough."},
        ],
    },
}
RESOURCES = [
    {"title":"Python Tutorial", "provider":"Python.org", "type":"Documentation", "skills":"Python", "description":"Official language tutorial and reference material.", "url":"https://docs.python.org/3/tutorial/", "free":True},
    {"title":"SQLBolt", "provider":"SQLBolt", "type":"Interactive practice", "skills":"SQL", "description":"Short lessons and exercises for learning SQL fundamentals.", "url":"https://sqlbolt.com/", "free":True},
    {"title":"Kaggle Learn", "provider":"Kaggle", "type":"Micro-courses", "skills":"Python, Pandas, Data Visualization, Machine Learning", "description":"Short, practical courses with notebook-based exercises.", "url":"https://www.kaggle.com/learn", "free":True},
    {"title":"scikit-learn User Guide", "provider":"scikit-learn", "type":"Documentation", "skills":"Machine Learning, Model Evaluation", "description":"Model selection, preprocessing, metrics, and estimator guidance.", "url":"https://scikit-learn.org/stable/user_guide.html", "free":True},
    {"title":"GitHub Skills", "provider":"GitHub", "type":"Hands-on learning", "skills":"Git, CI/CD", "description":"Interactive exercises for GitHub workflows and collaboration.", "url":"https://skills.github.com/", "free":True},
    {"title":"freeCodeCamp", "provider":"freeCodeCamp", "type":"Guided curriculum", "skills":"Python, APIs, SQL, Deployment", "description":"Free coding lessons and practice projects across web and data topics.", "url":"https://www.freecodecamp.org/learn/", "free":True},
    {"title":"Google Machine Learning Crash Course", "provider":"Google", "type":"Course", "skills":"Machine Learning, Statistics", "description":"Practical introduction to machine learning concepts and exercises.", "url":"https://developers.google.com/machine-learning/crash-course", "free":True},
    {"title":"Microsoft Learn", "provider":"Microsoft", "type":"Learning paths", "skills":"Cloud Fundamentals, Networking, Monitoring", "description":"Structured learning paths for cloud and technical fundamentals.", "url":"https://learn.microsoft.com/training/", "free":True},
    {"title":"Docker Get Started", "provider":"Docker", "type":"Documentation", "skills":"Docker, Deployment", "description":"Learn container fundamentals and the basic Docker workflow.", "url":"https://docs.docker.com/get-started/", "free":True},
    {"title":"LeetCode", "provider":"LeetCode", "type":"Practice platform", "skills":"Python, SQL, Interview preparation", "description":"Coding and SQL practice; some content may require a subscription.", "url":"https://leetcode.com/", "free":True},
]

def recommend(profile):
    role = profile.get("target_role", "Data Scientist")
    role_data = ROLE_DATA.get(role, ROLE_DATA["Data Scientist"])
    have = {s.lower() for s in profile.get("skills", [])}
    gaps = [s for s in role_data["skills"] if s.lower() not in have]
    interests = profile.get("interests", "").strip()
    hours = int(profile.get("weekly_hours", 6))
    actions = []
    if gaps:
        actions.append({
            "title": f"Build your {gaps[0]} foundation",
            "description": f"Complete one focused lesson, then solve a small exercise that demonstrates {gaps[0]}.",
            "focus": gaps[0], "effort": f"{max(1, min(3, hours // 3))} hours"
        })
    else:
        actions.append({
            "title": "Validate your skills with evidence",
            "description": "Choose one role skill and publish a small project or assessment result that demonstrates it.",
            "focus": "Portfolio evidence", "effort": f"{max(1, min(3, hours // 3))} hours"
        })
    actions.append({
        "title": "Ship one portfolio milestone",
        "description": f"Move one project forward with a clear README, reproducible steps, and a short explanation of trade-offs. Interests: {interests or 'not specified'}.",
        "focus": "Project delivery", "effort": f"{max(1, min(4, hours // 2))} hours"
    })
    actions.append({
        "title": "Practise communicating your work",
        "description": "Explain one project in 90 seconds: problem, approach, result, limitation, and next improvement.",
        "focus": "Interview communication", "effort": "30 minutes"
    })
    return {"actions": actions, "projects": role_data["projects"], "gaps": gaps}
