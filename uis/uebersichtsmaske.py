import streamlit as st
from navigate import navigate

def uebersichtsmaske():
    st.title("Übersichtsmaske")
    st.write("Übersicht der gewählten Gegenstände und deren Eigenschaften (Gewicht und Nutzen).")
    # Add elements to display and modify the selected items
    # ...
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Zurück"):
            navigate("Eingabemaske_Gegenstände")
    with col2:
        if st.button("Weiter"):
            navigate("Algorithmen-Auswahlmaske")