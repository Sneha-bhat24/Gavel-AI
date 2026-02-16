import streamlit as st
from core.retriever import retrieve_legal_context
from core.legal_reasoner import generate_legal_answer

st.set_page_config(page_title="Legal Analyser AI", page_icon="⚖️", layout="wide")

# ---------------- GLOBAL CSS ----------------
st.markdown("""
<style>

/* Remove default streamlit spacing */
.block-container {padding-top:1rem; padding-bottom:0rem; max-width:1100px;}
header {visibility:hidden;}
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

/* Navbar */
/* TRUE fixed navbar */
.navbar {
    position:fixed;
    top:0;
    left:0;
    right:0;
    height:64px;
    background:white;
    border-bottom:1px solid #e5e7eb;
    display:flex;
    align-items:center;
    padding:0 24px;
    z-index:9999;
}

/* push page below navbar */
.main .block-container {
    padding-top:90px !important;
}

.brand {
    display:flex;
    align-items:center;
    gap:12px;
}
.logo {
    width:38px;
    height:38px;
    border-radius:8px;
    background:#b45309;
    color:white;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:20px;
    font-weight:bold;
}
.brand-title {font-weight:700; font-size:20px; color:#0f172a;}
.brand-sub {font-size:12px; color:#64748b;}

/* Hero */
.hero {text-align:center; padding:60px 0 30px;}
.hero-icon {
    width:70px;height:70px;border-radius:50%;
    background:#fef3c7;margin:auto;
    display:flex;align-items:center;justify-content:center;
    font-size:30px;color:#b45309;
}
.hero-title {font-size:28px;font-weight:700;color:#0f172a;margin-top:12px;}
.hero-text {color:#475569;max-width:620px;margin:10px auto;font-size:16px;}

/* Info Card */
.info-card {
    background:#eff6ff;
    border:1px solid #bfdbfe;
    border-radius:12px;
    padding:18px;
    max-width:750px;
    margin:20px auto;
    color:#1e40af;
}

/* Sample buttons */
.sample-btn button {
    width:100%;
    background:white;
    border:1px solid #e5e7eb;
    border-radius:10px;
    padding:14px;
    text-align:left;
    font-size:14px;
}
.sample-btn button:hover {border-color:#b45309;background:#fff7ed;}

/* Chat messages */
.user-msg {background:#fff7ed;padding:12px;border-radius:12px;margin:8px 0;}
.ai-msg {background:white;padding:12px;border-radius:12px;margin:8px 0;border:1px solid #e5e7eb;}

/* Input box */
.chatbox {position:sticky;bottom:0;background:white;padding:12px;border-top:1px solid #e5e7eb;}

.footer {text-align:center;color:#64748b;font-size:12px;margin-top:25px;}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
st.markdown("""
<div class="navbar">
<div class="brand">
<div class="logo">⚖</div>
<div>
<div class="brand-title">Legal Analyser AI</div>
<div class="brand-sub">Intelligent Legal Research • Indian Law</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)


# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- HERO SCREEN ----------------
if len(st.session_state.messages) == 0:

    st.markdown("""
    <div class="hero">
        <div class="hero-icon">⚖</div>
        <div class="hero-title">Welcome to Legal Analyser AI</div>
        <div class="hero-text">
        Ask any question about Indian law. Get answers backed by real court judgments and constitutional provisions.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
    <b>How it works</b><br>
    Every answer is grounded in actual legal sources. The system retrieves relevant judgments from Supreme Court and High Courts, along with applicable constitutional provisions.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Try these sample questions")

    samples = [
        "What are my rights under Article 21 of the Constitution?",
        "Explain the legal requirements for property transfer",
        "What is the latest Supreme Court judgment on privacy?",
        "Can I claim adverse possession of property?"
    ]

    for s in samples:
        if st.button(s):
            st.session_state.pending_question = s

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-msg">{msg["content"]}</div>', unsafe_allow_html=True)

# ---------------- INPUT ----------------
query = st.chat_input("Ask a legal question...")

if "pending_question" in st.session_state:
    query = st.session_state.pending_question
    del st.session_state.pending_question

if query:
    st.session_state.messages.append({"role":"user","content":query})

    with st.spinner("Analyzing legal sources..."):
        evidence = retrieve_legal_context(query)
        answer = generate_legal_answer(query, evidence)

    st.session_state.messages.append({"role":"assistant","content":answer})
    st.rerun()

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
Legal Analyser AI provides information based on Indian law. This is not a substitute for professional legal advice.
</div>
""", unsafe_allow_html=True)
