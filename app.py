from pathlib import Path

code = r'''# ============================================================
# PS-09 AI MEETING ASSISTANT AGENT
# Clean single-file Streamlit application
# ============================================================

import io
import json
import streamlit as st

# ============================================================
# GEMINI CONFIGURATION
# ============================================================
# Paste your Gemini API key INSIDE the quotes.
# Example:
# GEMINI_API_KEY = "YOUR_API_KEY_HERE"
#
# IMPORTANT:
# Do not upload a real API key to GitHub.
GEMINI_API_KEY = "PASTE_YOUR_API_KEY_HERE"

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
    initial_sidebar_state="collapsed"
)


# ============================================================
# PREMIUM DARK GLASS UI
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: Inter, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 8% 0%, rgba(82,91,210,.22), transparent 30%),
        radial-gradient(circle at 92% 5%, rgba(38,111,255,.14), transparent 28%),
        linear-gradient(135deg,#03050a,#080d18 50%,#03050a);
    color: #eef2ff;
}

.block-container {
    max-width: 1180px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

.hero {
    text-align: center;
    padding: 28px 18px 34px;
}

.hero-icon {
    font-size: 52px;
    filter: drop-shadow(0 0 20px rgba(100,125,255,.6));
}

.hero-title {
    font-size: clamp(36px,5vw,56px);
    font-weight: 800;
    letter-spacing: -2px;
    background: linear-gradient(90deg,#fff,#c8d1ff,#8da6ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #9ba7c0;
    font-size: 16px;
    max-width: 700px;
    margin: auto;
}

.glass,
.content-card,
.stat-card {
    background: rgba(13,18,32,.68);
    border: 1px solid rgba(148,163,184,.14);
    box-shadow:
        0 18px 50px rgba(0,0,0,.25),
        inset 0 1px 0 rgba(255,255,255,.035);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}

.glass {
    border-radius: 22px;
    padding: 28px;
}

.upload-card {
    text-align: center;
    padding: 36px 30px;
    margin-bottom: 18px;
}

.content-card {
    border-radius: 20px;
    padding: 24px;
    margin-top: 18px;
}

.stat-card {
    min-height: 112px;
    border-radius: 18px;
    padding: 19px;
}

.stat-label {
    color: #8e9ab5;
    font-size: 13px;
    margin-bottom: 8px;
}

.stat-value {
    font-size: 28px;
    font-weight: 800;
    color: #f5f7ff;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #f5f7ff;
    margin-bottom: 6px;
}

.section-subtitle {
    color: #8e9ab5;
    font-size: 14px;
    margin-bottom: 18px;
}

.action-item {
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(148,163,184,.11);
    border-radius: 15px;
    padding: 17px;
    margin: 10px 0;
}

.demo-banner {
    border-radius: 14px;
    padding: 12px 16px;
    margin: 12px 0 18px;
    background: rgba(59,130,246,.08);
    border: 1px solid rgba(96,165,250,.18);
    color: #b9ccff;
}

.answer-box {
    border-radius: 15px;
    padding: 18px;
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(148,163,184,.12);
    margin-top: 12px;
}

.footer {
    text-align: center;
    color: #69758f;
    padding: 28px 0 5px;
    font-size: 12px;
}

div[data-testid="stFileUploader"] {
    background: rgba(255,255,255,.025);
    border: 1px dashed rgba(132,150,255,.28);
    border-radius: 16px;
    padding: 10px;
}

.stButton > button,
.stDownloadButton > button {
    border-radius: 12px !important;
    border: 1px solid rgba(125,145,255,.25) !important;
    background: linear-gradient(135deg,#3447a8,#5368d8) !important;
    color: #fff !important;
    font-weight: 650 !important;
    min-height: 44px;
}

.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div {
    background: rgba(8,12,23,.78) !important;
    color: #edf2ff !important;
    border-color: rgba(148,163,184,.18) !important;
    border-radius: 12px !important;
}

@media(max-width:700px) {
    .block-container {
        padding: 1rem;
    }

    .glass,
    .content-card,
    .upload-card {
        padding: 18px;
        border-radius: 16px;
    }
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# DEMO MEETING DATA
# ============================================================
DEMO_TRANSCRIPT = """
DEMO DATA — Fictional NovaCart Project Meeting

Rahul (Project Manager): Good morning everyone. Today's meeting is
about the NovaCart e-commerce platform release. We need to review
development status, the release date, payment testing, mobile
performance, marketing content, monitoring, and customer support.

Priya (Frontend Lead): The homepage and product pages are complete.
The redesigned checkout flow is ready, and the smaller-screen
navigation issue has been fixed.

Amit (Backend Engineer): The order service is stable. The payment
gateway works in staging, but we still need end-to-end testing for
successful payments, failed payments, and refunds.

Rahul: What is the testing timeline?

Amit: I can complete the payment test cycle by Thursday afternoon.
I will prepare a test report with failed cases and their status.

Priya: There is one remaining mobile issue. On some Android devices,
the checkout confirmation button responds slowly. It is not blocking
desktop release, but I recommend fixing it before public launch.

Rahul: Agreed. Treat the mobile checkout issue as high priority and
have it fixed by Friday morning.

Priya: Understood. I will coordinate with Amit for another test after
the fix.

Neha (Marketing): The launch campaign draft is ready. We need final
product descriptions and launch announcement copy. I can finish the
product descriptions by Wednesday and the announcement by Thursday.

Rahul: Thursday is the internal content deadline.

Neha: Agreed.

Amit: I suggest enabling payment failure alerts and checking the
error dashboard during the first few days after launch.

Rahul: Add payment failure alerts before the release.

Sanjay (Support Lead): Customer support needs an FAQ covering
refunds, failed payments, delivery estimates, and account issues.
The support team can review it Friday.

Rahul: Add it to the launch checklist. The FAQ can be completed by
Friday afternoon.

Priya: The analytics team has ideas for extra charts, but they are
not required for this release.

Rahul: Move those extra analytics charts to the next sprint. They
must not delay the launch.

Neha: The team lunch could be moved to Friday.

Rahul: Fine, but it is not part of the release plan.

Amit: The staging server had a temporary slow response this morning,
but it recovered after a service restart.

Rahul: Add server monitoring to the release checklist, but do not
treat the earlier slowdown as a confirmed production issue.

Rahul: Let's target Monday for the public NovaCart launch, provided
payment testing, mobile checkout, content, monitoring, and the FAQ
are completed.

Everyone: Agreed.

Rahul: Final review will happen Friday afternoon. Update the project
board as tasks are completed. Meeting closed.
"""


# ============================================================
# SESSION STATE
# ============================================================
defaults = {
    "transcript": "",
    "analysis": None,
    "source_name": "",
    "is_demo": False,
    "chat_history": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# HELPER FUNCTIONS
# ============================================================
def clean_json(text):
    """Remove markdown code fences from an AI JSON response."""
    text = (text or "").strip()

    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


def normalize(data):
    """Make sure the AI response has the expected structure."""
    if not isinstance(data, dict):
        raise ValueError("Unexpected AI response format.")

    actions = data.get("action_items", [])

    if not isinstance(actions, list):
        actions = []

    clean_actions = []

    for item in actions:
        if isinstance(item, dict):
            priority = str(
                item.get("priority", "Not specified")
            ).title()

            if priority not in {
                "High",
                "Medium",
                "Low",
                "Not Specified"
            }:
                priority = "Not specified"

            clean_actions.append({
                "task": str(item.get("task", "Not specified")),
                "person": str(item.get("person", "Not specified")),
                "deadline": str(item.get("deadline", "Not specified")),
                "priority": priority
            })

    def list_value(key):
        value = data.get(key, [])

        if not isinstance(value, list):
            return []

        return [str(item) for item in value]

    return {
        "summary": str(
            data.get("summary", "No summary generated.")
        ),
        "meeting_duration": str(
            data.get("meeting_duration", "Not specified")
        ),
        "key_points": list_value("key_points"),
        "decisions": list_value("decisions"),
        "risks": list_value("risks"),
        "action_items": clean_actions
    }


def read_file(uploaded_file):
    """Read supported uploaded meeting files."""
    name = uploaded_file.name.lower()
    raw = uploaded_file.getvalue()

    if name.endswith((".txt", ".md", ".csv")):
        return raw.decode("utf-8", errors="ignore")

    if name.endswith(".pdf"):
        try:
            from pypdf import PdfReader
        except ImportError:
            raise ValueError(
                "PDF support needs pypdf. Run: "
                "python -m pip install pypdf"
            )

        reader = PdfReader(io.BytesIO(raw))

        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")

        return "\n".join(pages)

    if name.endswith(".docx"):
        try:
            from docx import Document
        except ImportError:
            raise ValueError(
                "DOCX support needs python-docx. Run: "
                "python -m pip install python-docx"
            )

        document = Document(io.BytesIO(raw))

        return "\n".join(
            paragraph.text for paragraph in document.paragraphs
        )

    raise ValueError(
        "Unsupported file. Use TXT, MD, CSV, PDF, or DOCX."
    )


def mode_instruction(mode):
    instructions = {
        "⚡ Quick Summary":
            "Be very concise; keep only outcomes and next steps.",

        "📋 Standard Summary":
            "Give a balanced meeting briefing.",

        "🎓 Simple Summary":
            "Use simple, easy-to-understand language.",

        "💼 Professional Summary":
            "Write a polished stakeholder-ready briefing."
    }

    return instructions[mode]


def analyze_with_gemini(transcript, mode):
    """Send the meeting transcript to Gemini and return structured JSON."""

    if not GEMINI_AVAILABLE:
        return None, (
            "Gemini package is missing. Run: "
            "python -m pip install google-genai"
        )

    if (
        not GEMINI_API_KEY
        or GEMINI_API_KEY == "PASTE_YOUR_API_KEY_HERE"
    ):
        return None, (
            "Paste your Gemini API key into GEMINI_API_KEY "
            "near the top of app.py."
        )

    prompt = f"""
You are an AI Meeting Assistant.

Your goal is to save the user's time. Do not rewrite the entire
conversation. Extract only useful information.

Prioritize:
- Decisions
- Key discussion points
- Action items
- Deadlines
- Responsible people
- Priorities
- Risks or problems
- Important project information

Ignore filler and casual conversation.

Summary style:
{mode}

Style instruction:
{mode_instruction(mode)}

Rules:
1. Use ONLY information supported by the transcript.
2. Never invent names, dates, tasks, decisions, or priorities.
3. A suggestion is not a decision unless it is explicitly agreed.
4. If information is unknown, write "Not specified".
5. Return ONLY valid JSON.
6. Keep the summary useful and concise.

Return exactly this JSON structure:

{{
    "summary": "Meeting summary",
    "meeting_duration": "Duration or Not specified",
    "key_points": [
        "Important point 1"
    ],
    "decisions": [
        "Confirmed decision 1"
    ],
    "risks": [
        "Important risk or problem"
    ],
    "action_items": [
        {{
            "task": "Task description",
            "person": "Responsible person",
            "deadline": "Deadline",
            "priority": "High/Medium/Low/Not specified"
        }}
    ]
}}

MEETING TRANSCRIPT:
{transcript}
"""

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        response_text = getattr(response, "text", None)

        if not response_text:
            return None, "Gemini returned an empty response."

        data = json.loads(clean_json(response_text))

        return normalize(data), None

    except json.JSONDecodeError:
        return None, "Gemini returned an invalid JSON response."

    except Exception as error:
        message = str(error)

        if (
            "401" in message
            or "403" in message
            or "api key" in message.lower()
        ):
            return None, (
                "Gemini rejected the API key. "
                "Check that your API key is valid."
            )

        return None, f"Gemini API error: {message}"


def ask_ai(question, transcript, analysis):
    """Answer questions using only the meeting information."""

    if not GEMINI_AVAILABLE:
        return None, "Gemini package is missing."

    if (
        not GEMINI_API_KEY
        or GEMINI_API_KEY == "PASTE_YOUR_API_KEY_HERE"
    ):
        return None, "Gemini API key is not configured."

    prompt = f"""
You are an AI Meeting Assistant.

Answer the user's question using ONLY the meeting transcript and
the generated analysis below.

Never invent information.

If the answer is not present in the meeting, say exactly:

"I couldn't find that information in the meeting."

MEETING TRANSCRIPT:
{transcript}

MEETING ANALYSIS:
{json.dumps(analysis, indent=2)}

USER QUESTION:
{question}
"""

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        answer = getattr(response, "text", None)

        if not answer:
            return None, "Gemini returned an empty answer."

        return answer.strip(), None

    except Exception as error:
        return None, f"Gemini Q&A error: {error}"


def create_download_text(analysis):
    """Create a text report for download."""

    lines = [
        "AI MEETING ASSISTANT",
        "=" * 55,
        "",
        "AI SUMMARY",
        "-" * 55,
        analysis["summary"],
        "",
        "MEETING DURATION",
        "-" * 55,
        analysis["meeting_duration"],
        "",
        "KEY POINTS",
        "-" * 55
    ]

    lines.extend(
        f"- {item}" for item in analysis["key_points"]
    )

    lines.extend([
        "",
        "DECISIONS MADE",
        "-" * 55
    ])

    lines.extend(
        f"- {item}" for item in analysis["decisions"]
    )

    lines.extend([
        "",
        "ACTION ITEMS",
        "-" * 55
    ])

    for item in analysis["action_items"]:
        lines.extend([
            f"- Task: {item['task']}",
            f"  Person: {item['person']}",
            f"  Deadline: {item['deadline']}",
            f"  Priority: {item['priority']}",
            ""
        ])

    lines.extend([
        "RISKS / PROBLEMS",
        "-" * 55
    ])

    lines.extend(
        f"- {item}" for item in analysis["risks"]
    )

    return "\n".join(lines)


# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="hero">
    <div class="hero-icon">🤖</div>
    <div class="hero-title">AI Meeting Assistant</div>
    <div class="hero-subtitle">
        Turn long meetings into clear, actionable insights.
    </div>
</div>
""", unsafe_allow_html=True)


status_columns = st.columns(3)

with status_columns[0]:
    st.caption("🏠 Dashboard")

with status_columns[1]:
    st.caption("📄 Meeting → ✨ Summary → 🤖 Q&A")

with status_columns[2]:
    if not GEMINI_AVAILABLE:
        st.caption("🔴 Gemini package missing")
    elif GEMINI_API_KEY == "PASTE_YOUR_API_KEY_HERE":
        st.caption("🟡 API key needed")
    else:
        st.caption("🟢 AI configured")


# ============================================================
# UPLOAD SECTION
# ============================================================
st.markdown("""
<div class="glass upload-card">
    <div class="section-title">Upload Your Meeting</div>
    <div class="section-subtitle">
        Upload a meeting transcript or supported meeting file
        and let AI extract the important information.
    </div>
</div>
""", unsafe_allow_html=True)


file_column, demo_column = st.columns([3, 1])

with file_column:
    uploaded_file = st.file_uploader(
        "Meeting file",
        type=["txt", "md", "csv", "pdf", "docx"],
        label_visibility="collapsed"
    )

with demo_column:
    if st.button(
        "🧪 Load Demo Data",
        use_container_width=True
    ):
        st.session_state.transcript = DEMO_TRANSCRIPT
        st.session_state.source_name = "Demo Data"
        st.session_state.is_demo = True
        st.session_state.analysis = None
        st.session_state.chat_history = []

        st.rerun()


if uploaded_file:
    try:
        uploaded_text = read_file(uploaded_file)

        if not uploaded_text.strip():
            st.warning("The uploaded file is empty.")

        else:
            st.session_state.transcript = uploaded_text
            st.session_state.source_name = uploaded_file.name
            st.session_state.is_demo = False

            st.success(
                f"Loaded: {uploaded_file.name}"
            )

    except ValueError as error:
        st.error(str(error))


# ============================================================
# TRANSCRIPT SECTION
# ============================================================
st.markdown(
    '<div class="section-title">📄 Meeting Content</div>',
    unsafe_allow_html=True
)

edited_transcript = st.text_area(
    "Transcript",
    value=st.session_state.transcript,
    height=220,
    placeholder=(
        "Paste your meeting transcript here, "
        "or load Demo Data..."
    ),
    label_visibility="collapsed"
)


if edited_transcript != st.session_state.transcript:
    st.session_state.transcript = edited_transcript
    st.session_state.source_name = "Pasted Transcript"
    st.session_state.is_demo = False


mode_column, button_column = st.columns([1, 1])

with mode_column:
    summary_mode = st.selectbox(
        "Summary Style",
        [
            "⚡ Quick Summary",
            "📋 Standard Summary",
            "🎓 Simple Summary",
            "💼 Professional Summary"
        ]
    )

with button_column:
    st.write("")

    generate_button = st.button(
        "✨ Generate AI Summary",
        type="primary",
        use_container_width=True
    )


# ============================================================
# AI PROCESSING
# ============================================================
if generate_button:

    if not st.session_state.transcript.strip():
        st.error(
            "No meeting content found. "
            "Upload, paste, or load Demo Data."
        )

    elif not GEMINI_AVAILABLE:
        st.error(
            "Gemini package is missing. "
            "Run: python -m pip install google-genai"
        )

    elif (
        not GEMINI_API_KEY
        or GEMINI_API_KEY == "PASTE_YOUR_API_KEY_HERE"
    ):
        st.error(
            "Gemini API key is missing. "
            "Paste it into GEMINI_API_KEY near the top of app.py."
        )

    else:
        progress = st.progress(0)

        status = st.status(
            "🤖 AI is analyzing your meeting...",
            expanded=True
        )

        status.write("✓ Reading meeting content")
        progress.progress(15)

        status.write("✓ Identifying important topics")
        progress.progress(30)

        status.write("✓ Extracting key points")
        progress.progress(45)

        status.write("✓ Detecting decisions")
        progress.progress(60)

        status.write("✓ Finding action items")
        progress.progress(75)

        result, error = analyze_with_gemini(
            st.session_state.transcript,
            summary_mode
        )

        if error:
            status.update(
                label="❌ AI analysis failed",
                state="error"
            )

            st.error(error)
            st.session_state.analysis = None

        else:
            status.write("✓ Preparing concise summary")
            progress.progress(100)

            status.update(
                label="✅ Meeting analysis complete",
                state="complete",
                expanded=False
            )

            st.session_state.analysis = result
            st.session_state.chat_history = []

            st.success(
                "AI summary generated successfully."
            )


# ============================================================
# RESULTS DASHBOARD
# ============================================================
analysis = st.session_state.analysis


if analysis:

    if st.session_state.is_demo:
        st.markdown(
            """
            <div class="demo-banner">
                🧪 <strong>Demo Data</strong> —
                Fictional meeting content used to demonstrate
                the application.
            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------
    st.markdown(
        '<div class="section-title">Meeting Overview</div>',
        unsafe_allow_html=True
    )

    statistics_columns = st.columns(4)

    statistics = [
        (
            "⏱ Meeting Duration",
            analysis["meeting_duration"]
        ),
        (
            "📌 Key Points",
            str(len(analysis["key_points"]))
        ),
        (
            "✅ Action Items",
            str(len(analysis["action_items"]))
        ),
        (
            "💡 Decisions",
            str(len(analysis["decisions"]))
        )
    ]

    for column, (label, value) in zip(
        statistics_columns,
        statistics
    ):
        with column:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-label">{label}</div>
                    <div class="stat-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


    # --------------------------------------------------------
    # AI SUMMARY
    # --------------------------------------------------------
    st.markdown(
        """
        <div class="content-card">
            <div class="section-title">✨ AI Summary</div>
            <div class="section-subtitle">
                Only the information that matters most.
            </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(analysis["summary"])

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # KEY POINTS + DECISIONS
    # --------------------------------------------------------
    left_column, right_column = st.columns(2)

    with left_column:
        st.markdown(
            """
            <div class="content-card">
                <div class="section-title">📌 Key Points</div>
            """,
            unsafe_allow_html=True
        )

        if analysis["key_points"]:
            for point in analysis["key_points"]:
                st.markdown(f"- {point}")
        else:
            st.info(
                "No key points were identified."
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    with right_column:
        st.markdown(
            """
            <div class="content-card">
                <div class="section-title">✅ Decisions Made</div>
            """,
            unsafe_allow_html=True
        )

        if analysis["decisions"]:
            for decision in analysis["decisions"]:
                st.markdown(
                    f"☑️ **{decision}**"
                )
        else:
            st.info(
                "No confirmed decisions were identified."
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # ACTION ITEMS
    # --------------------------------------------------------
    st.markdown(
        """
        <div class="content-card">
            <div class="section-title">📋 Action Items</div>
            <div class="section-subtitle">
                Tasks, owners, deadlines and priorities
                extracted from the meeting.
            </div>
        """,
        unsafe_allow_html=True
    )

    if analysis["action_items"]:

        for number, item in enumerate(
            analysis["action_items"],
            start=1
        ):
            priority = item["priority"]

            if priority.lower() == "high":
                priority_icon = "🔴"
            elif priority.lower() == "medium":
                priority_icon = "🟡"
            elif priority.lower() == "low":
                priority_icon = "🟢"
            else:
                priority_icon = "⚪"

            st.markdown(
                f"""
                <div class="action-item">
                    <strong>Action {number}</strong>
                    <br><br>

                    <strong>Task:</strong>
                    {item["task"]}
                    <br>

                    <strong>Responsible:</strong>
                    {item["person"]}
                    <br>

                    <strong>Deadline:</strong>
                    {item["deadline"]}
                    <br>

                    <strong>Priority:</strong>
                    {priority_icon} {priority}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        st.info(
            "No action items were identified."
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # RISKS / PROBLEMS
    # --------------------------------------------------------
    if analysis["risks"]:

        st.markdown(
            """
            <div class="content-card">
                <div class="section-title">
                    ⚠️ Important Risks / Problems
                </div>
            """,
            unsafe_allow_html=True
        )

        for risk in analysis["risks"]:
            st.markdown(f"- {risk}")

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # EXPORT
    # --------------------------------------------------------
    report_text = create_download_text(analysis)

    st.markdown(
        """
        <div class="content-card">
            <div class="section-title">📤 Export</div>
        """,
        unsafe_allow_html=True
    )

    export_left, export_right = st.columns(2)

    with export_left:
        st.download_button(
            "📋 Download Summary",
            report_text,
            "meeting_summary.txt",
            "text/plain",
            use_container_width=True
        )

    with export_right:
        st.download_button(
            "⬇️ Download Full Briefing",
            report_text,
            "ai_meeting_briefing.txt",
            "text/plain",
            use_container_width=True
        )

    st.caption(
        "The export buttons create copy-ready text files."
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # ORIGINAL MEETING CONTENT
    # --------------------------------------------------------
    with st.expander("📄 View Meeting Content"):
        st.text_area(
            "Meeting",
            st.session_state.transcript,
            height=260,
            disabled=True,
            label_visibility="collapsed"
        )


    # --------------------------------------------------------
    # AI Q&A
    # --------------------------------------------------------
    st.markdown(
        """
        <div class="content-card">
            <div class="section-title">
                🤖 Ask AI About This Meeting
            </div>

            <div class="section-subtitle">
                Ask questions using only the meeting content
                and generated analysis.
            </div>
        """,
        unsafe_allow_html=True
    )

    question = st.text_input(
        "Question",
        placeholder=(
            "What was decided about the project deadline?"
        ),
        label_visibility="collapsed"
    )

    ask_button = st.button(
        "🤖 Ask AI",
        use_container_width=True
    )

    if ask_button:

        if not question.strip():
            st.warning(
                "Enter a question first."
            )

        else:
            with st.spinner(
                "🤖 AI is checking the meeting..."
            ):
                answer, error = ask_ai(
                    question,
                    st.session_state.transcript,
                    analysis
                )

            if error:
                st.error(error)

            else:
                st.markdown(
                    f"""
                    <div class="answer-box">
                        <strong>AI Answer</strong>
                        <br><br>
                        {answer}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.session_state.chat_history.append(
                    (question, answer)
                )


    # Show recent questions and answers
    for question_text, answer_text in reversed(
        st.session_state.chat_history[-5:]
    ):
        st.markdown(
            f"**Q:** {question_text}"
        )
        st.markdown(
            f"**A:** {answer_text}"
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# SETUP INFORMATION
# ============================================================
with st.expander("⚙️ Settings / Setup"):

    st.markdown(
        """
        **Gemini API key:** paste it into
        `GEMINI_API_KEY` near the top of this file.

        **Required package:**
        `python -m pip install google-genai`

        **Optional PDF support:**
        `python -m pip install pypdf`

        **Optional DOCX support:**
        `python -m pip install python-docx`
        """
    )

    if GEMINI_AVAILABLE:
        st.write("Gemini package: ✅ Installed")
    else:
        st.write("Gemini package: ❌ Missing")

    if (
        GEMINI_API_KEY
        and GEMINI_API_KEY != "PASTE_YOUR_API_KEY_HERE"
    ):
        st.write("API key: ✅ Configured")
    else:
        st.write("API key: ⚠️ Not configured")


# ============================================================
# FOOTER
# ============================================================
st.markdown(
    """
    <div class="footer">
        PS-09 • AI Meeting Assistant Agent<br>
        Turn long meetings into clear, actionable briefings.
    </div>
    """,
    unsafe_allow_html=True
)
'''

path = Path("/mnt/data/app.py")
print(f"Created clean app.py: {path}")
print(f"Lines: {len(code.splitlines())}")
