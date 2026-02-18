import streamlit as st
from core.retriever import retrieve_legal_context
from core.legal_reasoner import generate_legal_answer

st.set_page_config(page_title="Legal Analyser AI", page_icon="⚖️", layout="wide")

# ─────────────────────────────────────────────────────────────────────────────
#  GLOBAL CSS  –  Clean professional light theme, excellent contrast & readability
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap');

/* ── Reset ──────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp              { background: #F0EDE8 !important; }
.block-container                { padding-top: 0 !important; padding-bottom: 60px; max-width: 1300px; }
header, #MainMenu, footer       { visibility: hidden; }

/* ── Design tokens ──────────────────────────────────────── */
:root {
    --brand:         #8B1A1A;
    --brand-dark:    #6b0f0f;
    --amber:         #B8860B;
    --amber-bg:      #FFFBEB;
    --amber-border:  #FDE68A;
    --bg:            #F0EDE8;
    --surface:       #FFFFFF;
    --surface-2:     #F7F4EF;
    --border:        #DDD8CF;
    --border-strong: #C8BFB2;
    --text-primary:  #1A1612;
    --text-body:     #3D3730;
    --text-muted:    #6B6358;
    --text-caption:  #9C9389;
    --blue:          #1e3a5f;
    --blue-bg:       #EFF6FF;
    --blue-border:   #BFDBFE;
    --green:         #14532D;
    --green-bg:      #F0FDF4;
    --green-border:  #BBF7D0;
    --radius-sm:     8px;
    --radius-md:     12px;
    --shadow-sm:     0 1px 3px rgba(0,0,0,0.07), 0 1px 2px rgba(0,0,0,0.04);
    --shadow-md:     0 4px 16px rgba(0,0,0,0.09), 0 2px 6px rgba(0,0,0,0.05);
}

/* ── Navbar ─────────────────────────────────────────────── */
.navbar {
    position: fixed; top: 0; left: 0; right: 0; height: 64px;
    background: var(--brand);
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 32px; z-index: 9999;
    box-shadow: 0 2px 8px rgba(0,0,0,0.22);
}
.nav-left  { display: flex; align-items: center; gap: 14px; }
.nav-icon-box {
    width: 40px; height: 40px;
    background: rgba(255,255,255,0.20); border-radius: 8px;
    display: flex; align-items: center; justify-content: center; font-size: 20px;
}
.nav-title {
    font-family: 'Lora', serif; font-size: 18px; font-weight: 700;
    color: #FFFFFF; letter-spacing: 0.01em;
}
.nav-sub {
    font-family: 'Inter', sans-serif; font-size: 11px;
    color: rgba(255,255,255,0.72); letter-spacing: 0.08em; text-transform: uppercase;
}
.nav-badge {
    font-family: 'JetBrains Mono', monospace; font-size: 11px;
    background: rgba(255,255,255,0.18); color: #FFFFFF;
    border: 1px solid rgba(255,255,255,0.28);
    padding: 4px 14px; border-radius: 20px; letter-spacing: 0.06em;
}

/* ── Push content below navbar ─────────────────────────── */
.main .block-container { padding-top: 84px !important; }

/* ── Hero screen ─────────────────────────────────────────── */
.hero-wrap {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius-md); padding: 48px 40px 36px;
    text-align: center; box-shadow: var(--shadow-sm); margin-bottom: 20px;
}
.hero-icon {
    width: 76px; height: 76px;
    background: linear-gradient(135deg, var(--brand), var(--brand-dark));
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-size: 34px; margin: 0 auto 20px;
    box-shadow: 0 6px 24px rgba(139,26,26,0.28);
}
.hero-title {
    font-family: 'Lora', serif; font-size: 30px; font-weight: 700;
    color: var(--text-primary); margin-bottom: 10px;
}
.hero-title em { color: var(--brand); font-style: normal; }
.hero-desc {
    font-family: 'Lora', serif; font-style: italic;
    font-size: 15.5px; color: var(--text-muted);
    max-width: 520px; margin: 0 auto 22px; line-height: 1.75;
}
.hero-rule { width: 56px; height: 3px; background: var(--brand); border-radius: 2px; margin: 0 auto 22px; }

