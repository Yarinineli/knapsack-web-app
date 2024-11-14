import streamlit as st
from navigate import navigate, clear_inputs

def ergebnismaske():
    st.title("Ergebnismaske")
    st.write("Die Ergebnisse der ausgewählten Algorithmen werden präsentiert.")
    # Add elements to display the results and comparison of algorithms
    # ...
    if st.button("Zurück zur Startseite"):
        clear_inputs()
        navigate("Start")