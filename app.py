# ============================================================
# PS-09 AI MEETING ASSISTANT AGENT
# Clean Single-File Streamlit Application
# ============================================================

import os
import json
import re
import time
import streamlit as st


# ============================================================
# GEMINI IMPORT
# ============================================================

try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Meeting Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(37, 99, 235, 0.16),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(124, 58, 237, 0.14),
                transparent 30%
            ),
            #070b14;
        color: #f8fafc;
    }

    .main .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ---------- TEXT ---------- */

    h1, h2, h3, h4, p, label {
        color: #f8fafc !important;
    }

    .subtitle {
        color: #94a3b8 !important;
        font-size: 17px;
        text-align: center;
        margin-bottom: 30px;
    }

    .small-muted {
        color: #94a3b8;
        font-size: 14px;
    }

    /* ---------- HEADER ---------- */

    .hero {
        text-align: center;
        padding: 25px 10px 15px 10px;
    }

    .hero-title {
        font-size: 46px;
        font-weight: 800;
        background: linear-gradient(
            90deg,
            #60a5fa,
            #a78bfa
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 18px;
    }

    /* ---------- GLASS CARDS ---------- */

    .glass-card {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow:
            0 10px 35px rgba(0, 0, 0, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(14px);
    }

    /* ---------- STAT CARDS ---------- */

    .stat-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(96, 165, 250, 0.15);
        border-radius: 18px;
        padding: 20px;
        text-align: center;
        min-height: 125px;
    }

    .stat-number {
        font-size: 32px;
        font-weight: 800;
        color: #60a5fa;
    }

    .stat-label {
        color: #94a3b8;
        font-size: 14px;
        margin-top: 5px;
    }

    /* ---------- ACTION CARDS ---------- */

    .action-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 14px;
    }

    .priority-high {
        color: #f87171;
        font-weight: 700;
    }

    .priority-medium {
        color: #fbbf24;
        font-weight: 700;
    }

    .priority-low {
        color: #4ade80;
        font-weight: 700;
    }

    /* ---------- DEMO BADGE ---------- */

    .demo-badge {
        display: inline-block;
        background: rgba(124, 58, 237, 0.15);
        border: 1px solid rgba(167, 139, 250, 0.3);
        color: #c4b5fd;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 13px;
        margin-bottom: 15px;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: #090e19;
        border-right: 1px solid rgba(148, 163, 184, 0.12);
    }

    /* ---------- BUTTONS ---------- */

    .stButton > button {
        border-radius: 12px;
        border: 1px solid rgba(96, 165, 250, 0.25);
        font-weight: 600;
    }

    /* ---------- INPUTS ---------- */

    textarea,
    input {
        border-radius: 12px !important;
    }

    /* ---------- MOBILE ---------- */

    @media (max-width: 768px) {

        .hero-title {
            font-size: 34px;
        }

        .hero-subtitle {
            font-size: 15px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# API KEY CONFIGURATION
# ============================================================

def get_api_key():
    """
    Gets Gemini API key from Streamlit Secrets first.
    Falls back to environment variable.
    """

    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    return os.getenv("GEMINI_API_KEY")


# ============================================================
# DEMO MEETING DATA
# ============================================================

DEMO_TRANSCRIPT = """
Rahul: Good morning everyone. Let's start today's project meeting.
Our main goal is to discuss the launch of our new e-commerce website.

Priya: The frontend is almost complete. The homepage, product page,
and checkout page are ready.

Amit: I have tested most of the website, but the payment gateway
still needs additional testing.

Rahul: Amit, can you complete the payment testing by Friday?

Amit: Yes, I can complete it by Friday and share the testing report.

Priya: We also need to finalize the product descriptions and
marketing content before the launch.

Rahul: Priya, can you complete the final marketing content by Thursday?

Priya: Yes, I'll complete it by Thursday.

Amit: There is also a small issue with the mobile checkout page.
I will fix that while testing the payment system.

Rahul: Good. Let's make sure everything is completed before the weekend.

Priya: Should we target Monday for the official launch?

Rahul: Yes, let's target Monday as the launch date.

Amit: I'll make sure the payment system and mobile checkout
are tested before then.

Rahul: We also need to review the homepage performance.

Priya: The homepage currently loads well, but we can optimize
some large images later.

Amit: I noticed one irrelevant issue with an old test account.
It does not affect the current release.

Rahul: Okay, let's ignore that for now.

Rahul: So the final important tasks are payment testing,
mobile checkout fixing, marketing content, and the final review.
We'll review everything on Friday.

Priya: Agreed.

Amit: Agreed.

Rahul: Great. Meeting closed.
"""


# ============================================================
# DEMO ANALYSIS
# ============================================================

def demo_analysis():
    return {
        "summary": (
            "The team reviewed the progress of the e-commerce website "
            "and discussed the remaining work before launch. The frontend "
            "is nearly complete, while payment testing and a mobile "
            "checkout issue still require attention. Marketing content "
            "also needs to be finalized. The team agreed to target Monday "
            "for the official launch and review the remaining work on Friday."
        ),

        "meeting_duration": "Not specified",

        "key_points": [
            "The homepage, product page, and checkout page are almost complete.",
            "Payment gateway testing is still required.",
            "The mobile checkout page has a small issue.",
            "Marketing content and product descriptions need to be finalized.",
            "The team plans to review the remaining work on Friday.",
            "Homepage performance is currently acceptable, with possible future image optimization."
        ],

        "decisions": [
            "The team agreed to target Monday for the official website launch.",
            "The remaining critical work will be reviewed on Friday.",
            "The old test-account issue will not be addressed in the current release."
        ],

        "action_items": [
            {
                "task": "Complete payment gateway testing",
                "person": "Amit",
                "deadline": "Friday",
                "priority": "High"
            },
            {
                "task": "Share the payment testing report",
                "person": "Amit",
                "deadline": "Friday",
                "priority": "Medium"
            },
            {
                "task": "Finalize product descriptions and marketing content",
                "person": "Priya",
                "deadline": "Thursday",
                "priority": "High"
            },
            {
                "task": "Fix the mobile checkout issue",
                "person": "Amit",
                "deadline": "Before Monday launch",
                "priority": "High"
            }
        ],

        "risks": [
            "Payment testing must be completed before launch.",
            "The mobile checkout issue could affect the launch if it remains unresolved."
        ]
    }


# ============================================================
# SUMMARY MODE INSTRUCTIONS
# ============================================================

def get_mode_instruction(mode):

    instructions = {

        "Quick": (
            "Keep the summary very concise. Focus only on the most "
            "important decisions and actions."
        ),

        "Standard": (
            "Provide a balanced summary with the major discussion "
            "points, decisions, and actions."
        ),

        "Simple": (
            "Use very simple and easy-to-understand language. "
            "Avoid unnecessary technical words."
        ),

        "Professional": (
            "Write a polished professional meeting summary suitable "
            "for managers, project documentation, and business records."
        )
    }

    return instructions.get(mode, instructions["Standard"])


# ============================================================
# GEMINI ANALYSIS
# ============================================================

def analyze_with_gemini(transcript, summary_mode):

    api_key = get_api_key()

    if not api_key:
        return None, "Gemini API key is not configured."

    if not GEMINI_AVAILABLE:
        return None, "The google-genai package is not installed."

    prompt = f"""
You are an AI Meeting Assistant Agent.

Analyze the meeting transcript below.

Your job is to extract only useful information from the meeting.

Summary style:
{get_mode_instruction(summary_mode)}

Return ONLY valid JSON.

Use EXACTLY this structure:

{{
    "summary": "Detailed meeting summary",
    "meeting_duration": "Duration if explicitly available, otherwise Not specified",
    "key_points": [
        "Important point"
    ],
    "decisions": [
        "Decision made"
    ],
    "action_items": [
        {{
            "task": "Specific task",
            "person": "Responsible person or Not specified",
            "deadline": "Deadline or Not specified",
            "priority": "High, Medium, or Low"
        }}
    ],
    "risks": [
        "Important risk or concern"
    ]
}}

STRICT RULES:

1. Use ONLY information contained in the transcript.
2. Never invent names, deadlines, decisions, or tasks.
3. Do not treat casual discussion as a decision.
4. Identify explicit decisions.
5. Identify explicit action items.
6. Identify the person responsible when available.
7. Identify deadlines when available.
8. Assign priority based on the importance expressed in the meeting.
9. If priority cannot reasonably be determined, use "Medium".
10. Ignore irrelevant information unless it affects the project.
11. Do not include filler.
12. If there are no risks, return an empty list.
13. If duration is not provided, use "Not specified".
14. Return valid JSON only.

MEETING TRANSCRIPT:

{transcript}
"""

    try:

       client = genai.Client(api_key=api_key)

for attempt in range(3):

    try:

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        if not response or not response.text:
            return None, "Gemini returned an empty response."

        result = response.text.strip()

        break

    except Exception as error:

        error_message = str(error)

        if (
            "503" in error_message
            or "UNAVAILABLE" in error_message
        ):

            if attempt < 2:
                time.sleep(3 * (attempt + 1))
                continue

            return None, (
                "Gemini is temporarily overloaded. "
                "Please try again after a short wait."
            )

        return None, f"Gemini API error: {error_message}"

        # Remove Markdown code fences if Gemini adds them
        if result.startswith("```json"):
            result = result[7:]

        elif result.startswith("```"):
            result = result[3:]

        if result.endswith("```"):
            result = result[:-3]

        result = result.strip()

        data = json.loads(result)

        # Make sure required fields exist
        data.setdefault("summary", "No summary available.")
        data.setdefault("meeting_duration", "Not specified")
        data.setdefault("key_points", [])
        data.setdefault("decisions", [])
        data.setdefault("action_items", [])
        data.setdefault("risks", [])

        return data, None

    except json.JSONDecodeError:
        return None, "Gemini returned an invalid JSON response."

    except Exception as error:
        return None, str(error)


# ============================================================
# FILE READING
# ============================================================

def read_uploaded_file(uploaded_file):

    if uploaded_file is None:
        return ""

    file_name = uploaded_file.name.lower()

    try:

        # TXT / Markdown
        if file_name.endswith(".txt") or file_name.endswith(".md"):

            return uploaded_file.read().decode(
                "utf-8",
                errors="ignore"
            )

        # CSV
        if file_name.endswith(".csv"):

            return uploaded_file.read().decode(
                "utf-8",
                errors="ignore"
            )

        # PDF
        if file_name.endswith(".pdf"):

            from pypdf import PdfReader

            reader = PdfReader(uploaded_file)

            pages = []

            for page in reader.pages:
                text = page.extract_text()

                if text:
                    pages.append(text)

            return "\n".join(pages)

        # DOCX
        if file_name.endswith(".docx"):

            from docx import Document

            document = Document(uploaded_file)

            paragraphs = []

            for paragraph in document.paragraphs:
                if paragraph.text.strip():
                    paragraphs.append(paragraph.text)

            return "\n".join(paragraphs)

        return ""

    except Exception as error:

        raise ValueError(
            f"Could not read the uploaded file: {error}"
        )


# ============================================================
# TEXT HELPERS
# ============================================================

def clean_text(text):

    if not text:
        return ""

    text = text.replace("\x00", "")

    return text.strip()


def priority_class(priority):

    priority = str(priority).lower()

    if priority == "high":
        return "priority-high"

    if priority == "low":
        return "priority-low"

    return "priority-medium"


# ============================================================
# DOWNLOAD REPORT
# ============================================================

def create_report(data):

    report = []

    report.append("AI MEETING ASSISTANT")
    report.append("=" * 60)
    report.append("")

    report.append("SUMMARY")
    report.append("-" * 60)
    report.append(data.get("summary", "Not available"))
    report.append("")

    report.append("MEETING DURATION")
    report.append("-" * 60)
    report.append(data.get("meeting_duration", "Not specified"))
    report.append("")

    report.append("KEY POINTS")
    report.append("-" * 60)

    for point in data.get("key_points", []):
        report.append(f"- {point}")

    report.append("")

    report.append("DECISIONS")
    report.append("-" * 60)

    for decision in data.get("decisions", []):
        report.append(f"- {decision}")

    report.append("")

    report.append("ACTION ITEMS")
    report.append("-" * 60)

    for index, action in enumerate(
        data.get("action_items", []),
        start=1
    ):

        report.append(f"{index}. {action.get('task', 'Not specified')}")
        report.append(
            f"   Person: {action.get('person', 'Not specified')}"
        )
        report.append(
            f"   Deadline: {action.get('deadline', 'Not specified')}"
        )
        report.append(
            f"   Priority: {action.get('priority', 'Medium')}"
        )
        report.append("")

    report.append("RISKS")
    report.append("-" * 60)

    for risk in data.get("risks", []):
        report.append(f"- {risk}")

    return "\n".join(report)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">
            🤖 AI Meeting Assistant
        </div>

       <p class="hero-subtitle">
            Turn long meetings into clear, actionable insights.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚙️ Controls")

    st.markdown("### Summary Mode")

    summary_mode = st.selectbox(
        "Choose output style",
        [
            "Quick",
            "Standard",
            "Simple",
            "Professional"
        ],
        index=1
    )

    st.divider()

    st.markdown("### Features")

    st.write("📋 AI Summary")
    st.write("🎯 Key Decisions")
    st.write("🔑 Key Points")
    st.write("✅ Action Items")
    st.write("👤 Responsible Person")
    st.write("📅 Deadlines")
    st.write("🚦 Priority Detection")
    st.write("⚠️ Risk Detection")
    st.write("💬 AI Q&A")

    st.divider()

    api_key = get_api_key()

    if api_key:
        st.success("Gemini API configured")
    else:
        st.warning("Gemini API not configured")

    st.divider()

    if st.button(
        "🧪 Load Demo Meeting",
        use_container_width=True
    ):

        st.session_state["transcript"] = DEMO_TRANSCRIPT
        st.session_state["demo_loaded"] = True

        st.rerun()


# ============================================================
# UPLOAD SECTION
# ============================================================

st.markdown(
    '<div class="glass-card">',
    unsafe_allow_html=True
)

st.markdown("## 📂 Upload Your Meeting")

st.markdown(
    """
    Upload a meeting transcript or paste the conversation manually.
    Supported files: TXT, MD, CSV, PDF and DOCX.
    """
)

uploaded_file = st.file_uploader(
    "Choose a meeting file",
    type=["txt", "md", "csv", "pdf", "docx"],
    label_visibility="collapsed"
)

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# TRANSCRIPT INPUT
# ============================================================

if "transcript" not in st.session_state:
    st.session_state["transcript"] = ""

if "demo_loaded" not in st.session_state:
    st.session_state["demo_loaded"] = False


if uploaded_file is not None:

    try:

        uploaded_text = read_uploaded_file(uploaded_file)

        if uploaded_text:

            st.session_state["transcript"] = uploaded_text

            st.success(
                f"Loaded: {uploaded_file.name}"
            )

        else:

            st.error(
                "The uploaded file does not contain readable text."
            )

    except Exception as error:

        st.error(str(error))


st.markdown(
    '<div class="glass-card">',
    unsafe_allow_html=True
)

st.markdown("## 📝 Meeting Transcript")

transcript = st.text_area(
    "Meeting conversation",
    value=st.session_state["transcript"],
    height=320,
    placeholder=(
        "Paste your meeting transcript here...\n\n"
        "Example:\n"
        "Rahul: We need to finish the project.\n"
        "Priya: I will complete the frontend by Friday.\n"
        "Amit: I will test the payment system.\n"
        "Rahul: Let's review everything on Monday."
    ),
    label_visibility="collapsed"
)

st.session_state["transcript"] = transcript

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze_button = st.button(
    "✨ Generate AI Summary",
    type="primary",
    use_container_width=True
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze_button:

    transcript = clean_text(transcript)

    if not transcript:

        st.error(
            "Please upload a meeting file or enter a transcript first."
        )

        st.stop()

    # --------------------------------------------
    # Processing
    # --------------------------------------------

    progress = st.progress(0)

    status = st.status(
        "🤖 AI is analyzing the meeting...",
        expanded=True
    )

    try:

        status.write("📖 Reading meeting transcript...")
        progress.progress(15)

        status.write("🔍 Identifying important topics...")
        progress.progress(30)

        status.write("🎯 Extracting key decisions...")
        progress.progress(45)

        status.write("✅ Finding action items...")
        progress.progress(60)

        status.write("📅 Detecting people and deadlines...")
        progress.progress(75)

        status.write("📝 Preparing concise summary...")
        progress.progress(90)

        # ------------------------------------------------
        # Demo mode only when explicitly loaded
        # ------------------------------------------------

        if st.session_state.get("demo_loaded", False):

            data = demo_analysis()
            error = None

            st.session_state["demo_loaded"] = False

        else:

            data, error = analyze_with_gemini(
                transcript,
                summary_mode
            )

        if error:

            status.update(
                label="❌ Analysis failed",
                state="error"
            )

            progress.progress(100)

            st.error(
                f"AI analysis failed: {error}"
            )

            st.stop()

        progress.progress(100)

        status.update(
            label="✅ Analysis completed",
            state="complete"
        )

        st.session_state["analysis"] = data
        st.session_state["last_transcript"] = transcript

    except Exception as error:

        status.update(
            label="❌ Unexpected error",
            state="error"
        )

        st.error(
            f"Unexpected error: {error}"
        )

        st.stop()


# ============================================================
# RESULTS
# ============================================================

if "analysis" in st.session_state:

    data = st.session_state["analysis"]

    if st.session_state.get("demo_loaded", False):

        st.markdown(
            '<div class="demo-badge">🧪 DEMO DATA</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ========================================================
    # STATISTICS
    # ========================================================

    st.markdown("## 📊 Meeting Statistics")

    key_points_count = len(
        data.get("key_points", [])
    )

    decisions_count = len(
        data.get("decisions", [])
    )

    actions_count = len(
        data.get("action_items", [])
    )

    duration = data.get(
        "meeting_duration",
        "Not specified"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-number">
                    {duration}
                </div>
                <div class="stat-label">
                    Meeting Duration
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-number">
                    {key_points_count}
                </div>
                <div class="stat-label">
                    Key Points
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-number">
                    {actions_count}
                </div>
                <div class="stat-label">
                    Action Items
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-number">
                    {decisions_count}
                </div>
                <div class="stat-label">
                    Decisions
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("")


    # ========================================================
    # MAIN RESULT TABS
    # ========================================================

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📋 AI Summary",
            "🔑 Key Points",
            "🎯 Decisions",
            "✅ Action Items",
            "⚠️ Risks"
        ]
    )


    # ========================================================
    # SUMMARY
    # ========================================================

    with tab1:

        st.markdown("## AI Meeting Summary")

        st.markdown(
            f"""
            <div class="glass-card">
                {data.get("summary", "No summary available.")}
            </div>
            """,
            unsafe_allow_html=True
        )

        report = create_report(data)

        col1, col2 = st.columns(2)

        with col1:

            st.download_button(
                "⬇️ Download Meeting Report",
                data=report,
                file_name="meeting_report.txt",
                mime="text/plain",
                use_container_width=True
            )

        with col2:

            st.download_button(
                "⬇️ Download Summary",
                data=data.get(
                    "summary",
                    "No summary available."
                ),
                file_name="meeting_summary.txt",
                mime="text/plain",
                use_container_width=True
            )


    # ========================================================
    # KEY POINTS
    # ========================================================

    with tab2:

        st.markdown("## 🔑 Key Points")

        points = data.get(
            "key_points",
            []
        )

        if points:

            for point in points:

                st.markdown(
                    f"""
                    <div class="glass-card">
                        🔹 {point}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.info("No key points were identified.")


    # ========================================================
    # DECISIONS
    # ========================================================

    with tab3:

        st.markdown("## 🎯 Decisions Made")

        decisions = data.get(
            "decisions",
            []
        )

        if decisions:

            for decision in decisions:

                st.markdown(
                    f"""
                    <div class="glass-card">
                        ☑️ {decision}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.info(
                "No explicit decisions were identified."
            )


    # ========================================================
    # ACTION ITEMS
    # ========================================================

    with tab4:

        st.markdown("## ✅ Action Items")

        actions = data.get(
            "action_items",
            []
        )

        if actions:

            for index, action in enumerate(
                actions,
                start=1
            ):

                task = action.get(
                    "task",
                    "Not specified"
                )

                person = action.get(
                    "person",
                    "Not specified"
                )

                deadline = action.get(
                    "deadline",
                    "Not specified"
                )

                priority = action.get(
                    "priority",
                    "Medium"
                )

                priority_css = priority_class(
                    priority
                )

                st.markdown(
    f"""<div class="action-card">
<h3>Action {index}</h3>

<p>📌 <strong>Task:</strong> {task}</p>

<p>👤 <strong>Responsible:</strong> {person}</p>

<p>📅 <strong>Deadline:</strong> {deadline}</p>

<p>🚦 <strong>Priority:</strong>
<span class="{priority_css}">{priority}</span>
</p>

</div>""",
    unsafe_allow_html=True
)

        else:

            st.info(
                "No action items were identified."
            )


    # ========================================================
    # RISKS
    # ========================================================

    with tab5:

        st.markdown("## ⚠️ Risks & Concerns")

        risks = data.get(
            "risks",
            []
        )

        if risks:

            for risk in risks:

                st.markdown(
                    f"""
                    <div class="glass-card">
                        ⚠️ {risk}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.success(
                "No major risks were identified."
            )


    # ========================================================
    # AI Q&A
    # ========================================================

    st.markdown("---")

    st.markdown("## 💬 Ask AI About This Meeting")

    question = st.text_input(
        "Ask a question",
        placeholder=(
            "Example: Who is responsible for payment testing?"
        )
    )

    if st.button(
        "Ask AI",
        use_container_width=True
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            api_key = get_api_key()

            if not api_key:

                st.error(
                    "Gemini API key is not configured."
                )

            elif not GEMINI_AVAILABLE:

                st.error(
                    "google-genai package is not installed."
                )

            else:

                qa_prompt = f"""
You are answering questions about a meeting.

Use ONLY the meeting transcript and extracted analysis below.

Do not invent information.

If the answer is not present in the meeting,
say exactly:

"That information is not available in the meeting."

MEETING TRANSCRIPT:
{st.session_state.get("last_transcript", "")}

EXTRACTED ANALYSIS:
{json.dumps(data, indent=2)}

USER QUESTION:
{question}

Answer clearly and directly.
"""

                try:

                    client = genai.Client(
                        api_key=api_key
                    )

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=qa_prompt
                    )

                    answer = response.text.strip()

                    st.markdown(
                        f"""
                        <div class="glass-card">
                            <strong>🤖 AI Answer</strong>
                            <br><br>
                            {answer}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                except Exception as error:

                    st.error(
                        f"Q&A failed: {error}"
                    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#64748b;
        padding:20px;
        font-size:13px;
    ">
        PS-09 • AI Meeting Assistant Agent
        <br>
        Powered by Streamlit + Google Gemini
    </div>
    """,
    unsafe_allow_html=True
)