/* ── Info banner ─────────────────────────────────────────── */
.howit-banner {
    background: var(--amber-bg); border: 1px solid var(--amber-border);
    border-left: 4px solid var(--amber); border-radius: var(--radius-sm);
    padding: 14px 18px; margin-bottom: 20px;
    display: flex; gap: 12px; align-items: flex-start;
}
.howit-text { font-family: 'Inter', sans-serif; font-size: 13.5px; color: #78350F; line-height: 1.65; }
.howit-text strong { color: #431A00; font-weight: 600; }

/* ── Sample question buttons ─────────────────────────────── */
.sample-title {
    font-family: 'Inter', sans-serif; font-weight: 600; font-size: 11.5px;
    text-transform: uppercase; letter-spacing: 0.10em;
    color: var(--text-muted); margin-bottom: 8px;
}
div[data-testid="stButton"] > button {
    width: 100% !important;
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-body) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13.5px !important; font-weight: 400 !important;
    text-align: left !important; padding: 12px 16px !important;
    transition: all 0.15s ease !important; line-height: 1.5 !important;
    box-shadow: var(--shadow-sm) !important;
}
div[data-testid="stButton"] > button:hover {
    border-color: var(--brand) !important;
    color: var(--brand) !important;
    background: #FFF5F5 !important;
    box-shadow: 0 2px 8px rgba(139,26,26,0.12) !important;
    transform: translateY(-1px) !important;
}

/* ── User message ───────────────────────────────────────── */
.user-msg-wrap {
    display: flex; gap: 12px; align-items: flex-start; margin: 24px 0 8px;
}
.user-avatar {
    width: 36px; height: 36px; flex-shrink: 0;
    background: var(--brand); border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; color: white;
    box-shadow: 0 2px 8px rgba(139,26,26,0.30);
}
.user-bubble {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 2px 12px 12px 12px;
    padding: 13px 18px;
    font-family: 'Inter', sans-serif; font-size: 14.5px; font-weight: 500;
    color: var(--text-primary); line-height: 1.6;
    max-width: 700px; box-shadow: var(--shadow-sm);
}

/* ── Answer card ────────────────────────────────────────── */
.answer-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius-md); overflow: hidden;
    margin: 6px 0 28px; box-shadow: var(--shadow-md);
}
.answer-card-header {
    background: linear-gradient(135deg, var(--brand) 0%, var(--brand-dark) 100%);
    padding: 14px 22px; display: flex; align-items: center; gap: 10px;
}
.answer-card-header-title {
    font-family: 'Lora', serif; font-size: 15px; font-weight: 700;
    color: #FFFFFF; letter-spacing: 0.02em; flex: 1;
}
.answer-card-header-tag {
    font-family: 'JetBrains Mono', monospace; font-size: 10px;
    background: rgba(255,255,255,0.20); color: rgba(255,255,255,0.92);
    padding: 3px 12px; border-radius: 20px; letter-spacing: 0.06em;
}

/* ── Answer section container ───────────────────────────── */
.ans-section { padding: 20px 24px; border-bottom: 1px solid var(--border); }
.ans-section:last-child { border-bottom: none; }

