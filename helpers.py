import svgwrite
from rectpack import newPacker
from rectpack import guillotine as g
from rectpack import packer as p

# Dostępne wymiary arkuszy (mm)
ARKUSZE = {
    "1": (2800, 2070),
    "2": (2500, 1250)
}  # Lista dostępnych arkuszy

# Wybór rotacji elementów
# rotation_input = input("Czy usłojenie ma znaczenie? (tak/nie): ").strip().lower()
# ROTATION = False if rotation_input == "tak" else True


# Lista algorytmów
algos = [
    g.GuillotineBssfSas, g.GuillotineBssfLas, g.GuillotineBssfSlas, g.GuillotineBssfLlas, g.GuillotineBssfMaxas,
    g.GuillotineBssfMinas,
    g.GuillotineBlsfSas, g.GuillotineBlsfLas, g.GuillotineBlsfSlas, g.GuillotineBlsfLlas, g.GuillotineBlsfMaxas,
    g.GuillotineBlsfMinas,
    g.GuillotineBafSas, g.GuillotineBafLas, g.GuillotineBafSlas, g.GuillotineBafLlas, g.GuillotineBafMaxas,
    g.GuillotineBafMinas
]

# Lista metod sortowania
sorting_met = [
    p.SORT_NONE, p.SORT_SSIDE, p.SORT_AREA, p.SORT_PERI, p.SORT_DIFF, p.SORT_LSIDE, p.SORT_RATIO
]

# Tworzenie dynamicznego słownika nazw metod sortowania
sorting_names = {val: key for key, val in vars(p).items() if key.startswith("SORT_")}


def nesting_rectpack(arkusz_szer, arkusz_wys, formatki, algo, sorting, rotation):
    packer = newPacker(pack_algo=algo, rotation=rotation, sort_algo=sorting)

    # Dodanie elementów do packera
    for szer, wys in formatki:
        packer.add_rect(szer, wys)

    # Dodanie arkuszy
    packer.add_bin(arkusz_szer, arkusz_wys, float("inf"))

    # Wykonanie pakowania
    packer.pack()

    # Pobranie wyników
    arkusze = []
    for abin in packer:
        rozmieszczenie = []
        for rect in abin:
            x, y, szer, wys = rect.x, rect.y, rect.width, rect.height
            rozmieszczenie.append((x, y, szer, wys))
        arkusze.append(rozmieszczenie)

    return arkusze


def oblicz_wykorzystanie_arkusza(arkusze, arkusz_szer, arkusz_wys):
    if not arkusze:  # Jeśli lista jest pusta
        print("⚠️ Brak arkuszy - nie można obliczyć wykorzystania.")
        return 0
    powierzchnia_arkusza = arkusz_szer * arkusz_wys
    ostatni_arkusz = arkusze[-1]
    powierzchnia_ostatniego = sum(w * h for _, _, w, h in ostatni_arkusz)
    return powierzchnia_ostatniego / powierzchnia_arkusza * 100


def generuj_svg(arkusze, nazwa_pliku_base, arkusz_szer, arkusz_wys, uslojenie):
    """Tworzy podgląd rozmieszczenia elementów w plikach SVG dla każdego arkusza"""
    for idx, rozmieszczenie in enumerate(arkusze):
        nazwa_pliku = f"{nazwa_pliku_base}_{idx + 1}.svg"

        # Ustawienie viewBox, które pozwala poprawnie skalować SVG
        dwg = svgwrite.Drawing(nazwa_pliku, profile='tiny', size=(f'{arkusz_szer}px', f'{arkusz_wys}px'),
                               viewBox=f"0 0 {arkusz_szer} {arkusz_wys}")

        dwg.add(dwg.rect(insert=(0, 0), size=(arkusz_szer, arkusz_wys), fill='none', stroke='red', stroke_width=3))

        # Dodanie przerywanych linii dla kierunku słojów (jeśli usłojenie ma znaczenie)
        if not uslojenie:
            for i in range(0, arkusz_wys, 100):
                dwg.add(
                    dwg.line(start=(0, i), end=(arkusz_szer, i), stroke='blue', stroke_width=1, stroke_dasharray='5,5'))

        for x, y, szer, wys in rozmieszczenie:
            dwg.add(dwg.rect(insert=(x, y), size=(szer, wys), fill='lightgray', stroke='black'))

            # Adnotacje z wymiarami elementów
            text_x = x + szer / 2
            text_y = y + wys / 2
            dwg.add(dwg.text(f"{szer}x{wys}", insert=(text_x, text_y), fill='black', font_size='20px',
                             text_anchor='middle'))

        dwg.save()
        print(f"✅ Plik {nazwa_pliku} został wygenerowany.")

