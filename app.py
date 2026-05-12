import streamlit as st
import json
import random
import os

# --- CONFIGURATION & STYLE ---
st.set_page_config(page_title="SkyGuard Academy", page_icon="✈️", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); color: #f8fafc; }
    section[data-testid="stSidebar"] { background-color: rgba(30, 41, 59, 0.5) !important; }
    .custom-card { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 15px; }
    h1, h2, h3 { color: #38bdf8 !important; }
    .stButton>button { width: 100%; border-radius: 8px; background: linear-gradient(90deg, #38bdf8 0%, #0ea5e9 100%); color: white; border: none; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISATION DES DONNÉES ---
if 'stats' not in st.session_state:
    st.session_state.stats = {"xp": 0, "modules_termines": [], "reussites": 0, "total_essais": 0}

def charger_questions():
    if os.path.exists('questions_pro.json'):
        with open('questions_pro.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

COURS = {
    "Réglementation": "Le règlement (CE) 300/2008 définit les normes de base. L'objectif est la protection des passagers et du personnel au sol.",
    "Imagerie RX": "Orange = Organique (explosifs). Bleu = Métal (armes). Vert = Inorganique. Noir = Inpénétrable."
}

BADGES = {
    "Oeil de Lynx": {"cond": lambda s: s["reussites"] >= 5, "icon": "👁️"},
    "Expert": {"cond": lambda s: s["xp"] >= 200, "icon": "🏆"}
}

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.title("🛡️ SkyGuard")
    st.metric("Score", f"{st.session_state.stats['xp']} XP")
    menu = st.radio("Navigation", ["Tableau de bord", "Cours", "Quiz"])

# --- PAGES ---
if menu == "Tableau de bord":
    st.header("Progression de l'Agent")
    cols = st.columns(len(BADGES))
    for i, (nom, data) in enumerate(BADGES.items()):
        unlock = data["cond"](st.session_state.stats)
        cols[i].markdown(f"<div style='text-align:center; opacity:{'1' if unlock else '0.2'}'><h2>{data['icon']}</h2><p>{nom}</p></div>", unsafe_allow_html=True)

elif menu == "Cours":
    st.header("📚 Modules de formation")
    for titre, contenu in COURS.items():
        with st.expander(titre):
            st.write(contenu)
            if st.button(f"Valider {titre}"):
                if titre not in st.session_state.stats["modules_termines"]:
                    st.session_state.stats["modules_termines"].append(titre)
                    st.session_state.stats["xp"] += 50
                    st.rerun()

elif menu == "Quiz":
    st.header("🧠 Examen Blanc")
    questions = charger_questions()
    if questions:
        q = random.choice(questions)
        st.subheader(q['q'])
        choix = st.radio("Réponse :", q['o'])
        if st.button("Soumettre"):
            st.session_state.stats["total_essais"] += 1
            if choix == q['r']:
                st.success("Correct ! +20 XP")
                st.session_state.stats["reussites"] += 1
                st.session_state.stats["xp"] += 20
            else:
                st.error(f"Faux. La réponse était {q['r']}")