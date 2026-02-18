import streamlit as st
from core.retriever import retrieve_legal_context
from core.legal_reasoner import generate_legal_answer

st.set_page_config(page_title="Legal Analyser AI", page_icon="⚖️", layout="wide")

# ─────────────────────────────────────────────────────────────────────────────
#  CSS — Judicial document aesthetic. Think SCC Online, not SaaS dashboard.
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=Source+Sans+3:wght@400;500;600&display=swap');

/* ── Foundational reset ─────────────────────────────────── */
*, *::before, *::after   { box-sizing: border-box; }
html, body, .stApp       { background: #F5F1EA !important; }
.block-container         { padding-top: 0 !important; padding-bottom: 80px; max-width: 1240px; }
header, #MainMenu, footer{ visibility: hidden; }

/* ── Token system ───────────────────────────────────────── */
:root {
    /* Paper tones */
    --paper:          #F9F6F0;       /* document surface                     */
    --paper-ruled:    #F3EFE7;       /* slightly darker tint                 */
    --page-bg:        #EDE9E1;       /* outer page background                */

    /* Ink tones */
    --ink-primary:    #1C1812;       /* headline / holding text              */
    --ink-body:       #2E2A24;       /* body paragraphs                      */
    --ink-secondary:  #5A5448;       /* secondary labels, captions           */
    --ink-muted:      #8C867C;       /* metadata, timestamps                 */

    /* Rule / border */
    --rule-light:     #D8D2C8;       /* thin separator                       */
    --rule-medium:    #C4BDB2;       /* section divider                      */

    /* Accent: deep ink-blue (judicial authority) */
    --accent:         #1A3A5C;       /* section labels, links                */
    --accent-light:   #EBF0F7;       /* holding highlight background         */
    --accent-border:  #B8CCDF;

    /* Sienna for citations (echoes red stamps in legal docs) */
    --cite:           #7A3B19;
    --cite-bg:        #FBF5F0;
    --cite-border:    #D4B49A;

    /* Forest for guidance */
    --guide:          #1A4731;
    --guide-bg:       #F1F8F4;
    --guide-border:   #A8CDB8;

    /* Layout */
    --radius:         4px;           /* minimal rounding — documents are square */
    --shadow-paper:   0 1px 4px rgba(0,0,0,0.08), 0 4px 16px rgba(0,0,0,0.06);
}

/* ── Court header bar ───────────────────────────────────── */
.court-header {
    position: fixed; top: 0; left: 0; right: 0; height: 56px;
    background: var(--ink-primary);
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 36px;
    z-index: 9999;
    border-bottom: 3px solid var(--accent);
}
.ch-left   { display: flex; align-items: center; gap: 14px; }
.ch-seal   {
    width: 34px; height: 34px;
    border: 1.5px solid rgba(255,255,255,0.30);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 17px;
}
.ch-title  {
    font-family: 'EB Garamond', serif;
    font-size: 18px; font-weight: 600; letter-spacing: 0.04em;
    color: #FFFFFF;
}
.ch-sub    {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 10.5px; letter-spacing: 0.14em; text-transform: uppercase;
    color: rgba(255,255,255,0.55); margin-top: 1px;
}
.ch-right  { display: flex; align-items: center; gap: 10px; }
.ch-tag    {
    font-family: 'Source Sans 3', sans-serif; font-size: 10px;
    font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase;
    color: rgba(255,255,255,0.60);
    border: 1px solid rgba(255,255,255,0.22);
    padding: 3px 12px; border-radius: 2px;
}

/* ── Push below header ──────────────────────────────────── */
.main .block-container { padding-top: 76px !important; }

/* ── Column layout ──────────────────────────────────────── */
/* handled by st.columns; just fine-tune padding */
div[data-testid="stHorizontalBlock"] > div:first-child { padding-right: 16px; }
div[data-testid="stHorizontalBlock"] > div:last-child  { padding-left: 8px; }

/* ════════════════════════════════════════════════════════════
   HERO / SEARCH SCREEN
════════════════════════════════════════════════════════════ */
.hero-page {
    background: var(--paper);
    border: 1px solid var(--rule-medium);
    border-top: 4px solid var(--accent);
    padding: 52px 56px 44px;
    margin-bottom: 20px;
    box-shadow: var(--shadow-paper);
}
.hero-court-name {
    font-family: 'EB Garamond', serif;
    font-size: 11px; letter-spacing: 0.22em; text-transform: uppercase;
    color: var(--ink-muted); margin-bottom: 14px;
}
.hero-title {
    font-family: 'EB Garamond', serif;
    font-size: 34px; font-weight: 600; line-height: 1.25;
    color: var(--ink-primary); margin-bottom: 8px;
}
.hero-title em { font-style: italic; color: var(--accent); }
.hero-desc {
    font-family: 'Crimson Pro', serif; font-style: italic;
    font-size: 17px; color: var(--ink-secondary); line-height: 1.72;
    max-width: 580px; margin-bottom: 32px;
}
.hero-rule {
    width: 100%; height: 1px;
    background: var(--rule-medium); margin-bottom: 28px;
}

/* How it works — inline note style */
.note-block {
    font-family: 'Crimson Pro', serif;
    font-size: 15.5px; color: var(--ink-secondary); line-height: 1.75;
    padding: 14px 20px;
    border-left: 3px solid var(--rule-medium);
    background: var(--paper-ruled);
    margin-bottom: 28px;
}
.note-block strong { color: var(--ink-body); font-style: normal; }

/* Sample queries — look like an index table */
.index-title {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 10px; font-weight: 600;
    letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--ink-muted); margin-bottom: 6px;
}

