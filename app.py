import streamlit as st
import pandas as pd
from datetime import date, timedelta
from database import (
    init_db, get_profile, save_profile, get_goals, add_goal,
    toggle_goal, delete_goal, get_reflections, add_reflection,
)
from mentor_engine import ROLE_DATA, RESOURCES, recommend

st.set_page_config(
    page_title="Career Mentor | Student Career OS",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()

# ---------- Design system ----------
st.markdown("""
<style>
:root { --ink:#182230; --muted:#667085; --line:#e7ebf0; --brand:#3857d6; }
.block-container { padding-top: 1.4rem; padding-bottom: 2.5rem; max-width: 1440px; }
[data-testid="stSidebar"] { border-right: 1px solid #e7ebf0; }
[data-testid="stSidebar"] .block-container { padding-top: 1.8rem; }
.hero {
  padding: 1.35rem 1.55rem; border-radius: 18px;
  background: linear-gradient(120deg, #162a52 0%, #304fc4 65%, #5979ed 100%);
  color: white; margin-bottom: 1rem;
}
.hero h1 { color: white; font-size: 2rem; margin: 0 0 .35rem 0; }
.hero p { color: #e8edff; margin: 0; font-size: 1rem; }
.eyebrow { text-transform: uppercase; letter-spacing: .12em; font-size: .72rem; font-weight: 700; color: #9eb3ff; }
.section-label { font-size: .78rem; text-transform: uppercase; letter-spacing: .09em; color: #667085; font-weight: 700; }
.panel {
  border: 1px solid #e7ebf0; border-radius: 15px; padding: 1rem 1.1rem;
  background: white; min-height: 105px;
}
.panel h3 { font-size: 1.03rem; margin: .2rem 0 .45rem 0; color: #182230; }
.panel p { color: #667085; margin: 0; font-size: .9rem; }
.pill { display:inline-block; padding:.22rem .55rem; border-radius:999px;
  background:#edf2ff; color:#304fc4; font-size:.76rem; font-weight:650; }
.small-muted { color:#667085; font-size:.86rem; }
div[data-testid="stMetric"] {
  border: 1px solid #e7ebf0; border-radius: 14px; padding: .8rem 1rem;
  background: #fff;
}
div[data-testid="stMetricLabel"] { color: #667085; }
hr { border-color: #e7ebf0; }
.stButton button { border-radius: 9px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

profile = get_profile()

def hero(title, subtitle, eyebrow="CAREER MENTOR"):
    st.markdown(
        f'<div class="hero"><div class="eyebrow">{eyebrow}</div>'
        f'<h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True
    )

def panel(title, body, tag=None):
    tag_html = f'<span class="pill">{tag}</span>' if tag else ""
    st.markdown(
        f'<div class="panel">{tag_html}<h3>{title}</h3><p>{body}</p></div>',
        unsafe_allow_html=True
    )

def readiness(profile):
    role = profile.get("target_role", "Data Scientist")
    required = ROLE_DATA.get(role, ROLE_DATA["Data Scientist"])["skills"]
    skills = set(profile.get("skills", []))
    if not required:
        return 0, []
    matched = [s for s in required if s.lower() in {x.lower() for x in skills}]
    missing = [s for s in required if s.lower() not in {x.lower() for x in skills}]
    return round(100 * len(matched) / len(required)), missing

def skill_multiselect_key():
    return "profile_skills_widget"

with st.sidebar:
    st.markdown("## 🧭 Career Mentor")
    st.caption("Your personal career operating system")
    st.divider()
    page = st.radio(
        "WORKSPACE",
        ["Dashboard", "Learning Sources", "Profile Settings", "Personal Growth"],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown("**Your current target**")
    st.write(profile.get("target_role", "Data Scientist"))
    st.caption(f"{profile.get('stage', 'Undergraduate')} · {profile.get('weekly_hours', 6)} hrs/week")
    st.divider()
    st.caption("Prototype v1.0 · Profile-aware recommendations")

# ---------- Dashboard ----------
if page == "Dashboard":
    hero(
        f"Welcome back, {profile.get('name') or 'Future Professional'}",
        "A focused workspace for skills, projects, learning, and career progress.",
        "YOUR CAREER, WITH DIRECTION"
    )
    role = profile.get("target_role", "Data Scientist")
    readiness_pct, missing = readiness(profile)
    goals = get_goals()
    completed = sum(1 for g in goals if g["completed"])
    total = len(goals)
    active_goals = total - completed
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Target role", role)
    c2.metric("Skill coverage", f"{readiness_pct}%")
    c3.metric("Skills to build", len(missing))
    c4.metric("Active growth goals", active_goals)
    st.write("")
    left, right = st.columns([1.35, 1])
    with left:
        st.subheader("Your next best moves")
        recommendations = recommend(profile)
        for i, item in enumerate(recommendations["actions"], 1):
            st.markdown(f"**{i}. {item['title']}**")
            st.write(item["description"])
            st.caption(f"Focus: {item['focus']} · Effort: {item['effort']}")
            if i < len(recommendations["actions"]):
                st.divider()
    with right:
        st.subheader("Role readiness")
        st.progress(readiness_pct / 100)
        st.write(f"**{readiness_pct}% skill coverage** against a starter skill profile for {role}.")
        if missing:
            st.markdown("**Priority skills to develop**")
            for skill in missing[:5]:
                st.markdown(f"- {skill}")
        else:
            st.success("You have selected all starter skills for this role. Validate them with projects and assessments.")
        st.caption("This is a heuristic indicator, not a hiring probability or formal assessment.")
    st.divider()
    st.subheader("Recommended starter projects")
    projects = recommendations["projects"]
    cols = st.columns(len(projects))
    for col, proj in zip(cols, projects):
        with col:
            panel(proj["title"], proj["description"], proj["level"])
            st.caption("Evidence to publish: " + proj["evidence"])
    st.divider()
    st.subheader("Weekly momentum")
    if total:
        st.progress(completed / total)
        st.write(f"{completed} of {total} growth goals completed.")
    else:
        st.info("No growth goals yet. Open **Personal Growth** to add your first goal.")
    st.caption("Recommendations are generated from your saved profile and the built-in career knowledge base. No external AI API is required.")

# ---------- Learning Sources ----------
elif page == "Learning Sources":
    hero("Learning Sources", "A curated launchpad for building the skills your target role requires.")
    role = profile.get("target_role", "Data Scientist")
    _, missing = readiness(profile)
    st.markdown(f"**Current target:** {role}")
    search = st.text_input("Search resources", placeholder="Try Python, SQL, portfolio, interview…")
    filter_mode = st.selectbox("Show resources", ["All resources", "Priority skill gaps", "Free resources"])
    resource_rows = []
    for r in RESOURCES:
        if filter_mode == "Priority skill gaps" and not any(m.lower() in r["skills"].lower() for m in missing):
            continue
        if filter_mode == "Free resources" and not r["free"]:
            continue
        haystack = " ".join([r["title"], r["provider"], r["skills"], r["type"], r["description"]]).lower()
        if search and search.lower() not in haystack:
            continue
        resource_rows.append(r)
    if not resource_rows:
        st.info("No resources match those filters. Try another search or select All resources.")
    for r in resource_rows:
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"### {r['title']}")
                st.caption(f"{r['provider']} · {r['type']} · Skills: {r['skills']}")
                st.write(r["description"])
                st.caption("Free to access" if r["free"] else "Check provider pricing")
            with col2:
                st.link_button("Open resource ↗", r["url"], use_container_width=True)
    st.divider()
    st.subheader("Suggested learning sequence")
    st.markdown("1. Learn the fundamentals → 2. Practise with small exercises → 3. Build one portfolio project → 4. Document results on GitHub → 5. Practise explaining trade-offs in an interview.")

# ---------- Profile Settings ----------
elif page == "Profile Settings":
    hero("Profile Settings", "Keep your career mentor aligned with your goals, strengths, and available time.")
    st.caption("Your profile is used to tailor skill-gap suggestions, starter projects, and learning resources.")
    all_skills = sorted({s for role_data in ROLE_DATA.values() for s in role_data["skills"]})
    current_skills = profile.get("skills", [])
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your name", value=profile.get("name", ""), max_chars=80)
            target_role = st.selectbox(
                "Target role", list(ROLE_DATA.keys()),
                index=list(ROLE_DATA.keys()).index(profile.get("target_role", "Data Scientist"))
                if profile.get("target_role", "Data Scientist") in ROLE_DATA else 0
            )
            stage = st.selectbox(
                "Current stage",
                ["Undergraduate", "Recent graduate", "Early career", "Career switcher"],
                index=["Undergraduate", "Recent graduate", "Early career", "Career switcher"].index(profile.get("stage", "Undergraduate"))
                if profile.get("stage", "Undergraduate") in ["Undergraduate", "Recent graduate", "Early career", "Career switcher"] else 0
            )
        with col2:
            weekly_hours = st.slider("Hours available for learning each week", 1, 30, int(profile.get("weekly_hours", 6)))
            interests = st.text_input("Interests (comma separated)", value=profile.get("interests", "AI, Python, projects"))
            career_goal = st.text_area("Career goal", value=profile.get("career_goal", "Build a strong portfolio and prepare for placements."), height=100)
        skills = st.multiselect("Skills you currently have", all_skills, default=[s for s in current_skills if s in all_skills], help="Select only skills you can explain or demonstrate.")
        submitted = st.form_submit_button("Save profile", type="primary")
    if submitted:
        save_profile({
            "name": name.strip(),
            "target_role": target_role,
            "stage": stage,
            "weekly_hours": weekly_hours,
            "interests": interests.strip(),
            "career_goal": career_goal.strip(),
            "skills": skills,
        })
        st.success("Profile saved. Your dashboard recommendations have been refreshed.")
        st.rerun()
    st.divider()
    st.subheader("How personalization works")
    st.markdown("""
    - The target role selects a starter skill framework.
    - Your selected skills are compared with that framework to identify gaps.
    - Your available weekly hours inform the suggested learning workload.
    - Interests and goals provide context for the next-step recommendations.
    """)
    st.warning("Profile information is stored in the app's local SQLite database. On free hosted platforms, local file persistence may not be guaranteed. Avoid entering sensitive personal data.")

# ---------- Personal Growth ----------
elif page == "Personal Growth":
    hero("Personal Growth", "Turn career intentions into weekly actions you can complete and review.")
    goals = get_goals()
    done = sum(1 for g in goals if g["completed"])
    total = len(goals)
    col1, col2, col3 = st.columns(3)
    col1.metric("Goals created", total)
    col2.metric("Completed", done)
    col3.metric("Completion rate", f"{round(done / total * 100) if total else 0}%")
    st.subheader("Create a growth goal")
    with st.form("goal_form", clear_on_submit=True):
        title = st.text_input("Goal", placeholder="e.g., Complete SQL joins practice")
        category = st.selectbox("Category", ["Technical skill", "Portfolio project", "Interview preparation", "Communication", "Career planning"])
        due_date = st.date_input("Target date", value=date.today() + timedelta(days=7), min_value=date.today())
        notes = st.text_input("Definition of done", placeholder="e.g., Solve 10 exercises and save notes")
        add_submitted = st.form_submit_button("Add goal", type="primary")
    if add_submitted:
        if title.strip():
            add_goal(title.strip(), category, due_date.isoformat(), notes.strip())
            st.success("Goal added.")
            st.rerun()
        else:
            st.error("Enter a goal title.")
    st.divider()
    st.subheader("Your growth plan")
    goals = get_goals()
    if not goals:
        st.info("Create your first goal above. Keep it specific, measurable, and achievable.")
    for g in goals:
        with st.container(border=True):
            c1, c2, c3 = st.columns([5, 1.5, 1])
            with c1:
                st.markdown(("✅ " if g["completed"] else "◻️ ") + f"**{g['title']}**")
                st.caption(f"{g['category']} · Due {g['due_date'] or 'not set'}")
                if g["notes"]:
                    st.write(g["notes"])
            with c2:
                label = "Mark active" if g["completed"] else "Complete"
                if st.button(label, key=f"toggle_{g['id']}"):
                    toggle_goal(g["id"], not g["completed"])
                    st.rerun()
            with c3:
                if st.button("Delete", key=f"delete_{g['id']}"):
                    delete_goal(g["id"])
                    st.rerun()
    st.divider()
    st.subheader("Weekly reflection")
    with st.form("reflection_form", clear_on_submit=True):
        wins = st.text_area("What went well?", placeholder="Record one concrete win.")
        blockers = st.text_area("What blocked progress?", placeholder="Identify a blocker without judgement.")
        next_step = st.text_input("One next step", placeholder="What will you do next?")
        reflection_submit = st.form_submit_button("Save reflection")
    if reflection_submit:
        if wins.strip() or blockers.strip() or next_step.strip():
            add_reflection(wins.strip(), blockers.strip(), next_step.strip())
            st.success("Reflection saved.")
            st.rerun()
        else:
            st.error("Add at least one reflection detail.")
    reflections = get_reflections()
    if reflections:
        st.subheader("Recent reflections")
        for r in reflections[:5]:
            with st.container(border=True):
                st.caption(r["created_at"])
                if r["wins"]:
                    st.markdown(f"**Win:** {r['wins']}")
                if r["blockers"]:
                    st.markdown(f"**Blocker:** {r['blockers']}")
                if r["next_step"]:
                    st.markdown(f"**Next step:** {r['next_step']}")

st.sidebar.divider()
st.sidebar.caption("Built for learning and career planning. Recommendations are guidance, not guarantees of employment.")
