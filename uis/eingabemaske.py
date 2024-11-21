import streamlit as st
from navigate import navigate

def eingabemaske():
    st.title("Eingabemaske")
    st.write("Wähle einen Rucksack aus einer Liste oder definiere einen neuen Rucksack.")
    # Add input elements for selecting or defining a backpack and items
    # ...
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Zurück"):
            navigate("Start")
    with col2:
        if st.button("Weiter"):
            navigate("Übersichtsmaske")