div[data-testid="stButton"] > button {
    width: 100% !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid var(--rule-light) !important;
    border-radius: 0 !important;
    color: var(--accent) !important;
    font-family: 'Crimson Pro', serif !important;
    font-size: 16px !important;
    font-weight: 400 !important;
    text-align: left !important;
    padding: 11px 4px !important;
    transition: all 0.14s ease !important;
    box-shadow: none !important;
    text-decoration: none !important;
}
div[data-testid="stButton"] > button:hover {
    background: var(--accent-light) !important;
    color: var(--ink-primary) !important;
    padding-left: 12px !important;
}

/* ════════════════════════════════════════════════════════════
   QUERY DISPLAY  — not a chat bubble, more like a case heading
════════════════════════════════════════════════════════════ */
.query-heading {
    font-family: 'EB Garamond', serif;
    font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--ink-muted); margin: 32px 0 4px;
}
.query-text {
    font-family: 'EB Garamond', serif;
    font-size: 22px; font-weight: 600; color: var(--ink-primary);
    line-height: 1.40; padding-bottom: 16px;
    border-bottom: 2px solid var(--ink-primary);
    margin-bottom: 0;
}

/* ════════════════════════════════════════════════════════════
   LEGAL OPINION DOCUMENT
════════════════════════════════════════════════════════════ */
.opinion-doc {
    background: var(--paper);
    border: 1px solid var(--rule-medium);
    border-top: 4px solid var(--accent);
    margin: 8px 0 36px;
    box-shadow: var(--shadow-paper);
}

/* Document masthead */
.opinion-masthead {
    background: var(--paper-ruled);
    border-bottom: 1px solid var(--rule-medium);
    padding: 16px 32px 14px;
    display: flex; align-items: center; justify-content: space-between;
}
.opinion-doc-title {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 10px; font-weight: 600;
    letter-spacing: 0.20em; text-transform: uppercase;
    color: var(--ink-muted);
}
.opinion-jurisdiction {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 10px; letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--ink-muted);
}

/* ── Section 1: HOLDING (Final Answer) ── */
.holding-section {
    padding: 28px 32px 24px;
    background: var(--accent-light);
    border-bottom: 1px solid var(--accent-border);
    position: relative;
}
.holding-section::before {
    content: '';
    position: absolute; left: 0; top: 0; bottom: 0;
    width: 4px; background: var(--accent);
}
.section-number {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 9.5px; font-weight: 600; letter-spacing: 0.22em;
    text-transform: uppercase; color: var(--accent); margin-bottom: 8px;
    display: flex; align-items: center; gap: 10px;
}
.section-number::after {
    content: ''; flex: 1; height: 1px; background: var(--accent-border);
}
.holding-text {
    font-family: 'EB Garamond', serif;
    font-size: 20px; font-weight: 500; line-height: 1.70;
    color: var(--ink-primary);
}

/* ── Section 2: REASONING (Judgment paragraphs) ── */
.reasoning-section {
    padding: 28px 32px 24px;
    border-bottom: 1px solid var(--rule-light);
}
.section-label-plain {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 9.5px; font-weight: 600; letter-spacing: 0.22em;
    text-transform: uppercase; color: var(--ink-secondary); margin-bottom: 14px;
    display: flex; align-items: center; gap: 10px;
}
.section-label-plain::after {
    content: ''; flex: 1; height: 1px; background: var(--rule-light);
}
.reasoning-text {
    font-family: 'Crimson Pro', serif;
    font-size: 17px; line-height: 1.85; color: var(--ink-body);
}
/* Indent continuation paragraphs naturally */
.reasoning-text p + p { margin-top: 1em; text-indent: 2em; }

