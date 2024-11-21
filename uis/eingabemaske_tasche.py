import streamlit as st
from navigate import navigate
from streamlit_image_select import image_select


def eingabemaske_tasche():
    st.title("Tasche")
    
    Rucksackauswahl = """
    Jede Reise beginnt mit der Wahl des richtigen Rucksacks! Stell dir vor, du planst eine Wanderung, eine Geschäftsreise oder einfach 
    nur einen Tag in der Stadt. Der Platz in deinem Rucksack ist begrenzt, und du musst ihn so effizient wie möglich nutzen.
    
    In diesem Schritt kannst du eine Taschengröße auswählen, die am besten zu deinem Szenario passt. Jede Größe repräsentiert eine 
    andere Kapazität – von einem kompakten Rucksack für das Nötigste bis hin zu einem großen Reisegepäck, das Platz für alles bietet, 
    was du dir vorstellen kannst. Die gewählte Taschengröße legt die maximale Kapazität deines Rucksacks fest, also wähle weise!
    """
    
    st.write(Rucksackauswahl)
    
    # Image selection for bag sizes
    bag_image = image_select(
        label="Wähle eine Taschengröße",
        images=[
            "./images/HSBI_Logo_RRR_schwarz.png",  # Local image file for 'Klein'
            "./images/HSBI_Logo_GGG_schwarz.png",  # Local image file for 'Mittel'
            "./images/HSBI_Logo_BBB_schwarz.png",  # Local image file for 'Groß'
        ],
        captions=["Klein (5 kg)", "Mittel (10 kg)", "Groß (15 kg)"],  # Descriptive captions
        use_container_width=True
    )

    # Map selected image to corresponding bag size
    if bag_image == "./images/HSBI_Logo_RRR_schwarz.png":
        st.session_state["bag_size"] = "Klein (5 kg)"
    elif bag_image == "./images/HSBI_Logo_GGG_schwarz.png":
        st.session_state["bag_size"] = "Mittel (10 kg)"
    elif bag_image == "./images/HSBI_Logo_BBB_schwarz.png":
        st.session_state["bag_size"] = "Groß (15 kg)"

    # Display selected bag size
    st.success(f"Ausgewählte Taschengröße: {st.session_state.get('bag_size', 'Keine Auswahl')}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Zurück"):
            navigate("Start")
    with col2:
        if st.button("Weiter"):
            navigate("Eingabemaske_Gegenstände")
