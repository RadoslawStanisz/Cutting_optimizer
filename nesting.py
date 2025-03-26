from helpers import nesting_rectpack, oblicz_wykorzystanie_arkusza, generuj_svg, algos, sorting_met, \
    sorting_names
import streamlit as st


def wykonaj_nesting(formatki):
    ROTATION = st.session_state.ROTATION
    ARKUSZ_SZEROKOSC = st.session_state.ARKUSZ_SZEROKOSC
    ARKUSZ_WYSOKOSC = st.session_state.ARKUSZ_WYSOKOSC

    best_algo, best_sorting, best_arkusze = None, None, None
    best_sheet_count = float("inf")
    best_last_sheet_utilization = float("inf")

    for algo in algos:
        for sorting in sorting_met:
            arkusze = nesting_rectpack(ARKUSZ_SZEROKOSC, ARKUSZ_WYSOKOSC, formatki, algo, sorting, ROTATION)
            print(f"🛠️ Debug: Liczba arkuszy: {len(arkusze)}")  # Sprawdzenie, czy lista nie jest pusta
            wykorzystanie_ostatniego = oblicz_wykorzystanie_arkusza(arkusze, ARKUSZ_SZEROKOSC, ARKUSZ_WYSOKOSC)
            print(
                f"Algorytm: {algo.__name__}, Sortowanie: {sorting_names[sorting]} - Liczba arkuszy: {len(arkusze)}, Wykorzystanie ostatniego arkusza: {wykorzystanie_ostatniego:.2f}%")

            if len(arkusze) < best_sheet_count or (
                    len(arkusze) == best_sheet_count and wykorzystanie_ostatniego < best_last_sheet_utilization):
                best_sheet_count = len(arkusze)
                best_last_sheet_utilization = wykorzystanie_ostatniego
                best_algo = algo
                best_sorting = sorting
                best_arkusze = arkusze

    if best_algo:
        nazwa_sortowania = sorting_names.get(best_sorting, "UNKNOWN")
        nazwa_pliku_base = f"Rectpack_{best_algo.__name__}_{nazwa_sortowania}_{ARKUSZ_SZEROKOSC}x{ARKUSZ_WYSOKOSC}"
        print(
            f"📌 Najlepszy algorytm: {best_algo.__name__}, Sortowanie: {nazwa_sortowania} - Liczba arkuszy: {best_sheet_count}, Wykorzystanie ostatniego arkusza: {best_last_sheet_utilization:.2f}%")
        generuj_svg(best_arkusze, nazwa_pliku_base, ARKUSZ_SZEROKOSC, ARKUSZ_WYSOKOSC, ROTATION)