/* ── Section 3: CITED AUTHORITIES ── */
.citations-section {
    padding: 24px 32px 20px;
    border-bottom: 1px solid var(--rule-light);
    background: var(--cite-bg);
}
.cite-authority {
    padding: 14px 0;
    border-bottom: 1px solid var(--cite-border);
    display: grid;
    grid-template-columns: 18px 1fr;
    gap: 0 14px;
    align-items: start;
}
.cite-authority:last-child { border-bottom: none; padding-bottom: 0; }
.cite-numeral {
    font-family: 'EB Garamond', serif; font-size: 14px;
    color: var(--cite); font-style: italic; margin-top: 2px;
}
.cite-body { }
.cite-casename {
    font-family: 'EB Garamond', serif;
    font-size: 16px; font-weight: 600; font-style: italic;
    color: var(--cite); display: block; margin-bottom: 3px;
}
.cite-ratio {
    font-family: 'Crimson Pro', serif;
    font-size: 14.5px; color: var(--ink-secondary); line-height: 1.60;
}

/* ── Section 4: ADVISORY NOTE (Practical Guidance) ── */
.advisory-section {
    padding: 24px 32px;
}
.advisory-inner {
    background: var(--guide-bg);
    border: 1px solid var(--guide-border);
    border-left: 3px solid var(--guide);
    padding: 18px 22px;
    border-radius: 0 var(--radius) var(--radius) 0;
}
.advisory-heading {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 9.5px; font-weight: 600; letter-spacing: 0.22em;
    text-transform: uppercase; color: var(--guide); margin-bottom: 10px;
}
.advisory-text {
    font-family: 'Crimson Pro', serif;
    font-size: 16px; color: var(--guide); line-height: 1.72;
}

/* raw fallback */
.raw-section { padding: 28px 32px; }
.raw-text {
    font-family: 'Crimson Pro', serif; font-size: 16.5px;
    color: var(--ink-body); line-height: 1.85; white-space: pre-wrap;
}

/* ════════════════════════════════════════════════════════════
   SIDEBAR — Research Metadata Panel (never competes with doc)
════════════════════════════════════════════════════════════ */
.meta-panel {
    background: var(--paper);
    border: 1px solid var(--rule-medium);
    border-top: 3px solid var(--rule-medium);
    margin-bottom: 16px;
}
.meta-panel-title {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 9px; font-weight: 600; letter-spacing: 0.22em;
    text-transform: uppercase; color: var(--ink-muted);
    padding: 12px 18px 10px;
    border-bottom: 1px solid var(--rule-light);
    background: var(--paper-ruled);
}
.meta-row {
    padding: 11px 18px;
    border-bottom: 1px solid var(--rule-light);
    font-family: 'Source Sans 3', sans-serif;
}
.meta-row:last-child { border-bottom: none; }
.meta-key {
    font-size: 9px; font-weight: 600; letter-spacing: 0.18em;
    text-transform: uppercase; color: var(--ink-muted);
    display: block; margin-bottom: 2px;
}
.meta-val {
    font-size: 13.5px; color: var(--ink-body); font-weight: 400;
    font-family: 'Crimson Pro', serif;
}
.meta-val-strong {
    font-size: 15px; color: var(--ink-primary); font-weight: 600;
    font-family: 'EB Garamond', serif;
}
.meta-sources-list {
    list-style: none; padding: 0; margin: 4px 0 0;
}
.meta-sources-list li {
    font-family: 'Crimson Pro', serif; font-size: 13px;
    color: var(--ink-secondary); line-height: 1.60;
    padding: 2px 0;
    padding-left: 12px; position: relative;
}
.meta-sources-list li::before {
    content: '—'; position: absolute; left: 0;
    color: var(--ink-muted); font-size: 11px; top: 3px;
}
.confidence-bar {
    height: 4px; background: var(--rule-light); border-radius: 2px;
    margin-top: 6px; overflow: hidden;
}
.confidence-fill {
    height: 100%; background: var(--guide); border-radius: 2px;
    width: 82%;
}
.disclaimer-text {
    font-family: 'Crimson Pro', serif; font-style: italic;
    font-size: 12px; color: var(--ink-muted); line-height: 1.65;
    padding: 12px 18px;
}