/* Section label pill */
.section-pill {
    display: inline-flex; align-items: center; gap: 6px;
    font-family: 'Inter', sans-serif; font-weight: 700;
    font-size: 11px; text-transform: uppercase; letter-spacing: 0.10em;
    padding: 4px 12px; border-radius: 20px; margin-bottom: 14px;
}
.pill-answer    { background: #FEF2F2; color: #991B1B; border: 1px solid #FECACA; }
.pill-reasoning { background: var(--blue-bg); color: var(--blue); border: 1px solid var(--blue-border); }
.pill-precedent { background: var(--amber-bg); color: #92400E; border: 1px solid var(--amber-border); }
.pill-guidance  { background: var(--green-bg); color: var(--green); border: 1px solid var(--green-border); }
.pill-raw       { background: var(--surface-2); color: var(--text-muted); border: 1px solid var(--border); }

/* Final answer – boldest, most prominent */
.final-answer-body {
    font-family: 'Lora', serif; font-size: 16px; font-weight: 600;
    color: var(--text-primary); line-height: 1.78;
    background: #FEF9F9; border-left: 4px solid var(--brand);
    padding: 14px 20px; border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
}
/* Legal reasoning */
.reasoning-body {
    font-family: 'Inter', sans-serif; font-size: 14.5px;
    color: var(--text-body); line-height: 1.82;
    background: var(--blue-bg); border-left: 4px solid var(--blue);
    padding: 14px 20px; border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
}
/* Precedent cards */
.precedent-card {
    display: flex; gap: 12px; align-items: flex-start;
    background: var(--amber-bg); border: 1px solid var(--amber-border);
    border-left: 4px solid var(--amber);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    padding: 12px 16px; margin-bottom: 10px;
}
.precedent-card:last-child { margin-bottom: 0; }
.precedent-icon { color: var(--amber); font-size: 15px; flex-shrink: 0; margin-top: 2px; }
.precedent-body {
    font-family: 'Inter', sans-serif; font-size: 13.5px;
    color: var(--text-body); line-height: 1.65;
}
.precedent-body strong { color: #3D2C00; font-weight: 600; }
/* Guidance */
.guidance-body {
    font-family: 'Inter', sans-serif; font-size: 14px; font-weight: 500;
    color: var(--green); line-height: 1.78;
    background: var(--green-bg); border-left: 4px solid var(--green);
    padding: 14px 20px; border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
}
/* Raw fallback */
.raw-body {
    font-family: 'Inter', sans-serif; font-size: 14px;
    color: var(--text-body); line-height: 1.82; white-space: pre-wrap;
}

/* ── Sidebar cards ───────────────────────────────────────── */
.sb-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius-md); overflow: hidden;
    margin-bottom: 16px; box-shadow: var(--shadow-sm);
}
.sb-card-hdr {
    background: var(--surface-2); border-bottom: 1px solid var(--border);
    padding: 11px 18px;
    display: flex; align-items: center; gap: 8px;
    font-family: 'Inter', sans-serif; font-size: 11.5px;
    font-weight: 700; text-transform: uppercase; letter-spacing: 0.10em;
    color: var(--text-body);
}
.sb-card-hdr-dot { width: 8px; height: 8px; background: var(--brand); border-radius: 50%; }
.sb-card-body { padding: 4px 0; }

.cap-row {
    display: flex; align-items: center; gap: 12px;
    padding: 9px 18px; border-bottom: 1px solid var(--border);
    font-family: 'Inter', sans-serif; font-size: 13.5px; color: var(--text-body);
}
.cap-row:last-child { border-bottom: none; }
.cap-icon-box {
    width: 30px; height: 30px; background: #FEF2F2; border-radius: 6px;
    display: flex; align-items: center; justify-content: center; font-size: 14px; flex-shrink: 0;
}

.stat-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 11px 18px; border-bottom: 1px solid var(--border);
    font-family: 'Inter', sans-serif;
}
.stat-row:last-child { border-bottom: none; }
.stat-key { font-size: 11.5px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); font-weight: 500; }
.stat-val { font-size: 15px; font-weight: 700; color: var(--text-primary); }

/* ── Chat input ─────────────────────────────────────────── */
div[data-testid="stChatInput"] textarea {
    background: var(--surface) !important;
    color: var(--text-primary) !important;
    border: 2px solid var(--border-strong) !important;
    border-radius: var(--radius-md) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14.5px !important;
}
div[data-testid="stChatInput"] textarea:focus {
    border-color: var(--brand) !important;
    box-shadow: 0 0 0 3px rgba(139,26,26,0.10) !important;
}
div[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-caption) !important;
}

/* ── Spinner ─────────────────────────────────────────────── */
div[data-testid="stSpinner"] p {
    font-family: 'Inter', sans-serif !important;
    color: var(--brand) !important; font-size: 14px !important;
}

