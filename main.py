import streamlit as st
from src.ui.start_page import start_page
from src.ui.eingabemaske_tasche import eingabemaske_tasche
from src.ui.algorithmen_auswahlmaske import algorithmen_auswahlmaske
from src.ui.ergebnismaske import ergebnismaske
from src.ui.eingabemaske_gegenstände import eingabemaske_gegenstände


# Seiten-Definitionen
st.logo("static/images/HSBI_Logo_RGB_schwarz.png", size="large")
st.set_page_config(
    page_title="Knapsack Problem",
    page_icon="🎒",
    layout="wide",
)

pages = {
    "Start": lambda: start_page(pages),
    "Eingabemaske_Tasche": lambda: eingabemaske_tasche(pages),
    "Eingabemaske_Gegenstände": lambda: eingabemaske_gegenstände(pages),
    "Algorithmen-Auswahlmaske": lambda: algorithmen_auswahlmaske(pages),
    "Ergebnismaske": lambda: ergebnismaske(pages),
}

# Startpunkt der Anwendung
if "page" not in st.session_state:
    st.session_state.page = "Start"
pages[st.session_state.page]()