import streamlit as st
import re

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="Gavel — AI Legal Intelligence",
    page_icon="🔨",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=DM+Mono:wght@400;500&display=swap');

/* ═══════════════════════════════════════
   DESIGN TOKENS
═══════════════════════════════════════ */
:root {
  --ink:         #1A1814;
  --ink-60:      #5C5750;
  --ink-40:      #8C847C;
  --ink-20:      #C4BDB6;
  --parchment:   #FAF8F4;
  --cream:       #F4F1EB;
  --cream-2:     #EDE8DF;

  --gold:        #C9923A;
  --gold-light:  #FDF5E8;
  --gold-mid:    rgba(201,146,58,0.15);
  --gold-glow:   rgba(201,146,58,0.08);

  --crimson:     #B03A2E;
  --crimson-light: #FDF1EF;
  --crimson-mid: rgba(176,58,46,0.12);

  --forest:      #2D6A4F;
  --forest-light:#EAF4EE;

  --navy:        #1E3A5F;
  --navy-light:  #EEF2F8;
  --navy-mid:    rgba(30,58,95,0.12);

  --border:      rgba(26,24,20,0.08);
  --border-mid:  rgba(26,24,20,0.14);
  --border-strong: rgba(26,24,20,0.20);

  --r-sm:  5px;
  --r-md:  10px;
  --r-lg:  16px;
  --r-xl:  22px;
  --r-full: 999px;

  --shadow-sm:  0 1px 3px rgba(26,24,20,0.06), 0 1px 2px rgba(26,24,20,0.04);
  --shadow-md:  0 4px 16px rgba(26,24,20,0.08), 0 2px 6px rgba(26,24,20,0.04);
  --shadow-lg:  0 12px 40px rgba(26,24,20,0.10), 0 4px 12px rgba(26,24,20,0.05);
  --ease-out:   cubic-bezier(0.16, 1, 0.3, 1);
}

/* ═══════════════════════════════════════
   GLOBAL
═══════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; }

html, body, .stApp {
  background: var(--parchment) !important;
  font-family: 'DM Sans', sans-serif;
  color: var(--ink);
  -webkit-font-smoothing: antialiased;
}

.block-container {
  padding-top: 0 !important;
  padding-bottom: 5rem !important;
  max-width: 860px !important;
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 99px; }

.stMarkdown, .stMarkdown > div,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] > div {
  display: block !important;
  width: 100% !important;
  white-space: normal !important;
  word-break: break-word !important;
  overflow-wrap: break-word !important;
}

/* Hide Streamlit's native top header/toolbar */
header[data-testid="stHeader"] {
  display: none !important;
}

/* ═══════════════════════════════════════
   TOPBAR
═══════════════════════════════════════ */
.topbar {
  background: #FFFFFF;
  border-bottom: 1px solid var(--border);
  padding: 0 2.5rem;
  height: 62px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 200;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 38px; height: 38px;
  background: var(--ink);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 19px;
  flex-shrink: 0;
  box-shadow: 0 2px 12px rgba(26,24,20,0.25);
  color: var(--gold);
}

.logo-wordmark {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  font-weight: 700;
  color: var(--ink);
  letter-spacing: -0.5px;
}

.logo-wordmark em {
  font-style: italic;
  color: var(--gold);
}

.topbar-chips {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--forest-light);
  border: 1px solid rgba(45,106,79,0.2);
  border-radius: var(--r-full);
  padding: 5px 13px;
  font-size: 12px;
  font-weight: 500;
  color: var(--forest);
}

.status-chip::before {
  content: '';
  width: 6px; height: 6px;
  background: var(--forest);
  border-radius: 50%;
  animation: pulse-live 2.2s infinite;
}

@keyframes pulse-live {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.8); }
}

.version-chip {
  background: var(--cream);
  border: 1px solid var(--border);
  border-radius: var(--r-full);
  padding: 5px 12px;
  font-size: 12px;
  font-weight: 500;
  color: var(--ink-40);
  font-family: 'DM Mono', monospace;
}

/* ═══════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════ */
[data-testid="stSidebar"] {
  background: var(--cream) !important;
  border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] .block-container {
  max-width: none !important;
  padding: 1.75rem 1.25rem !important;
}

.sb-section-label {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 1.8px;
  text-transform: uppercase;
  color: var(--ink-20);
  margin-bottom: 10px;
  margin-top: 1.5rem;
}

