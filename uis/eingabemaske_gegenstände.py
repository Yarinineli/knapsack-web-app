import streamlit as st
import pandas as pd
from navigate import navigate
from data.data import df  # Importiere deine Gegenstände aus dem DataFrame

def eingabemaske_gegenstände():
    # Initialize an empty DataFrame if not already in session state
    if "gegenstände_df" not in st.session_state:
        st.session_state["gegenstände_df"] = pd.DataFrame(columns=["Gegenstand", "Gewicht (kg)", "Nutzen"])

    with st.container():
        tasche, gegenstände = st.columns([0.3, 0.7])

        with tasche:
            st.title("Gegenstände")
            if "bag_size" in st.session_state:
                bag_size = st.session_state["bag_size"]
                st.write(f"Du hast eine Taschengröße ausgewählt: {bag_size}")

                # Display corresponding bag image
                bag_images = {
                    "Klein (5 kg)": "./images/HSBI_Logo_RRR_schwarz.png",
                    "Mittel (10 kg)": "./images/HSBI_Logo_GGG_schwarz.png",
                    "Groß (15 kg)": "./images/HSBI_Logo_BBB_schwarz.png",
                }
                st.image(bag_images.get(bag_size, ""), caption=bag_size, width=400)
            else:
                st.warning("Es wurde keine Tasche ausgewählt. Bitte kehre zurück zur Taschenauswahl.")

        with gegenstände:
            st.title("Hier kannst du die Gegenstände hinzufügen:")

            # Form to add a new item
            with st.form(key="add_item_form"):
                # Dropdown für Gegenstandsauswahl
                new_item_with_weight = st.selectbox(
                    "Wähle einen Gegenstand:",
                    df.apply(lambda row: f"{row['Gegenstand']} ({row['Gewicht']} kg)", axis=1).unique())

                # Extract item name from the selected option
                new_item = new_item_with_weight.split(" (")[0]

                # Gewicht automatisch aus df holen basierend auf ausgewähltem Gegenstand
                new_weight = df.loc[df["Gegenstand"] == new_item, "Gewicht"].values[0]

              

                # Nutzen bewerten
                new_nutzen = st.selectbox(
                    "Bewerte den Nutzen:",
                    options=[1, 2, 3, 4, 5],
                    format_func=lambda x: {
                        1: "eher nice to have",
                        2: "kann hilfreich sein",
                        3: "praktisch zu haben",
                        4: "wichtig",
                        5: "brauche ich unbedingt",
                    }[x],
                )

                submitted = st.form_submit_button("Hinzufügen")

                if submitted:
                    # Überprüfen, ob der Gegenstand bereits hinzugefügt wurde
                    if new_item in st.session_state["gegenstände_df"]["Gegenstand"].values:
                        st.warning(f"{new_item} wurde bereits hinzugefügt.")
                    else:
                        # Neuen Gegenstand hinzufügen
                        new_row = pd.DataFrame([{
                            "Gegenstand": new_item,
                            "Gewicht (kg)": new_weight,
                            "Nutzen": new_nutzen,
                        }])
                        st.session_state["gegenstände_df"] = pd.concat(
                            [st.session_state["gegenstände_df"], new_row],
                            ignore_index=True
                        )
                        st.success(f"{new_item} wurde hinzugefügt!")

            # Display the DataFrame
            st.write("### Deine Auswahl:")
            st.dataframe(st.session_state["gegenstände_df"], hide_index=True, use_container_width=True)

    # Navigation Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Zurück"):
            navigate("Eingabemaske_Tasche")
    with col2:
        if st.button("Weiter"):
            if st.session_state["gegenstände_df"].empty:
                st.warning("Bitte füge mindestens einen Gegenstand hinzu, bevor du fortfährst.")
            else:
                navigate("Übersichtsmaske")
