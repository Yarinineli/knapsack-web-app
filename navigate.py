import streamlit as st

def navigate(page_name):
    st.session_state.page = page_name
    st.rerun()

# Funktion zum Löschen der Eingaben
def clear_inputs():
    for key in list(st.session_state.keys()):
        del st.session_state[key]