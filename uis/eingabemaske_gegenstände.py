import streamlit as st
from navigate import navigate
from data.data import df

def eingabemaske_gegenstände():
    
    with st.container():
    
        tasche, gegenstände = st.columns([0.3, 0.7])
        
        with tasche:
        
            st.title("Gegenstände")
            
            # Check if bag size is set in session_state
            if "bag_size" in st.session_state:
                bag_size = st.session_state['bag_size']
                st.write(f"Du hast eine Taschengröße ausgewählt: {bag_size}")
                
                if bag_size == "Klein (5 kg)":
                    st.image("./images/HSBI_Logo_RRR_schwarz.png", caption="Klein (5 kg)", width=400)
                elif bag_size == "Mittel (10 kg)":
                    st.image("./images/HSBI_Logo_GGG_schwarz.png", caption="Mittel (10 kg)", width=400)
                elif bag_size == "Groß (15 kg)":
                    st.image("./images/HSBI_Logo_BBB_schwarz.png", caption="Groß (15 kg)", width=400)
                else:
                    st.warning("Unbekannte Taschengröße ausgewählt.")
                
            else:
                st.warning("Es wurde keine Tasche ausgewählt. Bitte kehre zurück zur Taschenauswahl.")

            
                    
        with gegenstände:
            st.title("Hier könnt ihr die Gegenstände auswählen:")
            
            weight_limits = {
            "Klein (5 kg)": 5.0,
            "Mittel (10 kg)": 10.0,
            "Groß (15 kg)": 15.0
            }


            # Labels für die Nutzen-Skala
            nutzen_labels = {
                1: "eher nice to have",
                2: "kann hilfreich sein",
                3: "praktisch zu haben",
                4: "wichtig",
                5: "brauche ich unbedingt"
            }

            # Titel und Beschreibung
            st.title("Gegenstände auswählen")
            st.write("Bewerte den Nutzen der Gegenstände für deine Reise:")

            # DataFrame-Konfiguration
            editable_df = st.data_editor(
            df,
            column_config={
                "Nutzen": st.column_config.SelectboxColumn(
                    label="Nutzen",
                    options=list(nutzen_labels.keys()),
                    )
                },
                hide_index=True,
                use_container_width=True,
            )




    col1, col2 = st.columns(2)
    with col1:
        if st.button("Zurück"):
            navigate("Eingabemaske_Tasche")
    with col2:
        @st.dialog("Das willst du also mithnehmen?", width="large")
        def confirm_dialog(editable_df):
            st.dataframe(editable_df, hide_index=True, use_container_width=True)
            if st.button("Yess"):
                st.session_state["vote"] = True
                navigate("Übersichtsmaske")
                st.rerun()

        # Main app code
        if st.button("Weiter"):
            confirm_dialog(editable_df)
