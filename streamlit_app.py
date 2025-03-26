import streamlit as st
import os
import glob
from helpers import ARKUSZE
from cabinets import Wycena, SzafkaDolna, SzafkaGorna
from nesting import wykonaj_nesting

# Inicjalizacja session_state
if 'szafki' not in st.session_state:
    st.session_state.szafki = []
    st.session_state.wycena = Wycena()

st.sidebar.header("Add new cabinet")

arkusz_keys = list(ARKUSZE.keys())
arkusz_labels = [f"{ARKUSZE[key][0]} x {ARKUSZE[key][1]}" for key in arkusz_keys]
wybor_arkusza = st.sidebar.selectbox("Choose board size:", options=arkusz_keys,
                                     format_func=lambda x: f"{ARKUSZE[x][0]} x {ARKUSZE[x][1]}")
st.session_state.ARKUSZ_SZEROKOSC, st.session_state.ARKUSZ_WYSOKOSC = ARKUSZE[wybor_arkusza]

# Parametry szafki
typ_szafki = st.sidebar.selectbox("Cabinet type", ["Base", "Wall"])
szerokosc = st.sidebar.number_input("Width (mm)", min_value=100, max_value=1200, value=600, step=50)
wysokosc = st.sidebar.number_input("Height (mm)", min_value=100, max_value=2400, value=720, step=50)
glebokosc = st.sidebar.number_input("Depth (mm)", min_value=100, max_value=800, value=500, step=50)
ilosc = st.sidebar.number_input("Quantity", min_value=1, value=1, step=1)
front = st.sidebar.selectbox("Door type", ["Normal", "Special", "None"])

if typ_szafki == "Base":
    liczba_polek = st.sidebar.number_input("Number of shelves", min_value=0, value=0, step=1)
    liczba_szuflad = st.sidebar.number_input("Number of drawers", min_value=0, value=0, step=1)
    cargo = st.sidebar.checkbox("Cargo system")

    if st.sidebar.button("Add cabinet"):
        szafka = SzafkaDolna(szerokosc, wysokosc, glebokosc, ilosc, front, liczba_polek=liczba_polek,
                             liczba_szuflad=liczba_szuflad, cargo=cargo)
        st.session_state.szafki.append(szafka)
        st.session_state.wycena.dodaj_szafke(szafka)
        st.sidebar.success("Base cabinet added successfully!")

elif typ_szafki == "Wall":
    liczba_polek = st.sidebar.number_input("Number of shelves", min_value=0, value=0, step=1)

    if st.sidebar.button("Add cabinet"):
        szafka = SzafkaGorna(szerokosc, wysokosc, glebokosc, ilosc, front, liczba_polek=liczba_polek)
        st.session_state.szafki.append(szafka)
        st.session_state.wycena.dodaj_szafke(szafka)
        st.sidebar.success("Wall cabinet added successfully!")

rotation_option = st.sidebar.radio("Does grain direction matter?", ["Yes", "No"])
st.session_state.ROTATION = False if rotation_option == "Yes" else True

# st.sidebar.write("### Order list:")
# for i, szafka in enumerate(st.session_state.szafki):
# st.sidebar.write(f"**{i+1}.** {szafka.__class__.__name__} - {szafka.szerokosc}x{szafka.wysokosc}x{szafka.glebokosc} mm, {szafka.ilosc} szt.")

MAPOWANIE_NAZW = {
    "SzafkaGorna": "Wall cabinet",
    "SzafkaDolna": "Base cabinet"
}

st.sidebar.write("### Order list:")
for i, szafka in enumerate(st.session_state.szafki):
    nazwa_szafki = MAPOWANIE_NAZW.get(szafka.__class__.__name__,
                                      szafka.__class__.__name__)  # Domyślnie użyje oryginalnej nazwy, jeśli nie ma w mapowaniu
    st.sidebar.write(
        f"**{i + 1}.** {nazwa_szafki} - {szafka.szerokosc}x{szafka.wysokosc}x{szafka.glebokosc} mm, {szafka.ilosc} pcs.")

if st.sidebar.button("Reset order list"):
    st.session_state.szafki = []
    st.session_state.wycena = Wycena()
    st.sidebar.success("The order list has been cleared!")

# Generowanie wyceny
st.title("Order details")

# ✅ Przechowywanie wyników w st.session_state, aby nie znikały po kliknięciu drugiego guzika
if "podsumowanie" not in st.session_state:
    st.session_state.podsumowanie = None
if "rozrys" not in st.session_state:
    st.session_state.rozrys = None

# Przycisk "Generuj wycenę"
if st.button("Get report"):
    st.session_state.podsumowanie = st.session_state.wycena.podsumowanie()

# ✅ Wyświetlanie podsumowania wyceny, jeśli istnieje w sesji
if st.session_state.podsumowanie:
    podsumowanie = st.session_state.podsumowanie
    # st.header("Podsumowanie wyceny")

    st.subheader("Board elements")
    st.write(f"🪵 Elements total: {len(podsumowanie['Płyta meblowa'])}")
    st.write(", ".join([f"{w}x{h}" for w, h in podsumowanie["Płyta meblowa"]]))

    st.subheader("Door surface")
    st.write(f"{round(podsumowanie['Powierzchnia frontów (m²)'], 2)} [m²]")

    st.subheader("Back panel HDF")
    st.write(f"📏 Elements total: {len(podsumowanie['HDF plecy'])}")
    st.write(", ".join([f"{w}x{h}" for w, h in podsumowanie["HDF plecy"]]))

    st.subheader("Hardware")
    for akcesorium, ilosc in podsumowanie["Akcesoria"].items():
        st.write(f"🔩 {akcesorium}: {ilosc} pcs.")

# Przycisk "Generuj rozrys"
if st.button("Optimize cutting"):
    formatki = st.session_state.wycena.podsumowanie()['Płyta meblowa']
    wykonaj_nesting(formatki)  # Wywołanie nestingu
    lista_svg = glob.glob("*.svg")
    st.session_state.rozrys = lista_svg

# ✅ Wyświetlanie rozrysów, jeśli istnieją w sesji
if st.session_state.rozrys:
    st.subheader("Cutting plan preview")
    for sciezka_svg in st.session_state.rozrys:
        with open(sciezka_svg, "r", encoding="utf-8") as f:
            svg_content = f.read()

        st.markdown(f"""
        <div style="text-align: center; max-width: 90%; margin: auto; margin-bottom: 20px;">
            <div style="overflow: hidden;">
                {svg_content.replace('<svg', '<svg width="100%" height="auto" style="max-height: 500px; display: block;"')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    for sciezka_svg in lista_svg:
        os.remove(sciezka_svg)
    # st.success("Pliki SVG zostały usunięte po załadowaniu.")