.stat-card {
  background: var(--ink);
  border-radius: var(--r-lg);
  padding: 20px;
  margin-bottom: 12px;
  position: relative;
  overflow: hidden;
}

.stat-card::after {
  content: '⚖';
  position: absolute;
  right: 14px; bottom: 8px;
  font-size: 48px;
  opacity: 0.06;
}

.stat-num {
  font-family: 'Playfair Display', serif;
  font-size: 48px;
  color: var(--gold);
  line-height: 1;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 12px;
  font-weight: 400;
  color: rgba(255,255,255,0.45);
  letter-spacing: 0.3px;
}

.kb-list {
  background: white;
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  overflow: hidden;
  margin-bottom: 12px;
}

.kb-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px 15px;
  border-bottom: 1px solid var(--border);
  font-size: 13px;
  color: var(--ink-60);
  font-weight: 400;
}

.kb-item:last-child { border-bottom: none; }

.kb-ico {
  width: 28px; height: 28px;
  border-radius: 7px;
  background: var(--cream);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
}

div[data-testid="stButton"] > button {
  width: 100% !important;
  background: white !important;
  border: 1px solid var(--border-mid) !important;
  color: var(--ink-60) !important;
  border-radius: var(--r-md) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 500 !important;
  font-size: 13px !important;
  padding: 10px 16px !important;
  transition: all 0.18s ease !important;
  box-shadow: var(--shadow-sm) !important;
}

div[data-testid="stButton"] > button:hover {
  background: var(--cream) !important;
  border-color: var(--border-strong) !important;
  color: var(--ink) !important;
}

/* ═══════════════════════════════════════
   HERO
═══════════════════════════════════════ */
@keyframes fade-up {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: translateY(0); }
}

.hero {
  padding: 5rem 0 3.5rem;
  text-align: center;
  animation: fade-up 0.65s var(--ease-out) both;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--gold-light);
  border: 1px solid rgba(201,146,58,0.25);
  border-radius: var(--r-full);
  padding: 6px 16px;
  font-size: 11.5px;
  font-weight: 600;
  color: var(--gold);
  letter-spacing: 0.8px;
  text-transform: uppercase;
  box-shadow: var(--shadow-sm);
  margin-bottom: 2rem;
}

.hero-h1 {
  font-family: 'Playfair Display', serif;
  font-size: clamp(42px, 6vw, 62px);
  font-weight: 700;
  line-height: 1.10;
  color: var(--ink);
  letter-spacing: -1.5px;
  margin-bottom: 1.25rem;
}

.hero-h1 i {
  color: var(--gold);
  font-style: italic;
}

.hero-sub {
  font-size: 17px;
  color: var(--ink-40);
  max-width: 500px;
  margin: 0 auto 2.75rem;
  line-height: 1.7;
  font-weight: 300;
}

.samples-label {
  font-size: 10.5px;
  font-weight: 600;
  letter-spacing: 1.8px;
  text-transform: uppercase;
  color: var(--ink-20);
  text-align: center;
  margin-bottom: 12px;
}

div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button {
  background: white !important;
  border: 1px solid var(--border-mid) !important;
  color: var(--ink-60) !important;
  text-align: left !important;
  border-radius: var(--r-lg) !important;
  padding: 16px 18px !important;
  font-size: 13.5px !important;
  font-weight: 400 !important;
  line-height: 1.5 !important;
  height: auto !important;
  box-shadow: var(--shadow-sm) !important;
  transition: all 0.2s var(--ease-out) !important;
}

div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button:hover {
  border-color: var(--gold) !important;
  color: var(--gold) !important;
  background: var(--gold-light) !important;
  box-shadow: 0 0 0 3px var(--gold-mid), var(--shadow-md) !important;
  transform: translateY(-1px) !important;
}

/* ═══════════════════════════════════════
   USER MESSAGE
═══════════════════════════════════════ */
@keyframes bubble-in {
  from { opacity: 0; transform: translateY(10px) scale(0.98); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}

.msg-user-wrap {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  margin-bottom: 1.5rem;
  animation: bubble-in 0.35s var(--ease-out) both;
}

.msg-user-label {
  font-size: 10.5px;
  font-weight: 600;
  letter-spacing: 1px;
  color: var(--ink-20);
  margin-bottom: 6px;
  text-transform: uppercase;
}

.msg-user-bubble {
  background: var(--ink);
  color: #FAF8F4;
  padding: 14px 20px;
  border-radius: 20px 20px 4px 20px;
  max-width: 72%;
  font-size: 15px;
  font-weight: 400;
  line-height: 1.6;
  box-shadow: 0 4px 20px rgba(26,24,20,0.20);
}

/* ═══════════════════════════════════════
   RESPONSE CARD
═══════════════════════════════════════ */
.res-card {
  background: white;
  border: 1px solid var(--border);
  border-radius: var(--r-xl);
  overflow: hidden;
  margin-bottom: 2.5rem;
  box-shadow: var(--shadow-lg);
  animation: bubble-in 0.45s var(--ease-out) both;
  position: relative;
}

.res-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--gold), var(--crimson), var(--navy));
}

