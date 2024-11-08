import streamlit as st
import time
import random

# Startseite
def start_page():
    st.title("Einführung in das Knapsack-Problem")
    st.write("Die App startet mit einer Einführung in das Knapsack-Problem, die dem Benutzer eine einfache Erläuterung der Problemstellung bietet.")
    if st.button("Weiter"):
        navigate("Eingabemaske")

# Eingabemaske
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

# Übersichtsmaske
def uebersichtsmaske():
    st.title("Übersichtsmaske")
    st.write("Übersicht der gewählten Gegenstände und deren Eigenschaften (Gewicht und Nutzen).")
    # Add elements to display and modify the selected items
    # ...
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Zurück"):
            navigate("Eingabemaske")
    with col2:
        if st.button("Weiter"):
            navigate("Algorithmen-Auswahlmaske")

# Algorithmen-Auswahlmaske
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

# Ladescreen


def ladescreen():
    st.title("Ladescreen")
    st.write("Die Berechnungen laufen...")
    
    if "loading" not in st.session_state:
        st.session_state.loading = False

    if not st.session_state.loading:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Zurück"):
                navigate("Algorithmen-Auswahlmaske")
        with col2:
            if st.button("Weiter"):
                st.session_state.loading = True
                st.rerun()

    if st.session_state.loading:
        # Show the progress bar when "Weiter" is clicked
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.1)  # Adjust the sleep time for faster or slower progress
            my_bar.progress(percent_complete + 1, text=progress_text)

        time.sleep(1)  # Optional pause before clearing the progress bar
        my_bar.empty()

        # Navigate to the next screen
        st.session_state.loading = False
        navigate("Ergebnismaske")

# def ladescreen():
#     st.title("Ladescreen")
#     st.write("Die Berechnungen laufen...")
    
#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("Zurück"):
#             navigate("Algorithmen-Auswahlmaske")
#     with col2:
#         if st.button("Weiter"):
#             navigate("Ergebnismaske")

# Ergebnismaske
def ergebnismaske():
    st.title("Ergebnismaske")
    st.write("Die Ergebnisse der ausgewählten Algorithmen werden präsentiert.")
    # Add elements to display the results and comparison of algorithms
    # ...
    if st.button("Zurück zur Startseite"):
        clear_inputs()
        navigate("Start")

# Seitenwechsel-Funktion
def navigate(page_name):
    st.session_state.page = page_name
    st.rerun()

# Funktion zum Löschen der Eingaben
def clear_inputs():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Seiten-Definitionen
pages = {
    "Start": start_page,
    "Eingabemaske": eingabemaske,
    "Übersichtsmaske": uebersichtsmaske,
    "Algorithmen-Auswahlmaske": algorithmen_auswahlmaske,
    "Ladescreen": ladescreen,
    "Ergebnismaske": ergebnismaske
}

# Startpunkt der Anwendung
if "page" not in st.session_state:
    st.session_state.page = "Start"
pages[st.session_state.page]()