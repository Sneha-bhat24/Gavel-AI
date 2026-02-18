import streamlit as st
import re
from core.retriever import retrieve_legal_context
from core.legal_reasoner import generate_legal_answer

st.set_page_config(page_title="Gavel-AI", page_icon="⚖️", layout="centered")

# ─────────────────────────────────────────────────────────────────────────────
#  CSS  —  Matches the Figma design exactly: white + blue, clean, trustworthy
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Lora:ital,wght@0,600;0,700;1,500&display=swap');

/* ── Reset ─────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp     { background: #F5F7FA !important; }
.block-container       { padding-top: 0 !important; padding-bottom: 100px; max-width: 820px; }
header, #MainMenu, footer { visibility: hidden; }

/* ── Tokens ─────────────────────────────────────────────── */
:root {
    --blue:         #1A56DB;
    --blue-dark:    #1245B0;
    --blue-light:   #EBF2FF;
    --blue-border:  #BFDBFE;
    --blue-mid:     #3B82F6;
    --white:        #FFFFFF;
    --gray-50:      #F9FAFB;
    --gray-100:     #F3F4F6;
    --gray-200:     #E5E7EB;
    --gray-300:     #D1D5DB;
    --gray-400:     #9CA3AF;
    --gray-500:     #6B7280;
    --gray-600:     #4B5563;
    --gray-700:     #374151;
    --gray-800:     #1F2937;
    --gray-900:     #111827;
    --green:        #065F46;
    --green-bg:     #ECFDF5;
    --green-border: #6EE7B7;
    --radius-sm:    6px;
    --radius-md:    10px;
    --radius-lg:    14px;
    --shadow-sm:    0 1px 3px rgba(0,0,0,0.08);
    --shadow-md:    0 4px 12px rgba(0,0,0,0.08), 0 1px 4px rgba(0,0,0,0.04);
}

/* ── Navbar ─────────────────────────────────────────────── */
.gavel-nav {
    position: fixed; top: 0; left: 0; right: 0; height: 60px;
    background: var(--white);
    border-bottom: 1px solid var(--gray-200);
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 32px; z-index: 9999;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.gn-brand { display: flex; align-items: center; gap: 12px; }
.gn-logo {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, var(--blue), var(--blue-dark));
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 19px; box-shadow: 0 2px 8px rgba(26,86,219,0.30);
}
.gn-title {
    font-family: 'Inter', sans-serif; font-weight: 700; font-size: 18px;
    color: var(--gray-900); letter-spacing: -0.01em;
}
.gn-sub {
    font-family: 'Inter', sans-serif; font-size: 11.5px;
    color: var(--gray-400); margin-top: 0px;
}
.gn-badge {
    font-family: 'Inter', sans-serif; font-size: 11px; font-weight: 500;
    color: var(--blue); background: var(--blue-light);
    border: 1px solid var(--blue-border);
    padding: 3px 12px; border-radius: 20px; letter-spacing: 0.02em;
}

/* ── Page offset ────────────────────────────────────────── */
.main .block-container { padding-top: 80px !important; }

/* ── Hero screen ────────────────────────────────────────── */
.hero-wrap {
    background: var(--white);
    border: 1px solid var(--gray-200);
    border-radius: var(--radius-lg);
    padding: 52px 48px 44px;
    text-align: center;
    box-shadow: var(--shadow-sm);
    margin-bottom: 16px;
}
.hero-logo-big {
    width: 72px; height: 72px;
    background: linear-gradient(135deg, var(--blue), var(--blue-dark));
    border-radius: 18px;
    display: flex; align-items: center; justify-content: center;
    font-size: 33px; margin: 0 auto 20px;
    box-shadow: 0 6px 20px rgba(26,86,219,0.25);
}
.hero-title {
    font-family: 'Inter', sans-serif; font-size: 28px; font-weight: 700;
    color: var(--gray-900); margin-bottom: 10px; letter-spacing: -0.02em;
}
.hero-desc {
    font-family: 'Inter', sans-serif; font-size: 15px; color: var(--gray-500);
    max-width: 500px; margin: 0 auto 28px; line-height: 1.70;
}