.res-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 24px 16px;
  border-bottom: 1px solid var(--border);
}

.res-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.res-gavel {
  width: 38px; height: 38px;
  background: var(--gold);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 2px 10px rgba(201,146,58,0.30);
}

.res-title {
  font-family: 'Playfair Display', serif;
  font-size: 15px;
  font-weight: 600;
  color: var(--ink);
  letter-spacing: -0.2px;
}

.res-subtitle {
  font-size: 12px;
  color: var(--ink-40);
  font-weight: 400;
}

.verified-badge {
  display: flex;
  align-items: center;
  gap: 5px;
  background: var(--forest-light);
  border: 1px solid rgba(45,106,79,0.2);
  border-radius: var(--r-full);
  padding: 4px 11px;
  font-size: 11px;
  font-weight: 600;
  color: var(--forest);
}

.res-body {
  padding: 26px 28px;
}

/* ── Section Headers ── */
.sec-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
  margin-top: 24px;
}

.sec-header:first-child { margin-top: 0; }

.sec-icon {
  width: 30px; height: 30px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
}

.sec-icon-gold { background: var(--gold-light); }
.sec-icon-navy { background: var(--navy-light); }
.sec-icon-crimson { background: var(--crimson-light); }
.sec-icon-forest { background: var(--forest-light); }

.sec-title {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.4px;
  text-transform: uppercase;
}

.sec-title-gold  { color: var(--gold); }
.sec-title-navy  { color: var(--navy); }
.sec-title-crimson { color: var(--crimson); }
.sec-title-forest  { color: var(--forest); }

.sec-divider {
  height: 1px;
  background: var(--border);
  margin: 22px 0;
}

/* ── Final Answer ── */
.final-answer-text {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  line-height: 1.70;
  color: var(--ink);
  font-style: italic;
}

/* ── Legal Reasoning ── */
.reasoning-block {
  background: var(--navy-light);
  border: 1px solid rgba(30,58,95,0.12);
  border-left: 3px solid var(--navy);
  border-radius: var(--r-md);
  padding: 16px 18px;
  margin-bottom: 8px;
}

.reasoning-text {
  font-size: 14.5px;
  line-height: 1.72;
  color: var(--navy);
  font-weight: 400;
}

.reasoning-point {
  display: grid;
  grid-template-columns: 14px 1fr;
  gap: 8px;
  align-items: baseline;
  padding: 9px 0;
  border-bottom: 1px solid rgba(30,58,95,0.08);
  font-size: 14.5px;
  line-height: 1.65;
  color: var(--ink-60);
}

.reasoning-point:last-child { border-bottom: none; padding-bottom: 0; }

.reasoning-bullet {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--navy);
  flex-shrink: 0;
  display: inline-block;
  margin-top: 0.45em;
  justify-self: center;
}

/* ── Precedents ── */
.prec-card {
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  overflow: hidden;
  margin-bottom: 10px;
  transition: box-shadow 0.2s ease, transform 0.15s ease;
}

.prec-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.prec-top {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: var(--cream);
  border-bottom: 1px solid var(--border);
}

.prec-num-badge {
  font-family: 'DM Mono', monospace;
  font-size: 10px;
  font-weight: 500;
  color: var(--gold);
  background: var(--gold-light);
  border: 1px solid rgba(201,146,58,0.25);
  border-radius: 5px;
  padding: 2px 8px;
  flex-shrink: 0;
  letter-spacing: 0.5px;
}

.prec-case {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 600;
  color: var(--ink);
}

.prec-court {
  font-size: 11px;
  color: var(--ink-40);
  font-weight: 400;
  margin-left: auto;
  font-family: 'DM Mono', monospace;
}

.prec-body {
  padding: 13px 16px;
  background: white;
}

