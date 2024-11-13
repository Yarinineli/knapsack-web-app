import streamlit as st
from uis.start_page import start_page
from uis.eingabemaske import eingabemaske
from uis.uebersichtsmaske import uebersichtsmaske
from uis.algorithmen_auswahlmaske import algorithmen_auswahlmaske
from uis.ladescreen import ladescreen
from uis.ergebnismaske import ergebnismaske

# Seiten-Definitionen
pages = {
    "Start": lambda: start_page(),
    "Eingabemaske": lambda: eingabemaske(),
    "Übersichtsmaske": lambda: uebersichtsmaske(),
    "Algorithmen-Auswahlmaske": lambda: algorithmen_auswahlmaske(),
    "Ladescreen": lambda: ladescreen(),
    "Ergebnismaske": lambda: ergebnismaske()
}

# Startpunkt der Anwendung
if "page" not in st.session_state:
    st.session_state.page = "Start"
pages[st.session_state.page]()