/* How it works card */
.howit-card {
    background: var(--blue-light);
    border: 1px solid var(--blue-border);
    border-radius: var(--radius-md);
    padding: 16px 20px;
    display: flex; gap: 12px; align-items: flex-start;
    text-align: left; margin-bottom: 28px;
}
.howit-icon { font-size: 18px; flex-shrink: 0; margin-top: 1px; }
.howit-text {
    font-family: 'Inter', sans-serif; font-size: 13.5px;
    color: #1E40AF; line-height: 1.65;
}
.howit-text strong { color: #1E3A8A; font-weight: 600; }

/* Sample questions label */
.sample-label {
    font-family: 'Inter', sans-serif; font-weight: 600; font-size: 13px;
    color: var(--gray-700); margin-bottom: 10px; text-align: left;
}

/* Sample buttons */
div[data-testid="stButton"] > button {
    width: 100% !important;
    background: var(--white) !important;
    border: 1px solid var(--gray-200) !important;
    border-radius: var(--radius-md) !important;
    color: var(--gray-700) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important; font-weight: 400 !important;
    text-align: left !important; padding: 13px 16px !important;
    transition: all 0.15s ease !important;
    box-shadow: var(--shadow-sm) !important;
    margin-bottom: 4px !important;
}
div[data-testid="stButton"] > button:hover {
    border-color: var(--blue-border) !important;
    background: var(--blue-light) !important;
    color: var(--blue) !important;
}

/* ── Query display ───────────────────────────────────────── */
.query-wrap {
    display: flex; align-items: flex-start; gap: 12px;
    margin: 28px 0 16px;
}
.query-avatar {
    width: 34px; height: 34px; flex-shrink: 0;
    background: linear-gradient(135deg, var(--blue), var(--blue-dark));
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 15px; font-weight: 700;
    font-family: 'Inter', sans-serif;
    box-shadow: 0 2px 8px rgba(26,86,219,0.28);
}
.query-bubble {
    background: linear-gradient(135deg, var(--blue) 0%, var(--blue-dark) 100%);
    border-radius: 4px 14px 14px 14px;
    padding: 12px 18px;
    font-family: 'Inter', sans-serif; font-size: 15px; font-weight: 500;
    color: #FFFFFF; line-height: 1.55; flex: 1;
    box-shadow: 0 2px 10px rgba(26,86,219,0.22);
}

/* ── Answer panel ────────────────────────────────────────── */
.answer-panel {
    background: var(--white);
    border: 1px solid var(--gray-200);
    border-radius: var(--radius-lg);
    overflow: hidden;
    margin-bottom: 8px;
    box-shadow: var(--shadow-md);
}
.answer-body {
    padding: 24px 28px;
    font-family: 'Inter', sans-serif;
    font-size: 15px; color: var(--gray-800); line-height: 1.80;
}
.answer-body p { margin-bottom: 14px; }
.answer-body p:last-child { margin-bottom: 0; }
.answer-body ul { padding-left: 20px; margin: 10px 0; }
.answer-body li { margin-bottom: 6px; color: var(--gray-700); }
.answer-body strong { color: var(--gray-900); font-weight: 600; }

/* ── Legal References bar ────────────────────────────────── */
.refs-bar {
    border: 1px solid var(--gray-200);
    border-radius: var(--radius-lg);
    overflow: hidden;
    margin-bottom: 24px;
    box-shadow: var(--shadow-sm);
    background: var(--white);
}
.refs-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 20px;
    cursor: pointer;
    background: var(--white);
    user-select: none;
    transition: background 0.14s;
}
.refs-header:hover { background: var(--gray-50); }
.refs-header-left { display: flex; align-items: center; gap: 10px; }
.refs-icon { font-size: 16px; color: var(--blue); }
.refs-title {
    font-family: 'Inter', sans-serif; font-size: 14px; font-weight: 600;
    color: var(--gray-800);
}
.refs-pills { display: flex; gap: 6px; }
.refs-pill {
    font-family: 'Inter', sans-serif; font-size: 11.5px; font-weight: 500;
    padding: 2px 10px; border-radius: 20px;
}
.refs-pill-cases   { background: #EFF6FF; color: var(--blue); border: 1px solid var(--blue-border); }
.refs-pill-provs   { background: #F0FDF4; color: var(--green); border: 1px solid var(--green-border); }
.refs-chevron { font-size: 13px; color: var(--gray-400); transition: transform 0.2s; }
.refs-chevron.open { transform: rotate(180deg); }

/* Refs expanded body */
.refs-body { border-top: 1px solid var(--gray-200); }

/* Sub-section heading inside refs */
.refs-subsection-title {
    display: flex; align-items: center; gap: 8px;
    padding: 14px 20px 10px;
    font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 600;
    letter-spacing: 0.08em; text-transform: uppercase; color: var(--gray-500);
    border-bottom: 1px solid var(--gray-100);
}

/* Case card */
.case-card {
    padding: 18px 20px;
    border-bottom: 1px solid var(--gray-100);
}
.case-card:last-child { border-bottom: none; }
.case-header {
    display: flex; align-items: flex-start; justify-content: space-between;
    margin-bottom: 4px;
}
.case-name {
    font-family: 'Inter', sans-serif; font-size: 15px; font-weight: 600;
    color: var(--gray-900);
}
.case-year {
    font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 600;
    color: var(--blue); background: var(--blue-light);
    border: 1px solid var(--blue-border);
    padding: 2px 9px; border-radius: 4px; flex-shrink: 0; margin-left: 12px;
}
.case-citation {
    font-family: 'Inter', sans-serif; font-size: 12.5px; color: var(--gray-400);
    margin-bottom: 10px;
}
.case-summary {
    font-family: 'Inter', sans-serif; font-size: 14px; color: var(--gray-700);
    line-height: 1.65; margin-bottom: 10px;
}
.relevance-box {
    background: var(--blue-light); border-left: 3px solid var(--blue);
    padding: 8px 14px; border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    font-family: 'Inter', sans-serif; font-size: 13px; color: #1E3A8A;
    line-height: 1.55;
}
.relevance-box strong { font-weight: 600; color: var(--blue-dark); }

/* Provision card */
.prov-card {
    padding: 18px 20px;
    border-bottom: 1px solid var(--gray-100);
}
.prov-card:last-child { border-bottom: none; }
.prov-header {
    display: flex; align-items: flex-start; justify-content: space-between;
    margin-bottom: 3px;
}
.prov-name {
    font-family: 'Inter', sans-serif; font-size: 15px; font-weight: 600;
    color: var(--gray-900);
}
.prov-tag {
    font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 600;
    color: var(--green); background: var(--green-bg);
    border: 1px solid var(--green-border);
    padding: 2px 9px; border-radius: 4px; flex-shrink: 0; margin-left: 12px;
}
.prov-source {
    font-family: 'Inter', sans-serif; font-size: 12.5px; color: var(--gray-400);
    margin-bottom: 10px;
}
.prov-quote {
    font-family: 'Lora', serif; font-style: italic;
    font-size: 14px; color: var(--gray-700); line-height: 1.72;
    border-left: 3px solid var(--gray-300);
    padding: 8px 14px; margin-bottom: 10px;
    background: var(--gray-50);
}
.prov-relevance-box {
    background: var(--blue-light); border-left: 3px solid var(--blue);
    padding: 8px 14px; border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    font-family: 'Inter', sans-serif; font-size: 13px; color: #1E3A8A;
    line-height: 1.55;
}
.prov-relevance-box strong { font-weight: 600; color: var(--blue-dark); }

/* Guidance section inside answer (advisory note) */
.guidance-note {
    background: var(--green-bg); border: 1px solid var(--green-border);
    border-left: 3px solid var(--green); border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    padding: 14px 18px; margin-top: 16px;
    font-family: 'Inter', sans-serif; font-size: 14px; color: #064E3B;
    line-height: 1.68;
}
.guidance-note-label {
    font-size: 11px; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: var(--green); margin-bottom: 6px;
}

/* ── Input ───────────────────────────────────────────────── */
div[data-testid="stChatInput"] > div {
    background: var(--white) !important;
    border: 1.5px solid var(--gray-300) !important;
    border-radius: var(--radius-lg) !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08) !important;
    transition: border-color 0.15s !important;
}
div[data-testid="stChatInput"] > div:focus-within {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 3px rgba(26,86,219,0.10), 0 2px 12px rgba(0,0,0,0.08) !important;
}
div[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: var(--gray-900) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important; border: none !important;
    padding: 14px 16px !important;
}
div[data-testid="stChatInput"] textarea::placeholder {
    color: var(--gray-400) !important;
}
/* Send button */
div[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, var(--blue), var(--blue-dark)) !important;
    border-radius: 8px !important; border: none !important;
    color: white !important;
}
div[data-testid="stChatInput"] button:hover {
    background: linear-gradient(135deg, var(--blue-mid), var(--blue)) !important;
}