.prec-principle {
  font-family: 'Playfair Display', serif;
  font-size: 14.5px;
  line-height: 1.65;
  color: var(--ink-60);
  font-style: italic;
  margin-bottom: 6px;
}

.prec-relevance {
  font-size: 13px;
  color: var(--ink-40);
  line-height: 1.55;
}

/* ── Statutes ── */
.statute-item {
  display: flex;
  gap: 14px;
  padding: 13px 0;
  border-bottom: 1px solid var(--border);
  align-items: flex-start;
}

.statute-item:last-child { border-bottom: none; }

.statute-tag {
  font-family: 'DM Mono', monospace;
  font-size: 10.5px;
  font-weight: 500;
  color: var(--crimson);
  background: var(--crimson-light);
  border: 1px solid rgba(176,58,46,0.2);
  border-radius: 5px;
  padding: 3px 9px;
  flex-shrink: 0;
  white-space: nowrap;
  margin-top: 2px;
}

.statute-text {
  font-size: 14px;
  line-height: 1.65;
  color: var(--ink-60);
}

/* ── Judicial Outcome ── */
.outcome-card {
  background: linear-gradient(135deg, var(--gold-light), #FEF9EC);
  border: 1px solid rgba(201,146,58,0.22);
  border-radius: var(--r-lg);
  padding: 18px 22px;
}

.outcome-text {
  font-size: 15px;
  line-height: 1.70;
  color: #6B4C10;
  font-weight: 400;
}

/* ── Practical Guidance ── */
.practical-card {
  background: linear-gradient(135deg, var(--forest-light), #E6F4ED);
  border: 1px solid rgba(45,106,79,0.2);
  border-radius: var(--r-lg);
  padding: 20px 22px;
}

.practical-item {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  font-size: 14.5px;
  line-height: 1.65;
  color: #1A4032;
  padding: 7px 0;
  border-bottom: 1px solid rgba(45,106,79,0.1);
}

.practical-item:last-child { border-bottom: none; }

.practical-arrow {
  color: var(--forest);
  font-weight: 700;
  flex-shrink: 0;
  margin-top: 1px;
}

/* ── Plain text fallback ── */
.plain-text {
  font-size: 15px;
  line-height: 1.72;
  color: var(--ink-60);
  font-weight: 300;
}

/* ── Disclaimer strip ── */
.disclaimer {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--cream);
  border-top: 1px solid var(--border);
  padding: 12px 22px;
  font-size: 11.5px;
  color: var(--ink-40);
}

/* ═══════════════════════════════════════
   CHAT INPUT AREA
═══════════════════════════════════════ */

/* Kill the black bottom bar Streamlit adds */
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
.stChatFloatingInputContainer,
.stChatFloatingInputContainer > div {
  background: var(--parchment) !important;
  border-top: 1px solid var(--border) !important;
  box-shadow: none !important;
}

[data-testid="stChatInput"] textarea {
  font-family: 'DM Sans', sans-serif !important;
  font-size: 15px !important;
  color: var(--ink) !important;
  background: white !important;
  border-radius: var(--r-xl) !important;
  border: 1.5px solid var(--border-mid) !important;
  box-shadow: var(--shadow-md) !important;
  padding: 16px 20px !important;
}

[data-testid="stChatInput"] textarea:focus {
  border-color: var(--gold) !important;
  box-shadow: var(--shadow-md), 0 0 0 4px var(--gold-glow) !important;
  outline: none !important;
}

/* Send button */
[data-testid="stChatInput"] button {
  background: var(--gold) !important;
  border-radius: 50% !important;
  border: none !important;
  color: white !important;
}

[data-testid="stSpinner"] p {
  color: var(--gold) !important;
  font-weight: 500 !important;
  font-family: 'DM Sans', sans-serif !important;
}

/* ═══════════════════════════════════════
   FOOTER
═══════════════════════════════════════ */
.footer {
  text-align: center;
  padding: 2.5rem 1rem;
  margin-top: 2rem;
  border-top: 1px solid var(--border);
}

.footer-logo {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 8px;
}

.footer-logo em { font-style: italic; color: var(--gold); }

.footer-note {
  font-size: 12px;
  color: var(--ink-40);
  max-width: 460px;
  margin: 0 auto;
  line-height: 1.65;
}

.footer-tags {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 14px;
  flex-wrap: wrap;
}

.footer-tag {
  font-size: 11px;
  font-weight: 500;
  color: var(--ink-40);
  background: var(--cream);
  border: 1px solid var(--border);
  border-radius: var(--r-full);
  padding: 3px 11px;
  font-family: 'DM Mono', monospace;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════
# ROBUST PARSER — matches the 6-section prompt output
# ═══════════════════════════════════════
def parse_legal_response(raw: str) -> dict:
    """
    Parse the 6-section structured output from the LLM prompt:
    1️⃣ FINAL ANSWER
    2️⃣ LEGAL REASONING
    3️⃣ KEY PRECEDENTS
    4️⃣ RELEVANT STATUTORY / CONSTITUTIONAL PROVISIONS
    5️⃣ EXPECTED JUDICIAL OUTCOME
    6️⃣ PRACTICAL GUIDANCE
    """
    sections = {
        "final_answer": "",
        "legal_reasoning": [],
        "precedents": [],
        "statutes": [],
        "outcome": "",
        "practical": [],
    }

    # Section header patterns — robust to emoji/number variations
    PATTERNS = {
        "final_answer":    re.compile(r"(?:1[️⃣]?\s*)?FINAL\s+ANSWER", re.I),
        "legal_reasoning": re.compile(r"(?:2[️⃣]?\s*)?LEGAL\s+REASONING", re.I),
        "precedents":      re.compile(r"(?:3[️⃣]?\s*)?KEY\s+PRECEDENTS", re.I),
        "statutes":        re.compile(r"(?:4[️⃣]?\s*)?RELEVANT\s+STATUTORY", re.I),
        "outcome":         re.compile(r"(?:5[️⃣]?\s*)?EXPECTED\s+JUDICIAL", re.I),
        "practical":       re.compile(r"(?:6[️⃣]?\s*)?PRACTICAL\s+GUIDANCE", re.I),
    }

    current = None
    buffer = []

    def flush(key, buf):
        text = "\n".join(buf).strip()
        if not text:
            return
        if key == "final_answer":
            sections["final_answer"] = text
        elif key == "outcome":
            sections["outcome"] = text
        elif key == "legal_reasoning":
            # Split into bullet points
            points = []
            for line in buf:
                s = line.strip().lstrip("-•*·▪▸➤→").strip()
                if s:
                    points.append(s)
            if points:
                sections["legal_reasoning"] = points
        elif key == "precedents":
            sections["precedents"] = parse_precedents(buf)
        elif key == "statutes":
            sections["statutes"] = parse_statutes(buf)
        elif key == "practical":
            points = []
            for line in buf:
                s = line.strip().lstrip("-•*·▪▸➤→1234567890. ").strip()
                if s:
                    points.append(s)
            if points:
                sections["practical"] = points

    lines = raw.split("\n")
    for line in lines:
        stripped = line.strip()
        matched = False
        for key, pat in PATTERNS.items():
            if pat.search(stripped) and len(stripped) < 80:
                # Flush previous buffer
                if current:
                    flush(current, buffer)
                current = key
                buffer = []
                matched = True
                break
        if not matched and current is not None:
            buffer.append(line)

    # Flush last section
    if current:
        flush(current, buffer)

    # Fallback: if nothing parsed, dump raw into final_answer
    if not any([sections["final_answer"], sections["legal_reasoning"],
                sections["precedents"], sections["statutes"]]):
        sections["final_answer"] = raw

    return sections


def parse_precedents(lines: list) -> list:
    """Parse precedent blocks into structured dicts."""
    precedents = []
    current = {}
    i = 0
    raw_lines = [l.strip() for l in lines if l.strip()]

    while i < len(raw_lines):
        line = raw_lines[i]
        # Numbered item start: "1. Case Name" or "1) Case Name" or bold **Case**
        num_match = re.match(r'^(\d+)[.)]\s+(.+)', line)
        bold_match = re.match(r'^\*\*(.+?)\*\*', line)

        if num_match or bold_match:
            if current:
                precedents.append(current)
            name_raw = num_match.group(2) if num_match else bold_match.group(1)
            # Strip court info in parens
            court_match = re.search(r'\(([^)]+)\)\s*$', name_raw)
            court = court_match.group(1) if court_match else ""
            name = re.sub(r'\s*\([^)]+\)\s*$', '', name_raw).strip("*_ ")
            current = {"case": name, "court": court, "principle": "", "relevance": ""}
        elif line.lower().startswith("legal principle") or line.lower().startswith("principle"):
            val = re.sub(r'^[^:]+:\s*', '', line)
            if not val:
                i += 1
                if i < len(raw_lines):
                    val = raw_lines[i]
            if current:
                current["principle"] = val.strip("*_ ")
        elif line.lower().startswith("why it applies") or line.lower().startswith("relevance"):
            val = re.sub(r'^[^:]+:\s*', '', line)
            if not val:
                i += 1
                if i < len(raw_lines):
                    val = raw_lines[i]
            if current:
                current["relevance"] = val.strip("*_ ")
        elif current:
            # Continuation lines — assign to principle if empty, else relevance
            if not current["principle"]:
                current["principle"] = line.strip("*_- ")
            elif not current["relevance"]:
                current["relevance"] = line.strip("*_- ")
        i += 1

    if current:
        precedents.append(current)

    return precedents


def parse_statutes(lines: list) -> list:
    """Parse statute blocks into structured dicts."""
    statutes = []
    current = {}
    raw_lines = [l.strip() for l in lines if l.strip()]
    i = 0

    while i < len(raw_lines):
        line = raw_lines[i]
        num_match = re.match(r'^(\d+)[.)]\s+(.+)', line)
        sec_match = re.match(r'^(?:Section|Article|Art\.|Sec\.)\s+[\d\w]+', line, re.I)

        if num_match:
            if current:
                statutes.append(current)
            rest = num_match.group(2)
            current = {"ref": rest, "provides": "", "relevance": ""}
        elif sec_match:
            if current:
                statutes.append(current)
            current = {"ref": line.strip("*_ "), "provides": "", "relevance": ""}
        elif re.match(r'^what it provides', line, re.I):
            val = re.sub(r'^[^:]+:\s*', '', line)
            if not val:
                i += 1
                if i < len(raw_lines):
                    val = raw_lines[i]
            if current:
                current["provides"] = val.strip()
        elif re.match(r'^why relevant|^relevance|^scope', line, re.I):
            val = re.sub(r'^[^:]+:\s*', '', line)
            if not val:
                i += 1
                if i < len(raw_lines):
                    val = raw_lines[i]
            if current:
                current["relevance"] = val.strip()
        elif current:
            if not current["provides"]:
                current["provides"] = line.strip("*_- ")
            elif not current["relevance"]:
                current["relevance"] = line.strip("*_- ")
        i += 1

    if current:
        statutes.append(current)

    return statutes


# ═══════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════
if "messages" not in st.session_state:
    st.session_state.messages = []
if "query_count" not in st.session_state:
    st.session_state.query_count = 0
if "scroll_top" not in st.session_state:
    st.session_state.scroll_top = False


# Scroll to top after new response loads
if st.session_state.scroll_top:
    st.session_state.scroll_top = False
    st.components.v1.html("""
    <script>
      window.parent.document.querySelector('section[data-testid="stMain"]').scrollTo({top: 0, behavior: 'smooth'});
    </script>
    """, height=0)

# ═══════════════════════════════════════
# TOPBAR
# ═══════════════════════════════════════
st.markdown("""
<div class="topbar">
  <div class="logo">
    <div class="logo-icon">🔨</div>
    <div class="logo-wordmark">Gavel <em>AI</em></div>
  </div>
  <div class="topbar-chips">
    <div class="status-chip">Live · SC Corpus</div>
    <div class="version-chip">v2.0</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; padding: 0.25rem 0 1.25rem; border-bottom:1px solid rgba(26,24,20,0.08); margin-bottom:1.25rem;">
      <div style="width:40px; height:40px; background:#C9923A; border-radius:10px;
           display:flex; align-items:center; justify-content:center; font-size:20px;
           box-shadow:0 2px 10px rgba(201,146,58,0.30); flex-shrink:0;">🔨</div>
      <div>
        <div style="font-family:'Playfair Display',serif; font-size:24px; font-weight:700;
             color:#1A1814; letter-spacing:-0.5px; line-height:1.1;">Gavel <em style="font-style:italic; color:#C9923A;">AI</em></div>
        <div style="font-size:11px; color:#8C847C; font-weight:500; letter-spacing:0.4px; margin-top:1px;">Indian Legal Intelligence</div>
      </div>
    </div>
    <div style="font-family:'Playfair Display',serif; font-size:20px; font-weight:700;
         color:#1A1814; letter-spacing:-0.5px; margin-bottom:4px;">
      Session
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stat-card">
      <div class="stat-num">{st.session_state.query_count:02d}</div>
      <div class="stat-label">Queries this session</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-section-label">Knowledge Base</div>', unsafe_allow_html=True)

    kb = [
        ("📜", "Constitution of India"),
        ("🏛", "SC Judgments 1950–2025"),
        ("⚖", "High Court Precedents"),
        ("📋", "IPC, CrPC & BNS"),
        ("📑", "Civil Procedure Code"),
        ("🔖", "Arbitration & Contracts"),
    ]
    kb_html = '<div class="kb-list">'
    for icon, name in kb:
        kb_html += f'<div class="kb-item"><div class="kb-ico">{icon}</div>{name}</div>'
    kb_html += '</div>'
    st.markdown(kb_html, unsafe_allow_html=True)

    st.markdown('<div class="sb-section-label">Actions</div>', unsafe_allow_html=True)
    if st.button("↺  Clear Session"):
        st.session_state.messages = []
        st.session_state.query_count = 0
        st.rerun()


# ═══════════════════════════════════════
# RESPONSE RENDERER
# ═══════════════════════════════════════
def render_response(raw: str):
    s = parse_legal_response(raw)

    st.markdown("""
    <div class="res-card">
      <div class="res-header">
        <div class="res-header-left">
          <div class="res-gavel">🔨</div>
          <div>
            <div class="res-title">Gavel AI</div>
            <div class="res-subtitle">Indian Legal Intelligence</div>
          </div>
        </div>
        <div class="verified-badge">✓ Verified Corpus</div>
      </div>
      <div class="res-body">
    """, unsafe_allow_html=True)

    # ── 1. Final Answer ──
    if s["final_answer"]:
        st.markdown("""
        <div class="sec-header">
          <div class="sec-icon sec-icon-gold">📋</div>
          <span class="sec-title sec-title-gold">Final Answer</span>
        </div>
        """, unsafe_allow_html=True)
        clean = s["final_answer"].replace("**", "").replace("*", "")
        st.markdown(f'<div class="final-answer-text">{clean}</div>', unsafe_allow_html=True)

    # ── 2. Legal Reasoning ──
    if s["legal_reasoning"]:
        st.markdown('<div class="sec-divider"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="sec-header">
          <div class="sec-icon sec-icon-navy">⚖</div>
          <span class="sec-title sec-title-navy">Legal Reasoning</span>
        </div>
        """, unsafe_allow_html=True)
        points_html = ""
        for pt in s["legal_reasoning"]:
            clean = pt.replace("**", "").replace("*", "")
            points_html += f"""<div class="reasoning-point"><div class="reasoning-bullet"></div><div>{clean}</div></div>"""
        st.markdown(f'<div class="reasoning-block">{points_html}</div>', unsafe_allow_html=True)

    # ── 3. Key Precedents ──
    if s["precedents"]:
        st.markdown('<div class="sec-divider"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="sec-header">
          <div class="sec-icon sec-icon-crimson">🏛</div>
          <span class="sec-title sec-title-crimson">Key Precedents</span>
        </div>
        """, unsafe_allow_html=True)
        for idx, p in enumerate(s["precedents"]):
            case = p.get("case", "").replace("**", "").replace("*", "")
            court = p.get("court", "")
            principle = p.get("principle", "").replace("**", "").replace("*", "")
            relevance = p.get("relevance", "").replace("**", "").replace("*", "")

            court_html = f'<div class="prec-court">{court}</div>' if court else ""
            principle_html = f'<div class="prec-principle">{principle}</div>' if principle else ""
            relevance_html = f'<div class="prec-relevance">{relevance}</div>' if relevance else ""

            st.markdown(f"""
            <div class="prec-card">
              <div class="prec-top">
                <div class="prec-num-badge">#{idx+1:02d}</div>
                <div class="prec-case">{case if case else f'Precedent {idx+1}'}</div>
                {court_html}
              </div>
              <div class="prec-body">
                {principle_html}
                {relevance_html}
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── 4. Statutes ──
    if s["statutes"]:
        st.markdown('<div class="sec-divider"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="sec-header">
          <div class="sec-icon sec-icon-crimson">📜</div>
          <span class="sec-title sec-title-crimson">Statutory & Constitutional Provisions</span>
        </div>
        """, unsafe_allow_html=True)
        for stat in s["statutes"]:
            ref = stat.get("ref", "").replace("**", "").replace("*", "")
            provides = stat.get("provides", "").replace("**", "").replace("*", "")
            relevance = stat.get("relevance", "").replace("**", "").replace("*", "")
            body = " — ".join(filter(None, [provides, relevance]))
            st.markdown(f"""
            <div class="statute-item">
              <div class="statute-tag">{ref}</div>
              <div class="statute-text">{body}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── 5. Judicial Outcome ──
    if s["outcome"]:
        st.markdown('<div class="sec-divider"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="sec-header">
          <div class="sec-icon sec-icon-gold">⚖</div>
          <span class="sec-title sec-title-gold">Expected Judicial Outcome</span>
        </div>
        """, unsafe_allow_html=True)
        clean = s["outcome"].replace("**", "").replace("*", "")
        st.markdown(f'<div class="outcome-card"><div class="outcome-text">{clean}</div></div>',
                    unsafe_allow_html=True)

    # ── 6. Practical Guidance ──
    if s["practical"]:
        st.markdown('<div class="sec-divider"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="sec-header">
          <div class="sec-icon sec-icon-forest">💡</div>
          <span class="sec-title sec-title-forest">Practical Guidance</span>
        </div>
        """, unsafe_allow_html=True)
        # Build entire practical card in one markdown call to avoid empty-box issue
        items_html = ""
        for pt in s["practical"]:
            clean = pt.replace("**", "").replace("*", "")
            items_html += f"""
            <div class="practical-item">
              <div class="practical-arrow">→</div>
              <div>{clean}</div>
            </div>"""
        st.markdown(f'<div class="practical-card">{items_html}</div>', unsafe_allow_html=True)

    # Close res-body and res-card, then disclaimer strip
    st.markdown("""
      </div>
      <div class="disclaimer">
        ⚠️ &nbsp;Gavel AI provides legal information, not legal advice. Always consult a qualified advocate for your specific matter.
      </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════
# HERO (no messages)
# ═══════════════════════════════════════
if not st.session_state.messages:
    st.markdown("""
    <div class="hero">
      <div class="hero-badge">🔨 &nbsp;AI-Powered · Indian Jurisdiction</div>
      <div class="hero-h1">
        Indian law, <i>clarified.</i><br>Instantly.
      </div>
      <div class="hero-sub">
        Ask any question about Indian law. Powered by Supreme Court judgments,
        constitutional articles, and landmark precedents — synthesized in seconds.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="samples-label">Try a sample inquiry</div>', unsafe_allow_html=True)

    samples = [
        ("📋", "What are my rights under Article 21 of the Constitution?"),
        ("🏠", "Legal requirements for valid property transfer in India"),
        ("🔏", "Supreme Court's current stance on Right to Privacy"),
        ("⏳", "How does Adverse Possession work for land disputes?"),
    ]

    cols = st.columns(2)
    for i, (icon, txt) in enumerate(samples):
        if cols[i % 2].button(f"{icon}  {txt}", use_container_width=True):
            st.session_state.pending_question = txt


# ═══════════════════════════════════════
# CHAT HISTORY
# ═══════════════════════════════════════
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="msg-user-wrap">
          <div class="msg-user-label">You</div>
          <div class="msg-user-bubble">{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        render_response(msg["content"])

st.markdown('<div id="bottom-anchor" style="height:1px;"></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════
# INPUT
# ═══════════════════════════════════════
query = st.chat_input("Ask anything about Indian law…")

if "pending_question" in st.session_state:
    query = st.session_state.pending_question
    del st.session_state.pending_question

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.query_count += 1

    # Show user message immediately before fetching
    st.markdown(f"""
    <div class="msg-user-wrap">
      <div class="msg-user-label">You</div>
      <div class="msg-user-bubble">{query}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Analysing statutes and precedents…"):
        from core.retriever import retrieve_legal_context
        from core.legal_reasoner import generate_legal_answer
        evidence = retrieve_legal_context(query)
        answer = generate_legal_answer(query, evidence)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.scroll_top = True
    st.rerun()


# ═══════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════
st.markdown("""
<div class="footer">
  <div class="footer-logo">Gavel <em>AI</em></div>
  <div class="footer-note">
    Provides legal information synthesized from public statutes and judgments.
    Not a substitute for professional legal counsel.
  </div>
  <div class="footer-tags">
    <span class="footer-tag">Constitution of India</span>
    <span class="footer-tag">SC Corpus 1950–2025</span>
    <span class="footer-tag">IPC · CrPC · BNS</span>
    <span class="footer-tag">v2.0</span>
  </div>
</div>
""", unsafe_allow_html=True)
