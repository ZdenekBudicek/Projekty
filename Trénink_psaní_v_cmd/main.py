import curses
from curses import wrapper
import time
import random


# Tento program lze spouštět jen v cmd, je nutno v cmd být ve složce kde je soubor a pak nainstalovat: pip install windows-curses
# pak dát python main.py v cmd
# Lze otevřít soubor normálně přes počítač a do cesty napsat cmd, to nám spustí cmd v dané cestě

def start_screen(stdscr):
    """
    vyčistí obrazovku a na ní zobrazí "Welcome to the Speed Typing Test!" a "Press any key to begin!".
    Po stisknutí libovolné klávesy se aktualizuje obrazovka.

    :param stdscr: je proměnná, která představuje okno terminálu, v tomto případě využitého pro výpis a zobrazování
    textu a informací o aplikaci. "curses" modul ji vytváří a poskytuje k ní rozhraní pro
    výpis a manipulaci s terminálovým oknem.
    """
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target, current, wpm=0):
    """
    Na obrazovku zobrazí cílový text a aktuální text uživatele, stejně jako rychlost psaní (WPM).
    Zeleně zobrazuje správně zadané znaky, červeně špatně.

    :param target: Náhodně vygenerovaná věta textu z proměnné target_text.
    :param current: Text psaný uživatelem, proměnná current_text.
    :param wpm: Začátek měřeného času
    :param stdscr: je proměnná, která představuje okno terminálu, v tomto případě využitého pro výpis a zobrazování
    textu a informací o aplikaci. "curses" modul ji vytváří a poskytuje k ní rozhraní pro
    výpis a manipulaci s terminálovým oknem.
    """
    stdscr.addstr(target)
    stdscr.addstr(5, 0, f"WPM: {wpm}")
    # Rozebere text vložený uživatelem na písmena
    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)


def load_text():
    """
     Načte text ze souboru "text.txt" a vrátí náhodný řádek.
    """
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()


def wpm_test(stdscr):
    """
    Slouží k testu rychlosti psaní. Získá cílový text pomocí funkce load_text, vytvoří prázdný aktuální
    text a inicializuje proměnnou WPM na 0. Nastavuje, že stdscr bude mít funkci non-blocking (nodelay).
    V cyklu se vykresluje obrazovka s aktualizovaným textem a WPM. Po dokončení psaní textu nebo stisku
    klávesy Esc se ukončí cyklus. Uživatel může psát text a stisknout klávesu backspace pro smazání znaku.
    """
    target_text = load_text()
    current_text = []
    start_time = time.time()
    # Nečekej než uživatel stiskne klávesu
    stdscr.nodelay(True)

    while True:
        # Čas se počítá tak že z velkého čísla se ty sekundy odečítají po té co se zavolá funkce time.time()
        # Takže prvotní funkce time.time() bude vždy menší než aktuální
        time_elapsed = max(time.time() - start_time, 1)
        # dělíme 5 jako odhadovaný průměr počtu znaků ve slově (takže máme kolik slov průměrně napíše uživatel za minutu)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)
        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()
        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break
        try:
            key = stdscr.getkey()
        except:
            continue
        # Restartuje čas pokud je text uživatele prázdný
        if not current_text:
            start_time = time.time()
        # Číslo 27 definuje klávesu esc, to nám umožní zavírat program
        if ord(key) == 27:
            break
        # Maže backspacem text
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(stdscr):
    """
    Inicializuje barevné schéma pro obrazovku a spouští funkci start_screen.
    Poté v nekonečném cyklu opakovaně spouští funkci wpm_test a po dokončení textu čeká na stisk libovolné klávesy.
    Pokud uživatel stiskne klávesu Esc, ukončí se celý program.
    """
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
        key = stdscr.getkey()

        if ord(key) == 27:
            break


# Funkce wrapper se volá s argumentem main, což inicializuje celý program a zajišťuje správné ukončení programu.
wrapper(main)
