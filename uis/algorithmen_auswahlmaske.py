import streamlit as st
from navigate import navigate
import pandas as pd



def algorithmen_auswahlmaske(pages):
    tasche, gegenstände = st.columns([0.2, 0.8])
    with tasche:
        if "bag_size" in st.session_state:
            bag_size = st.session_state["bag_size"]
            st.write(f"Du hast eine Taschengröße ausgewählt: {bag_size}")
            bag_images = {
                    "Klein (5 kg)": "./images/klein.png",
                    "Mittel (10 kg)": "./images/mittel.png",
                    "Groß (15 kg)": "./images/gross.png",
                }
            st.image(bag_images.get(bag_size, ""), caption=bag_size, width=400)
        
        
        
        tasche_data = st.session_state.get("bag_size", "Keine Auswahl")
        st.write("Tasche:", tasche_data)
    with gegenstände:
        gegenstände_data = st.session_state.get("gegenstände_df", pd.DataFrame(columns=["Gegenstand", "Gewicht (kg)", "Nutzen"]))
        st.write("Gegenstände:")
        st.dataframe(gegenstände_data, hide_index=True, use_container_width=True)

    
    
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