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
                
#TODO:Eventuell muss ich hier eine Auswahl bereitstellen in der der Benutzer erstmal auswählt welche gegenstände mitnehmen würde und anschließend die Nutzenbewertung folgt. Sonst ergeibt die App nciht so viuel sinn wenn ich die dinge nur nach gewicht auswähle

        with gegenstände:
            st.title("Hier kannst du die Gegenstände hinzufügen:")

            # Form to add a new item
            hinzufügen, entfernen = st.columns([0.5, 0.5])
            
            with hinzufügen:
            
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
                        elif st.session_state["current_weight"] + new_weight > max_capacity:
                            st.error(f"{new_item} kann nicht hinzugefügt werden. Der Rucksack würde überfüllt werden!")
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
                            st.session_state["current_weight"] += new_weight
                            st.success(f"{new_item} wurde hinzugefügt!")
                            st.write("### Aktuelle Kapazität des Rucksacks:")
                             # Display current and max capacity
            with entfernen:
                if st.session_state["gegenstände_df"].empty:
                    st.write(" ")
                else:
                    # Form to delete an item
                    with st.form(key="delete_item_form"):
                        delete_item = st.selectbox(
                            "Wähle einen Gegenstand zum Entfernen:",
                            st.session_state["gegenstände_df"]["Gegenstand"].unique()
                        )
                        delete_submitted = st.form_submit_button("Entfernen")

                        if delete_submitted:
                            # Gegenstand entfernen
                            item_row = st.session_state["gegenstände_df"].loc[
                                st.session_state["gegenstände_df"]["Gegenstand"] == delete_item
                            ]
                            if not item_row.empty:
                                item_weight = item_row["Gewicht (kg)"].values[0]
                                st.session_state["gegenstände_df"] = st.session_state["gegenstände_df"][
                                    st.session_state["gegenstände_df"]["Gegenstand"] != delete_item
                                ]
                                st.session_state["current_weight"] -= item_weight
                                st.success(f"{delete_item} wurde entfernt!")
                            else:
                                st.error(f"{delete_item} konnte nicht gefunden werden.")
                        

            # Display the DataFrame
            st.write("### Deine Auswahl:")
            current_capacity = st.session_state["current_weight"]
            st.progress(current_capacity / max_capacity)
            st.write(f"{current_capacity:.2f} kg / {max_capacity} kg")  # Display current and max capacity
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
                        @st.dialog("Cast your vote", width="large")
                        def dialog():
                            st.write("Bitte bestätige deine Auswahl")
                            st.dataframe(st.session_state["gegenstände_df"], hide_index=True, use_container_width=True)
                            if st.button("Bestätigen"):
                                navigate("Algorithmen-Auswahlmaske", pages)
                            if st.button("Abbrechen"):
                                st.rerun()
                        dialog()