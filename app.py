import streamlit as st
import json
import random
import os

# --- CONFIGURATION INTERFACE ---
st.set_page_config(page_title="SkyGuard Academy", page_icon="✈️", layout="centered")

# --- DESIGN PREMIUM CSS ---
st.markdown("""
    <style>
    /* Fond et conteneur */
    .stApp { background-color: #0f172a; color: #f8fafc; }
    
    /* Cartes de modules */
    .module-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        margin-bottom: 15px;
    }
    
    /* Boutons */
    .stButton>button {
        background: linear-gradient(90deg, #0284c7 0%, #0369a1 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { border-color: #38bdf8; box-shadow: 0 0 10px #38bdf8; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'page' not in st.session_state: st.session_state.page = "Dashboard"

# --- LOGIQUE QUESTIONS ---
def load_questions():
    if os.path.exists('questions_pro.json'):
        with open('questions_pro.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return [{"q": "Erreur de base", "o": ["A", "B"], "r": "A"}]

# --- NAVIGATION ---
st.sidebar.title("✈️ SkyGuard")
st.sidebar.metric("Score Agent", f"{st.session_state.xp} XP")
if st.sidebar.button("📊 Tableau de bord"): st.session_state.page = "Dashboard"
if st.sidebar.button("🎓 Cours"): st.session_state.page = "Cours"
if st.sidebar.button("🧠 Quiz"): st.session_state.page = "Quiz"

# --- PAGES ---
if st.session_state.page == "Dashboard":
    st.title("Bienvenue, Agent")
    st.markdown(f"""
    <div class="module-card">
        <h3>Statistiques Actuelles</h3>
        <p>XP Total : <b>{st.session_state.xp}</b></p>
        <p>Niveau : <b>{'Débutant' if st.session_state.xp < 100 else 'Confirmé'}</b></p>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "Cours":
    st.title("Modules de Formation")
    with st.container():
        st.markdown("<div class='module-card'><h3>Module 1 : Imagerie RX</h3><p>L'orange désigne les matières organiques comme les explosifs.</p></div>", unsafe_allow_html=True)
        if st.button("Valider le module (+50 XP)"):
            st.session_state.xp += 50
            st.success("Points ajoutés !")
            st.rerun()

elif st.session_state.page == "Quiz":
    st.title("Testez vos réflexes")
    qs = load_questions()
    q = random.choice(qs)
    
    st.subheader(q['q'])
    rep = st.radio("Sélectionnez :", q['o'])
    
    if st.button("Vérifier"):
        if rep == q['r']:
            st.balloons()
            st.session_state.xp += 20
            st.success("Bravo ! +20 XP")
            st.button("Question suivante")
        else:
            st.error(f"Raté ! La réponse était : {q['r']}")