/* Input hint */
.input-hint {
    text-align: center; font-family: 'Inter', sans-serif;
    font-size: 11.5px; color: var(--gray-400); margin-top: 6px;
}

/* ── Spinner ─────────────────────────────────────────────── */
div[data-testid="stSpinner"] p {
    font-family: 'Inter', sans-serif !important;
    color: var(--blue) !important; font-size: 14px !important;
}

/* ── Footer ──────────────────────────────────────────────── */
.gavel-footer {
    text-align: center; font-family: 'Inter', sans-serif;
    font-size: 12px; color: var(--gray-400);
    padding: 20px 0 0; border-top: 1px solid var(--gray-200); margin-top: 20px;
}
.gavel-footer a { color: var(--blue); text-decoration: underline; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  NAVBAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="gavel-nav">
    <div class="gn-brand">
        <div class="gn-logo">⚖️</div>
        <div>
            <div class="gn-title">Gavel-AI</div>
            <div class="gn-sub">Intelligent Legal Research · Indian Law</div>
        </div>
    </div>
    <div class="gn-badge">Demo Version</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
if "messages"     not in st.session_state: st.session_state.messages     = []
if "query_count"  not in st.session_state: st.session_state.query_count  = 0
if "refs_open"    not in st.session_state: st.session_state.refs_open    = {}


# ─────────────────────────────────────────────────────────────────────────────
#  PARSER
# ─────────────────────────────────────────────────────────────────────────────
def parse_answer(text: str) -> dict:
    """Extract structured sections from LLM output."""
    sections = {
        "final_answer":       "",
        "legal_reasoning":    "",
        "key_precedents":     [],
        "practical_guidance": "",
        "raw":                text,
    }
    cur, buf = None, []

    markers = {
        "final answer:":       "final_answer",
        "legal reasoning:":    "legal_reasoning",
        "key precedent":       "key_precedents",
        "practical guidance:": "practical_guidance",
    }

    def flush(sec, buf):
        if   sec == "final_answer":       sections["final_answer"]       = " ".join(b for b in buf if b).strip()
        elif sec == "legal_reasoning":    sections["legal_reasoning"]    = "\n".join(buf).strip()
        elif sec == "key_precedents":     sections["key_precedents"]     = [l.lstrip("-•– ").strip() for l in buf if l.strip()]
        elif sec == "practical_guidance": sections["practical_guidance"] = "\n".join(buf).strip()

    for line in text.splitlines():
        low, hit = line.strip().lower(), False
        for marker, sec in markers.items():
            if low.startswith(marker):
                if cur: flush(cur, buf)
                cur = sec
                rest = line.strip()[len(marker):].strip() if sec != "key_precedents" else ""
                buf = [rest] if rest else []
                hit = True; break
        if not hit and cur:
            buf.append(line)
    if cur:
        flush(cur, buf)
    return sections


def parse_precedent(raw: str):
    """Split 'Case Name — legal principle' into (name, ratio)."""
    for sep in [" — ", " – ", " - "]:
        if sep in raw:
            parts = raw.split(sep, 1)
            return parts[0].strip(), parts[1].strip()
    if "," in raw[:70]:
        idx = raw.index(",")
        return raw[:idx].strip(), raw[idx+1:].strip()
    return raw.strip(), ""


def build_answer_text(parsed: dict) -> str:
    """Combine final_answer + legal_reasoning into one readable answer body."""
    parts = []
    if parsed["final_answer"]:
        parts.append(parsed["final_answer"])
    if parsed["legal_reasoning"]:
        parts.append(parsed["legal_reasoning"])
    if not parts:
        return parsed["raw"]
    return "\n\n".join(parts)


def format_answer_html(text: str) -> str:
    """Convert plain text answer to readable HTML paragraphs."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    return "".join(f"<p>{p}</p>" for p in paragraphs)


# ─────────────────────────────────────────────────────────────────────────────
#  RENDER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────
def render_answer_with_refs(parsed: dict, msg_idx: int):
    """Render a full answer panel + collapsible Legal References bar."""

    # ── Answer panel ──────────────────────────────────────────
    answer_text = build_answer_text(parsed)
    answer_html = format_answer_html(answer_text)

    guidance_html = ""
    if parsed["practical_guidance"]:
        guidance_html = f"""
        <div class="guidance-note">
            <div class="guidance-note-label">Advisory Note</div>
            {parsed['practical_guidance']}
        </div>"""

    st.markdown(f"""
    <div class="answer-panel">
        <div class="answer-body">
            {answer_html}
            {guidance_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Legal References collapsible bar ──────────────────────
    precs = parsed["key_precedents"]
    if not precs:
        return

    # Count cases vs provisions (heuristic: contains "Article" or "Section" → provision)
    cases_list = []
    provs_list = []
    for p in precs:
        if re.search(r'\bArticle\b|\bSection\b|\bSchedule\b|\bClause\b', p, re.I):
            provs_list.append(p)
        else:
            cases_list.append(p)

    n_total  = len(precs)
    n_cases  = len(cases_list)
    n_provs  = len(provs_list)

    pills_html = ""
    if n_cases:
        pills_html += f'<span class="refs-pill refs-pill-cases">{n_cases} Case{"s" if n_cases>1 else ""}</span>'
    if n_provs:
        pills_html += f'<span class="refs-pill refs-pill-provs">{n_provs} Provision{"s" if n_provs>1 else ""}</span>'
    if not pills_html:
        pills_html = f'<span class="refs-pill refs-pill-cases">{n_total} Reference{"s" if n_total>1 else ""}</span>'

    # Toggle state
    key = f"refs_{msg_idx}"
    if key not in st.session_state.refs_open:
        st.session_state.refs_open[key] = False

    is_open = st.session_state.refs_open[key]
    chevron_cls = "refs-chevron open" if is_open else "refs-chevron"
    chevron = "▲" if is_open else "▼"

    # Clickable header using Streamlit button styled as the bar
    col1, col2 = st.columns([1, 0.001])
    with col1:
        if st.button(
            f"📋  Legal References ({n_total})   {('▲ collapse' if is_open else '▼ expand')}",
            key=f"refs_toggle_{msg_idx}",
            help="Click to expand/collapse legal references"
        ):
            st.session_state.refs_open[key] = not st.session_state.refs_open[key]
            st.rerun()

    # Expanded content
    if st.session_state.refs_open.get(key, False):
        # ── Court Judgments ──
        if cases_list:
            st.markdown("""
            <div style="background:white;border:1px solid #E5E7EB;border-radius:10px;overflow:hidden;margin-bottom:12px;">
                <div style="padding:10px 18px 8px;font-family:Inter,sans-serif;font-size:11px;font-weight:700;
                     letter-spacing:0.12em;text-transform:uppercase;color:#6B7280;
                     border-bottom:1px solid #F3F4F6;display:flex;align-items:center;gap:8px;">
                    ⚖️ Court Judgments
                </div>
            """, unsafe_allow_html=True)

            for p in cases_list:
                name, ratio = parse_precedent(p)
                # Extract year if present (4-digit number)
                year_match = re.search(r'\b(19|20)\d{2}\b', name)
                year = year_match.group(0) if year_match else ""
                clean_name = re.sub(r'\s*[\(\[]\d{4}[\)\]]', '', name).strip()

                # Guess citation
                citation_line = "Supreme Court of India"
                if "high court" in clean_name.lower():
                    citation_line = "High Court"

                ratio_html = ""
                if ratio:
                    ratio_html = f'<div class="relevance-box"><strong>Relevance:</strong> {ratio}</div>'

                year_badge = f'<span class="case-year">{year}</span>' if year else ""

                st.markdown(f"""
                <div class="case-card">
                    <div class="case-header">
                        <span class="case-name">{clean_name}</span>
                        {year_badge}
                    </div>
                    <div class="case-citation">{citation_line}</div>
                    {ratio_html}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # ── Constitutional / Statutory Provisions ──
        if provs_list:
            st.markdown("""
            <div style="background:white;border:1px solid #E5E7EB;border-radius:10px;overflow:hidden;margin-bottom:12px;">
                <div style="padding:10px 18px 8px;font-family:Inter,sans-serif;font-size:11px;font-weight:700;
                     letter-spacing:0.12em;text-transform:uppercase;color:#6B7280;
                     border-bottom:1px solid #F3F4F6;display:flex;align-items:center;gap:8px;">
                    📜 Constitutional / Statutory Provisions
                </div>
            """, unsafe_allow_html=True)

            for p in provs_list:
                name, ratio = parse_precedent(p)

                # Extract article/section tag
                art_match = re.search(r'(Article\s+\d+[A-Z]?|Section\s+\d+[A-Z]?)', name, re.I)
                art_tag = art_match.group(0).title() if art_match else ""
                art_badge = f'<span class="prov-tag">{art_tag}</span>' if art_tag else ""

                ratio_html = ""
                if ratio:
                    ratio_html = f'<div class="prov-relevance-box"><strong>Relevance:</strong> {ratio}</div>'

                st.markdown(f"""
                <div class="prov-card">
                    <div class="prov-header">
                        <span class="prov-name">{name}</span>
                        {art_badge}
                    </div>
                    <div class="prov-source">Constitution of India</div>
                    {ratio_html}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────────────────────

# Hero screen (before first query)
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-logo-big">⚖️</div>
        <div class="hero-title">Welcome to Gavel-AI</div>
        <div class="hero-desc">
            Ask any question about Indian law. Get answers backed by
            real court judgments and constitutional provisions.
        </div>
        <div class="howit-card">
            <div class="howit-icon">ℹ️</div>
            <div class="howit-text">
                <strong>How it works:</strong> Every answer is grounded in actual legal sources.
                The system retrieves relevant judgments from Supreme Court and High Courts, along
                with applicable constitutional articles and statutory provisions. This ensures
                explainable, precedent-backed legal reasoning.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sample-label">Try these sample questions:</div>', unsafe_allow_html=True)

    samples = [
        "What are my rights under Article 21 of the Constitution?",
        "Explain the legal requirements for property transfer",
        "What is the latest Supreme Court judgment on privacy?",
        "Can I claim adverse possession of property?",
    ]
    for s in samples:
        if st.button(s, key=f"sq_{s[:25]}"):
            st.session_state.pending_question = s


# Chat history
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="query-wrap">
            <div class="query-avatar">U</div>
            <div class="query-bubble">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        parsed = parse_answer(msg["content"])
        render_answer_with_refs(parsed, i)


# Input
query = st.chat_input("Ask a legal question... (e.g., 'What are my rights under Article 21?' or 'Latest judgment on property disputes')")

if "pending_question" in st.session_state:
    query = st.session_state.pending_question
    del st.session_state.pending_question

if query:
    st.session_state.messages.append({"role": "user",      "content": query})
    st.session_state.query_count += 1
    with st.spinner("Analysing legal sources and retrieving relevant judgments…"):
        evidence = retrieve_legal_context(query)
        answer   = generate_legal_answer(query, evidence)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()


# Footer
st.markdown("""
<div class="gavel-footer">
    Gavel-AI provides information based on Indian law. This is not a substitute for professional legal advice.
    Consult a <a href="#">qualified lawyer</a> for specific legal matters.
</div>
""", unsafe_allow_html=True)