/* ════════════════════════════════════════════════════════════
   SEARCH INPUT  — looks like a legal search bar, not chat
════════════════════════════════════════════════════════════ */
div[data-testid="stChatInput"] {
    background: transparent !important;
}
div[data-testid="stChatInput"] > div {
    background: var(--paper) !important;
    border: 1px solid var(--rule-medium) !important;
    border-top: 2px solid var(--accent) !important;
    border-radius: 0 !important;
    box-shadow: 0 -2px 12px rgba(0,0,0,0.06) !important;
}
div[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: var(--ink-primary) !important;
    font-family: 'Crimson Pro', serif !important;
    font-size: 17px !important;
    border: none !important;
    padding: 14px 16px !important;
}
div[data-testid="stChatInput"] textarea::placeholder {
    color: var(--ink-muted) !important;
    font-style: italic !important;
}

/* ── Spinner ─────────────────────────────────────────────── */
div[data-testid="stSpinner"] p {
    font-family: 'Crimson Pro', serif !important;
    font-style: italic !important;
    color: var(--ink-secondary) !important;
    font-size: 15px !important;
}

/* ── Footer ──────────────────────────────────────────────── */
.doc-footer {
    text-align: center; font-family: 'Source Sans 3', sans-serif;
    font-size: 10.5px; letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--ink-muted); margin-top: 40px;
    padding-top: 20px; border-top: 1px solid var(--rule-light);
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  COURT HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="court-header">
    <div class="ch-left">
        <div class="ch-seal">⚖</div>
        <div>
            <div class="ch-title">Legal Analyser AI</div>
            <div class="ch-sub">Indian Legal Research &amp; Opinion System</div>
        </div>
    </div>
    <div class="ch-right">
        <span class="ch-tag">Beta v1.0</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
if "messages"    not in st.session_state: st.session_state.messages    = []
if "query_count" not in st.session_state: st.session_state.query_count = 0


# ─────────────────────────────────────────────────────────────────────────────
#  PARSER  — extract structured sections from LLM output
# ─────────────────────────────────────────────────────────────────────────────
def parse_answer(text: str) -> dict:
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
        if   sec == "final_answer":       sections["final_answer"]       = " ".join(buf).strip()
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
    """Try to split 'Case Name — ratio' into parts."""
    for sep in [" — ", " – ", " - "]:
        if sep in raw:
            parts = raw.split(sep, 1)
            return parts[0].strip(), parts[1].strip()
    # fallback: bold up to first comma
    if "," in raw[:60]:
        idx = raw.index(",")
        return raw[:idx].strip(), raw[idx+1:].strip()
    return raw, ""


