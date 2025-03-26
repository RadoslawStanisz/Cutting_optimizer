class Szafka:
    def __init__(self, szerokosc, wysokosc, glebokosc, ilosc=1, front="Normal"):
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc
        self.glebokosc = glebokosc
        self.front = front
        self.ilosc = ilosc
        self.powierzchnia_frontu = self.oblicz_powierzchnie_frontu() if front in ("Normal", "Special") else 0
        self.plyta_meblowa = []
        self.hdf_plecy = []
        self.akcesoria = {}

    def oblicz_powierzchnie_frontu(self):
        return (self.wysokosc - 3) * (self.szerokosc - 4) / 1000000 * self.ilosc  # m²


class SzafkaDolna(Szafka):
    def __init__(self, szerokosc, wysokosc, glebokosc, ilosc=1, front="Normal", liczba_polek=0, liczba_szuflad=0,
                 cargo=False, dodatkowe_nozki=0, wysokosc_trawersu=100):
        super().__init__(szerokosc, wysokosc, glebokosc, ilosc, front)
        self.liczba_polek = liczba_polek
        self.liczba_szuflad = liczba_szuflad
        self.cargo = cargo
        self.liczba_nozek = 4 + dodatkowe_nozki
        self.wysokosc_trawersu = wysokosc_trawersu
        self.rozloz_na_elementy()

    def rozloz_na_elementy(self):
        for _ in range(self.ilosc):
            self.plyta_meblowa += [
                (self.wysokosc, self.glebokosc),  # Bok lewy
                (self.wysokosc, self.glebokosc),  # Bok prawy
                (self.szerokosc - 36, self.glebokosc),  # Wieniec dolny
                (self.szerokosc - 36, self.wysokosc_trawersu),
                (self.szerokosc - 36, self.wysokosc_trawersu)
            ]
            self.plyta_meblowa += [(self.szerokosc - 36, self.glebokosc - 10)] * self.liczba_polek
            self.hdf_plecy.append((self.szerokosc - 4, self.wysokosc - 3))
            self.akcesoria['legs'] = self.liczba_nozek * self.ilosc

            if self.front == "Normal" and self.liczba_szuflad == 0 and not self.cargo:
                zawiasy = 2 if self.szerokosc <= 600 else 4
                self.akcesoria['hinges'] = zawiasy * self.ilosc
            elif self.front == "Special":
                self.akcesoria['sliding system'] = 1 * self.ilosc

            if self.liczba_szuflad > 0:
                self.akcesoria['drawers'] = self.liczba_szuflad * self.ilosc
            if self.cargo:
                self.akcesoria['cargo'] = 1 * self.ilosc


class SzafkaGorna(Szafka):
    def __init__(self, szerokosc, wysokosc, glebokosc, ilosc=1, front="Normal", liczba_polek=0):
        super().__init__(szerokosc, wysokosc, glebokosc, ilosc, front)
        self.liczba_polek = liczba_polek
        self.rozloz_na_elementy()

    def rozloz_na_elementy(self):
        for _ in range(self.ilosc):
            self.plyta_meblowa += [
                (self.wysokosc, self.glebokosc),  # Bok lewy
                (self.wysokosc, self.glebokosc),  # Bok prawy
                (self.szerokosc - 36, self.glebokosc),
                (self.szerokosc - 36, self.glebokosc - 20)
            ]
            self.plyta_meblowa += [(self.szerokosc - 36, self.glebokosc - 30)] * self.liczba_polek
            self.hdf_plecy.append((self.szerokosc - 18, self.wysokosc - 12))
            self.akcesoria['hanging brackets'] = 2 * self.ilosc

            if self.front == "Normal":
                zawiasy = 2 if self.wysokosc <= 900 else 3
                if self.szerokosc > 600:
                    zawiasy *= 2
                self.akcesoria['hinges'] = zawiasy * self.ilosc
            elif self.front == "Special":
                self.akcesoria['cabinet lifts'] = 2 * self.ilosc


class Wycena:
    def __init__(self):
        self.plyta_meblowa = []
        self.fronty_powierzchnia = 0.0
        self.hdf_plecy = []
        self.akcesoria = {}

    def dodaj_szafke(self, szafka):
        self.plyta_meblowa.extend(szafka.plyta_meblowa)
        self.hdf_plecy.extend(szafka.hdf_plecy)
        if szafka.front in ["Normal", "Special"]:
            self.fronty_powierzchnia += szafka.powierzchnia_frontu
        for klucz, wartosc in szafka.akcesoria.items():
            self.akcesoria[klucz] = self.akcesoria.get(klucz, 0) + wartosc

    def podsumowanie(self):
        return {
            'Płyta meblowa': self.plyta_meblowa,
            'Powierzchnia frontów (m²)': round(self.fronty_powierzchnia, 2),
            'HDF plecy': self.hdf_plecy,
            'Akcesoria': self.akcesoria
        }



