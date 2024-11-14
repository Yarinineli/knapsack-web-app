import streamlit as st
from navigate import navigate


def algorithmen_auswahlmaske():
    st.title("Algorithmen-Auswahlmaske")
    st.write("Wähle einen oder mehrere Algorithmen zur Lösung des Knapsack-Problems.")
    # Add elements to select algorithms and show information about them
    # ...
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Zurück"):
            navigate("Übersichtsmaske")
    with col2:
        if st.button("Weiter"):
            navigate("Ladescreen")