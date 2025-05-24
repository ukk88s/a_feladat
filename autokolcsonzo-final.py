from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


class Auto(ABC):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: int):
        self.rendszam = rendszam
        self.tipus = tipus
        self.berleti_dij = berleti_dij

    @abstractmethod
    def __str__(self):
        pass


class Szemelyauto(Auto):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: int, ajtok_szama: int):
        super().__init__(rendszam, tipus, berleti_dij)
        self.ajtok_szama = ajtok_szama

    def __str__(self):
        return f"Személyautó - {self.rendszam} ({self.tipus}), Ajtók: {self.ajtok_szama}, Díj: {self.berleti_dij} Schmeckles/nap"


class Teherauto(Auto):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: int, terheles: int):
        super().__init__(rendszam, tipus, berleti_dij)
        self.terheles = terheles

    def __str__(self):
        return f"Teherautó - {self.rendszam} ({self.tipus}), Terhelés: {self.terheles} kg, Díj: {self.berleti_dij} Schmeckles/nap"


class Berles:
    def __init__(self, auto: Auto, kezdo_datum: str, veg_datum: str):
        self.auto = auto
        self.kezdo_datum = kezdo_datum
        self.veg_datum = veg_datum
        self.aktiv = True

    def __str__(self):
        statusz = "Aktív" if self.aktiv else "Törölve"
        return f"{self.auto.rendszam} - {self.kezdo_datum} -> {self.veg_datum} - {statusz}"


class Autokolcsonzo:
    def __init__(self, nev: str):
        self.nev = nev
        self.autok: List[Auto] = []
        self.berlesek: List[Berles] = []

    def hozzaad_auto(self, auto: Auto):
        self.autok.append(auto)

    def hozzaad_berles(self, berles: Berles):
        self.berlesek.append(berles)

    def listaz_autok(self):
        print(f"--- Autók a(z) {self.nev} kölcsönzőben ---")
        for auto in self.autok:
            print(auto)

    def listaz_berlesek(self):
        print(f"--- Bérlések a(z) {self.nev} kölcsönzőben ---")
        for idx, berles in enumerate(self.berlesek):
            if berles.aktiv:
                print(f"{idx + 1}. {berles}")

    def auto_foglalt(self, rendszam: str, kezdo: datetime, veg: datetime):
        for berles in self.berlesek:
            if berles.auto.rendszam == rendszam and berles.aktiv:
                b_start = datetime.strptime(berles.kezdo_datum, "%Y-%m-%d")
                b_end = datetime.strptime(berles.veg_datum, "%Y-%m-%d")
                if b_start <= veg and kezdo <= b_end:
                    return True
        return False

    def berel_auto(self, rendszam: str, kezdo_datum: str, veg_datum: str):
        try:
            kezdo = datetime.strptime(kezdo_datum, "%Y-%m-%d")
            veg = datetime.strptime(veg_datum, "%Y-%m-%d")
            if veg < kezdo:
                print("A végdátum nem lehet korábbi, mint a kezdődátum.")
                return
        except ValueError:
            print("Érvénytelen dátumformátum! Használja: ÉÉÉÉ-HH-NN")
            return

        auto = next((a for a in self.autok if a.rendszam == rendszam), None)
        if not auto:
            print("Nincs ilyen rendszámú autó.")
            return

        if self.auto_foglalt(rendszam, kezdo, veg):
            print("Ez az autó nem elérhető az adott időszakban.")
            return

        napok_szama = (veg - kezdo).days + 1
        osszeg = napok_szama * auto.berleti_dij
        print(f"Bérlés időtartama: {napok_szama} nap. Összeg: {osszeg} Schmeckles")

        megerosites = input("Jóváhagyod a bérlést? (i/n): ").strip().lower()
        if megerosites == "i":
            uj_berles = Berles(auto, kezdo_datum, veg_datum)
            self.hozzaad_berles(uj_berles)
            print("Bérlés sikeresen rögzítve.")
        else:
            print("Bérlés megszakítva.")

    def lemond_berles(self, index: int):
        if 0 <= index < len(self.berlesek) and self.berlesek[index].aktiv:
            self.berlesek[index].aktiv = False
            print("Bérlés sikeresen lemondva.")
        else:
            print("Érvénytelen bérlés azonosító vagy már törölve.")


def konzol_menu(kolcsonzo: Autokolcsonzo):
    while True:
        print(f"\n--- {kolcsonzo.nev.upper()} - MENÜ ---")
        print("1. Autó bérlése")
        print("2. Bérlés lemondása")
        print("3. Bérlések listázása")
        print("4. Autók listázása")
        print("0. Vissza")
        valasztas = input("Válassz egy opciót: ")

        if valasztas == "1":
            kolcsonzo.listaz_autok()
            rendszam = input("Add meg a kiválasztott autó rendszámát: ").strip().upper()
            kezdo = input("Bérlés kezdete (ÉÉÉÉ-HH-NN): ").strip()
            veg = input("Bérlés vége (ÉÉÉÉ-HH-NN): ").strip()
            kolcsonzo.berel_auto(rendszam, kezdo, veg)

        elif valasztas == "2":
            kolcsonzo.listaz_berlesek()
            try:
                idx = int(input("Add meg a lemondandó bérlés sorszámát: ")) - 1
                kolcsonzo.lemond_berles(idx)
            except ValueError:
                print("Hibás bemenet. Kérlek számot adj meg.")

        elif valasztas == "3":
            kolcsonzo.listaz_berlesek()

        elif valasztas == "4":
            kolcsonzo.listaz_autok()

        elif valasztas == "0":
            break

        else:
            print("Érvénytelen választás. Próbáld újra.")


if __name__ == "__main__":
    kolcsonzo1 = Autokolcsonzo("Star Wars Autókölcsönző")
    # kolcsonzo2 = Autokolcsonzo("Pokemon Autókölcsönző")

    auto1 = Szemelyauto("DOG001", "Trabant", 9500, 4)
    auto2 = Teherauto("CAT321", "Man Kamion", 18000, 12000)
    auto3 = Szemelyauto("GTR034", "VW Corrado", 11000, 5)
    auto4 = Teherauto("HMM420", "Mercedes F1", 20000, 1600)

    kolcsonzo1.hozzaad_auto(auto1)
    kolcsonzo1.hozzaad_auto(auto2)
    kolcsonzo1.hozzaad_auto(auto3)
    # kolcsonzo1.hozzaad_auto(auto4)

    kolcsonzo1.hozzaad_berles(Berles(auto1, "2025-01-24", "2025-03-25"))
    kolcsonzo1.hozzaad_berles(Berles(auto2, "2025-02-25", "2025-02-26"))
    kolcsonzo1.hozzaad_berles(Berles(auto3, "2025-04-01", "2025-04-27"))
    kolcsonzo1.hozzaad_berles(Berles(auto2, "2025-06-28", "2025-07-05"))

    kolcsonzok = [kolcsonzo1]

    while True:
        print("\n--- KÖLCSÖNZŐ VÁLASZTÓ ---")
        for idx, k in enumerate(kolcsonzok):
            print(f"{idx + 1}. {k.nev}")
        print("0. Kilépés")
        valasztas = input("Válassz egy kölcsönzőt (szám): ")

        if valasztas == "0":
            print("Kilépés a rendszerből. Viszlát!")
            break
        try:
            index = int(valasztas) - 1
            if 0 <= index < len(kolcsonzok):
                konzol_menu(kolcsonzok[index])
            else:
                print("Nincs ilyen sorszámú kölcsönző.")
        except ValueError:
            print("Kérlek számot adj meg.")
