import streamlit as st
import time
from navigate import navigate


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