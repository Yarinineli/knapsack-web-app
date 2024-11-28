import streamlit as st
import pandas as pd
from navigate import navigate
from data.data import df  # Importiere deine Gegenstände aus dem DataFrame

def eingabemaske_gegenstände(pages):
    # Initialize an empty DataFrame if not already in session state
    if "gegenstände_df" not in st.session_state:
        st.session_state["gegenstände_df"] = pd.DataFrame(columns=["Gegenstand", "Gewicht (kg)", "Nutzen"])

    # Initialize bag size and capacity if not already in session state
    if "current_weight" not in st.session_state:
        st.session_state["current_weight"] = 0.0

    if "weight_limits" not in st.session_state:
        st.session_state["weight_limits"] = {
            "Klein (5 kg)": 5.0,
            "Mittel (10 kg)": 10.0,
            "Groß (15 kg)": 15.0
        }
    weight_limits = st.session_state["weight_limits"]

    with st.container():
        tasche, gegenstände = st.columns([0.2, 0.8])

        with tasche:
            st.title("Tasche:")
            if "bag_size" in st.session_state:
                bag_size = st.session_state["bag_size"]
                max_capacity = weight_limits[bag_size]
                st.write(f"Du hast eine Taschengröße ausgewählt: {bag_size}")

                # Display corresponding bag image
                bag_images = {
                    "Klein (5 kg)": "./images/klein.png",
                    "Mittel (10 kg)": "./images/mittel.png",
                    "Groß (15 kg)": "./images/gross.png",
                }
                st.image(bag_images.get(bag_size, ""), caption=bag_size, use_container_width=True)
            else:
                st.warning("Es wurde keine Tasche ausgewählt. Bitte kehre zurück zur Taschenauswahl.")

        with gegenstände:
            st.title("Hier kannst du die Gegenstände hinzufügen:")

            # Prepare items for selection
            items_selection = df.copy()
            items_selection['Auswählen'] = False
            items_selection['Nutzen'] = "praktisch zu haben"  # Default utility rating (label)

            # Define utility labels and mapping
            utility_labels = {
                1: "eher nice to have",
                2: "kann hilfreich sein",
                3: "praktisch zu haben",
                4: "wichtig",
                5: "brauche ich unbedingt"
            }

            label_to_value = {v: k for k, v in utility_labels.items()}  # Reverse mapping

            # Create an editable dataframe for item selection
            edited_items = st.data_editor(
                items_selection,
                column_config={
                    "Auswählen": st.column_config.CheckboxColumn(default=False),
                    "Nutzen": st.column_config.SelectboxColumn(
                        options=list(utility_labels.values()),  # Display only labels
                        default="praktisch zu haben"
                    )
                },
                disabled=['Gegenstand', 'Gewicht'],
                hide_index=True
            )

            # Map selected labels back to numeric values
            edited_items['Nutzen'] = edited_items['Nutzen'].map(label_to_value)

            # Identify selected items
            selected_items = edited_items[edited_items['Auswählen']]

            # Display current selection and capacity
            st.write("### Deine Auswahl:")

            # Display selected items
            if not selected_items.empty:
                # Prepare selected items DataFrame
                selected_df = selected_items[['Gegenstand', 'Gewicht', 'Nutzen']].copy()
                selected_df.columns = ['Gegenstand', 'Gewicht (kg)', 'Nutzen']

                st.dataframe(selected_df, hide_index=True, use_container_width=True)
                current_capacity = st.session_state["current_weight"] + selected_items['Gewicht'].sum()
                st.write(f"### Aktuelles Gewicht: {current_capacity:.2f} kg")

            # Navigation Buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Zurück"):
                    navigate("Eingabemaske_Tasche")
            with col2:
                if st.button("Weiter"):
                    if selected_items.empty:
                        st.warning("Bitte wähle mindestens einen Gegenstand aus, bevor du fortfährst.")
            
                    @st.dialog("Bitte bestätige deine Auswahl", width="large")
                    def dialog():
                        if current_capacity > max_capacity:
                            st.write(f"Du willst also in deine {max_capacity} kg Tasche {current_capacity:.2f} kg packen?! 🤣🤣🤣")
                        st.dataframe(selected_df, hide_index=True, use_container_width=True)
                        if st.button("Bestätigen"):
                            # Store selected items in session state
                            st.session_state["gegenstände_df"] = selected_df
                            navigate("Algorithmen-Auswahlmaske", pages)
                        if st.button("Abbrechen"):
                            st.rerun()
                    dialog()