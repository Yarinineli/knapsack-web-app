import streamlit as st

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
    # Add loading animation or message
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Zurück"):
            navigate("Algorithmen-Auswahlmaske")
    with col2:
        if st.button("Weiter"):
            navigate("Ergebnismaske")

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