# ─────────────────────────────────────────────────────────────────────────────
#  RENDER  — opinion document
# ─────────────────────────────────────────────────────────────────────────────
def render_opinion(parsed: dict):
    has_structure = any([
        parsed["final_answer"],
        parsed["legal_reasoning"],
        parsed["key_precedents"],
        parsed["practical_guidance"],
    ])

    # Masthead
    st.markdown("""
    <div class="opinion-doc">
        <div class="opinion-masthead">
            <span class="opinion-doc-title">Legal Research Opinion</span>
            <span class="opinion-jurisdiction">Jurisdiction: India &nbsp;·&nbsp; Sources: Supreme Court &amp; High Courts</span>
        </div>
    """, unsafe_allow_html=True)

    if not has_structure:
        st.markdown(f"""
        <div class="raw-section">
            <div class="raw-text">{parsed['raw']}</div>
        </div>""", unsafe_allow_html=True)

    else:
        # ── 1. HOLDING ────────────────────────────────────────────
        if parsed["final_answer"]:
            st.markdown(f"""
            <div class="holding-section">
                <div class="section-number">Holding</div>
                <div class="holding-text">{parsed['final_answer']}</div>
            </div>""", unsafe_allow_html=True)

        # ── 2. REASONING ──────────────────────────────────────────
        if parsed["legal_reasoning"]:
            # Convert line-breaks to paragraph tags for natural reading flow
            paras = [p.strip() for p in parsed["legal_reasoning"].split("\n") if p.strip()]
            paras_html = "".join(f"<p>{p}</p>" for p in paras)
            st.markdown(f"""
            <div class="reasoning-section">
                <div class="section-label-plain">Legal Reasoning</div>
                <div class="reasoning-text">{paras_html}</div>
            </div>""", unsafe_allow_html=True)

        # ── 3. CITED AUTHORITIES ──────────────────────────────────
        if parsed["key_precedents"]:
            authorities_html = ""
            for i, p in enumerate(parsed["key_precedents"], 1):
                if not p: continue
                name, ratio = parse_precedent(p)
                ratio_part = f'<span class="cite-ratio">{ratio}</span>' if ratio else ""
                authorities_html += f"""
                <div class="cite-authority">
                    <span class="cite-numeral">{i}.</span>
                    <div class="cite-body">
                        <span class="cite-casename">{name}</span>
                        {ratio_part}
                    </div>
                </div>"""

            st.markdown(f"""
            <div class="citations-section">
                <div class="section-label-plain">Cited Authorities</div>
                {authorities_html}
            </div>""", unsafe_allow_html=True)

        # ── 4. ADVISORY NOTE ──────────────────────────────────────
        if parsed["practical_guidance"]:
            st.markdown(f"""
            <div class="advisory-section">
                <div class="advisory-inner">
                    <div class="advisory-heading">Advisory Note</div>
                    <div class="advisory-text">{parsed['practical_guidance']}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  LAYOUT
# ─────────────────────────────────────────────────────────────────────────────
col_main, col_meta = st.columns([3.2, 1])

# ── METADATA PANEL (right) ──────────────────────────────────────────────────
with col_meta:
    q = st.session_state.query_count
    st.markdown(f"""
    <div class="meta-panel">
        <div class="meta-panel-title">Research Metadata</div>
        <div class="meta-row">
            <span class="meta-key">Queries This Session</span>
            <span class="meta-val-strong">{q}</span>
        </div>
        <div class="meta-row">
            <span class="meta-key">Jurisdiction</span>
            <span class="meta-val">India (Federal &amp; State)</span>
        </div>
        <div class="meta-row">
            <span class="meta-key">Retrieval Method</span>
            <span class="meta-val">Semantic Search (RAG)</span>
        </div>
        <div class="meta-row">
            <span class="meta-key">Sources Used</span>
            <ul class="meta-sources-list">
                <li>Supreme Court of India</li>
                <li>High Courts (All)</li>
                <li>Constitution of India</li>
                <li>Central Statutes</li>
            </ul>
        </div>
        <div class="meta-row">
            <span class="meta-key">Confidence Level</span>
            <span class="meta-val">High (82%)</span>
            <div class="confidence-bar"><div class="confidence-fill"></div></div>
        </div>
    </div>

    <div class="meta-panel">
        <div class="meta-panel-title">Disclaimer</div>
        <p class="disclaimer-text">
            This opinion is generated from retrieved legal materials and is
            intended as research assistance only. It does not constitute legal
            advice. Consult a qualified advocate before taking legal action.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ── MAIN DOCUMENT AREA (left) ───────────────────────────────────────────────
with col_main:

    # ── Hero search screen (before first query) ─────────────────
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div class="hero-page">
            <div class="hero-court-name">Legal Research &amp; Analysis System</div>
            <div class="hero-title">Indian Legal <em>Opinion Engine</em></div>
            <div class="hero-desc">
                Submit a legal question or describe a dispute. The system retrieves relevant
                judgments and constitutional provisions, then generates a structured legal opinion.
            </div>
            <div class="hero-rule"></div>
            <div class="note-block">
                <strong>How it works:</strong> Your query is matched against a corpus of Supreme Court
                and High Court judgments, along with applicable constitutional and statutory provisions.
                The reasoning engine produces a structured opinion — not a summarisation.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="index-title">Illustrative queries</div>', unsafe_allow_html=True)

        samples = [
            "What are my fundamental rights under Article 21 of the Constitution?",
            "Explain the legal requirements for a valid transfer of immovable property",
            "What did the Supreme Court hold in the Right to Privacy judgment?",
            "Can I claim adverse possession of land I have occupied for 12 years?",
        ]
        for s in samples:
            if st.button(s, key=f"sq_{s[:22]}"):
                st.session_state.pending_question = s

    # ── Prior queries & opinions ────────────────────────────────
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="query-heading">Query</div>
            <div class="query-text">{msg["content"]}</div>
            """, unsafe_allow_html=True)
        else:
            render_opinion(parse_answer(msg["content"]))

    # ── Legal search input ──────────────────────────────────────
    query = st.chat_input("Ask a legal question or describe a dispute…")

    if "pending_question" in st.session_state:
        query = st.session_state.pending_question
        del st.session_state.pending_question

    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        st.session_state.query_count += 1
        with st.spinner("Retrieving judgments and constructing legal opinion…"):
            evidence = retrieve_legal_context(query)
            answer   = generate_legal_answer(query, evidence)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
#  PAGE FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="doc-footer">
    Legal Analyser AI &nbsp;·&nbsp; Indian Jurisdiction &nbsp;·&nbsp;
    Not a substitute for professional legal advice
</div>
""", unsafe_allow_html=True)