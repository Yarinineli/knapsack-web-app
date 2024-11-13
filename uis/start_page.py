import streamlit as st 
from navigate import navigate

def start_page():
    st.title("Einführung in das Knapsack-Problem")
    st.write("Die App startet mit einer Einführung in das Knapsack-Problem, die dem Benutzer eine einfache Erläuterung der Problemstellung bietet.")
    if st.button("Weiter"):
        navigate("Eingabemaske")