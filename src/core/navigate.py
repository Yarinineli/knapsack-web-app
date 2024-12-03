import streamlit as st

def navigate(page_name, pages):
    """
    Updates the current page in the session state and logs session state keys and values.
    """
    if page_name in pages:
        st.session_state.page = page_name
        # Log session state keys and values to the console
        print("\n--- Navigation Triggered ---")
        print(f"Navigating to: {page_name}")
        print("Current Session State:")
        for key, value in st.session_state.items():
            print(f"{key}: {value}")
        print("--- End of Session State ---\n")
        st.rerun()  # Ensure the app refreshes to show the new page
    else:
        print(f"Error: Page {page_name} not found in navigation pages.")

# Function to clear all inputs in the session state
def clear_inputs():
    for key in list(st.session_state.keys()):
        del st.session_state[key]