import streamlit as st
import pandas as pd
from src.core import navigate
from src.data import df

def eingabemaske_gegenstände(pages):
    # Existing initialization code...
    if "gegenstände_df" not in st.session_state:
        st.session_state["gegenstände_df"] = pd.DataFrame(columns=["Gegenstand", "Gewicht (kg)", "Nutzen"])

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

                bag_images = {
                    "Klein (5 kg)": "static/images/klein.png",
                    "Mittel (10 kg)": "static/images/mittel.png",
                    "Groß (15 kg)": "static/images/gross.png",
                }
                st.image(bag_images.get(bag_size, ""), caption=bag_size, use_container_width=True)
                
                # Add test mode button below the bag image
                test_mode = st.toggle("Test-Modus", value=False, help="Alle Gegenstände automatisch auswählen")
            else:
                st.warning("Es wurde keine Tasche ausgewählt. Bitte kehre zurück zur Taschenauswahl.")
                test_mode = False

        with gegenstände:
            st.title("Hier kannst du die Gegenstände hinzufügen:")

            # Prepare items for selection
            items_selection = df.copy()

            # Define utility labels and mapping
            utility_labels = {
                1: "eher nice to have",
                2: "kann hilfreich sein",
                3: "praktisch zu haben",
                4: "wichtig",
                5: "brauche ich unbedingt"
            }

            label_to_value = {v: k for k, v in utility_labels.items()}

            # Apply test mode if activated
            if test_mode:
                items_selection['Auswählen'] = True
                for i in range(len(items_selection)):
                    items_selection.at[i, 'Nutzen'] = utility_labels[(i % 5) + 1]
            else:
                items_selection['Auswählen'] = False
                items_selection['Nutzen'] = utility_labels[3]  # Default: "praktisch zu haben"

            # Create an editable dataframe
            edited_items = st.data_editor(
                items_selection,
                column_config={
                    "Auswählen": st.column_config.CheckboxColumn(default=False),
                    "Nutzen": st.column_config.SelectboxColumn(
                        options=list(utility_labels.values()),
                        default="praktisch zu haben"
                    )
                },
                disabled=['Gegenstand', 'Gewicht'],
                hide_index=True,
                height=0
            )

            # Rest of your code remains the same...
            edited_items['Nutzen'] = edited_items['Nutzen'].map(label_to_value)
            selected_items = edited_items[edited_items['Auswählen']]

            st.write("### Deine Auswahl:")

            current_capacity = st.session_state["current_weight"] + selected_items['Gewicht'].sum()

            if not selected_items.empty:
                selected_df = selected_items[['Gegenstand', 'Gewicht', 'Nutzen']].copy()
                selected_df.columns = ['Gegenstand', 'Gewicht (kg)', 'Nutzen']

                st.dataframe(selected_df, hide_index=True, use_container_width=True)
                current_capacity = st.session_state["current_weight"] + selected_items['Gewicht'].sum()
                st.write(f"### Aktuelles Gewicht: {current_capacity:.2f} kg")

            # Navigation Buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Zurück"):
                    navigate("Eingabemaske_Tasche", pages)
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
                            st.session_state["gegenstände_df"] = selected_df
                            navigate("Algorithmen-Auswahlmaske", pages)
                        if st.button("Abbrechen"):
                            st.rerun()
                    dialog()