/* ── Footer ──────────────────────────────────────────────── */
.footer-bar {
    text-align: center; font-family: 'Inter', sans-serif;
    font-size: 12px; color: var(--text-caption);
    padding: 20px; border-top: 1px solid var(--border); margin-top: 32px;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  NAVBAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <div class="nav-left">
        <div class="nav-icon-box">⚖️</div>
        <div>
            <div class="nav-title">Legal Analyser AI</div>
            <div class="nav-sub">Intelligent Legal Research · Indian Law</div>
        </div>
    </div>
    <div class="nav-badge">BETA v1.0</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
if "messages"    not in st.session_state: st.session_state.messages    = []
if "query_count" not in st.session_state: st.session_state.query_count = 0


# ─────────────────────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def parse_answer(text: str) -> dict:
    sections = {
        "final_answer": "", "legal_reasoning": "",
        "key_precedents": [], "practical_guidance": "", "raw": text,
    }
    cur, buf = None, []

    section_map = {
        "final answer:":       "final_answer",
        "legal reasoning:":    "legal_reasoning",
        "key precedent":       "key_precedents",
        "practical guidance:": "practical_guidance",
    }

    def flush(sec, buf):
        if   sec == "final_answer":       sections["final_answer"]       = " ".join(buf).strip()
        elif sec == "legal_reasoning":    sections["legal_reasoning"]    = "\n".join(buf).strip()
        elif sec == "key_precedents":     sections["key_precedents"]     = [l.lstrip("-•– ").strip() for l in buf if l.strip()]
        elif sec == "practical_guidance": sections["practical_guidance"] = "\n".join(buf).strip()

    for line in text.splitlines():
        low, matched = line.strip().lower(), False
        for key, sec in section_map.items():
            if low.startswith(key):
                if cur: flush(cur, buf)
                cur = sec
                rest = line.strip()[len(key):].strip() if sec != "key_precedents" else ""
                buf = [rest] if rest else []
                matched = True; break
        if not matched and cur:
            buf.append(line)
    if cur: flush(cur, buf)
    return sections


def render_answer_card(parsed: dict):
    has_structure = any([parsed["final_answer"], parsed["legal_reasoning"],
                         parsed["key_precedents"], parsed["practical_guidance"]])

    st.markdown("""
    <div class="answer-card">
        <div class="answer-card-header">
            <span style="font-size:18px">⚖️</span>
            <span class="answer-card-header-title">Legal Analysis Report</span>
            <span class="answer-card-header-tag">Indian Jurisdiction</span>
        </div>
    """, unsafe_allow_html=True)

    if not has_structure:
        st.markdown(f"""
        <div class="ans-section">
            <span class="section-pill pill-raw">📄 Response</span>
            <div class="raw-body">{parsed['raw']}</div>
        </div>""", unsafe_allow_html=True)
    else:
        if parsed["final_answer"]:
            st.markdown(f"""
            <div class="ans-section">
                <span class="section-pill pill-answer">✦ Final Answer</span>
                <div class="final-answer-body">{parsed['final_answer']}</div>
            </div>""", unsafe_allow_html=True)

        if parsed["legal_reasoning"]:
            st.markdown(f"""
            <div class="ans-section">
                <span class="section-pill pill-reasoning">§ Legal Reasoning</span>
                <div class="reasoning-body">{parsed['legal_reasoning']}</div>
            </div>""", unsafe_allow_html=True)

        if parsed["key_precedents"]:
            cards_html = "".join([
                f"""<div class="precedent-card">
                        <span class="precedent-icon">📋</span>
                        <div class="precedent-body">{p}</div>
                    </div>"""
                for p in parsed["key_precedents"] if p
            ])
            st.markdown(f"""
            <div class="ans-section">
                <span class="section-pill pill-precedent">⚑ Key Precedents</span>
                {cards_html}
            </div>""", unsafe_allow_html=True)

        if parsed["practical_guidance"]:
            st.markdown(f"""
            <div class="ans-section">
                <span class="section-pill pill-guidance">→ Practical Guidance</span>
                <div class="guidance-body">{parsed['practical_guidance']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  LAYOUT
# ─────────────────────────────────────────────────────────────────────────────
col_main, col_right = st.columns([3, 1.1])

# ── RIGHT SIDEBAR ───────────────────────────────────────────
with col_right:
    st.markdown("""
    <div class="sb-card">
        <div class="sb-card-hdr"><div class="sb-card-hdr-dot"></div> System Capabilities</div>
        <div class="sb-card-body">
            <div class="cap-row"><div class="cap-icon-box">🏛</div> Supreme Court Judgments</div>
            <div class="cap-row"><div class="cap-icon-box">⚖️</div> High Court Case Law</div>
            <div class="cap-row"><div class="cap-icon-box">📜</div> Constitutional Provisions</div>
            <div class="cap-row"><div class="cap-icon-box">📚</div> Statutory Provisions</div>
            <div class="cap-row"><div class="cap-icon-box">🔍</div> Semantic Retrieval (RAG)</div>
            <div class="cap-row"><div class="cap-icon-box">🧠</div> Legal Reasoning Engine</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    q = st.session_state.query_count
    st.markdown(f"""
    <div class="sb-card">
        <div class="sb-card-hdr"><div class="sb-card-hdr-dot"></div> Session Stats</div>
        <div class="sb-card-body">
            <div class="stat-row"><span class="stat-key">Queries</span><span class="stat-val">{q}</span></div>
            <div class="stat-row"><span class="stat-key">Jurisdiction</span><span class="stat-val">India</span></div>
            <div class="stat-row"><span class="stat-key">Sources</span><span class="stat-val">SC + HC</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sb-card">
        <div class="sb-card-hdr"><div class="sb-card-hdr-dot"></div> Disclaimer</div>
        <div class="sb-card-body" style="padding:14px 18px;">
            <p style="font-family:'Inter',sans-serif;font-size:12.5px;color:#6B6358;line-height:1.70;margin:0;">
                This tool provides legal information grounded in Indian case law.
                It is <strong style="color:#3D3730;">not a substitute</strong> for advice
                from a qualified advocate.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── MAIN AREA ───────────────────────────────────────────────
with col_main:

    # Hero (only before first query)
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div class="hero-wrap">
            <div class="hero-icon">⚖️</div>
            <div class="hero-title">Welcome to <em>Legal Analyser AI</em></div>
            <div class="hero-desc">
                Ask any question about Indian law and receive a structured legal opinion
                backed by real Supreme Court and High Court judgments.
            </div>
            <div class="hero-rule"></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="howit-banner">
            <div style="font-size:18px;flex-shrink:0;margin-top:1px;">ℹ️</div>
            <div class="howit-text">
                <strong>How it works:</strong> Your query is matched against a corpus of Supreme Court &amp;
                High Court judgments and constitutional provisions. The reasoning engine synthesises a
                <strong>structured legal opinion</strong> — not a chatbot reply.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sample-title">Try a sample question</div>', unsafe_allow_html=True)

        samples = [
            ("🏛", "What are my rights under Article 21 of the Constitution?"),
            ("🏠", "Explain the legal requirements for property transfer"),
            ("🔒", "What is the Supreme Court judgment on Right to Privacy?"),
            ("📋", "Can I claim adverse possession of land after 12 years?"),
        ]
        for icon, text in samples:
            if st.button(f"{icon}  {text}", key=f"sq_{text[:20]}"):
                st.session_state.pending_question = text

    # Chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="user-msg-wrap">
                <div class="user-avatar">👤</div>
                <div class="user-bubble">{msg["content"]}</div>
            </div>""", unsafe_allow_html=True)
        else:
            render_answer_card(parse_answer(msg["content"]))

    # Input
    query = st.chat_input("Ask a legal question about Indian law…")

    if "pending_question" in st.session_state:
        query = st.session_state.pending_question
        del st.session_state.pending_question

    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        st.session_state.query_count += 1
        with st.spinner("Retrieving judgments and analysing legal sources…"):
            evidence = retrieve_legal_context(query)
            answer   = generate_legal_answer(query, evidence)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-bar">
    Legal Analyser AI · Grounded in Indian case law · Not a substitute for professional legal advice
</div>
""", unsafe_allow_html=True)