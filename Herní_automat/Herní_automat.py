import random

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 4,
    "B": 6,
    "C": 8,
    "D": 10
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}


def check_winnings(columns, lines, bet, values):
    """
    Kontrola výhry, pokud se písmena v řádku rovnají

    :param columns: náhodně vygenerované sloupce písmen v listu ve 3 členech
    :param lines: Počet řádků na které chce uživatel vsadit
    :param bet: Kolik chce uživatel vsadit
    :param values: Hodnoty písmen ze symbol_value
    """
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines


def get_slot_machine_spin(rows, cols, symbols):
    """
    Vytváří náhodně generované herní sloupce

    :param rows: Počet řádků, definováno na začátku programu ROWS
    :param cols: Počet sloupců, definováno na začátku programu COLS
    :param symbols: Počet jednotlivých symbolů, definováno na začátku programu symbol_count
    """
    all_symbols = []
    for symbol, symbol_number in symbols.items():
        for _ in range(symbol_number):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)

    return columns


def print_slot_machine(columns):
    """
    Převádíme list 3 proměnných na 3 sloupce a 3 řádky, hodnoty od sebe oddělujeme | až na tu poslední
    v řádku, dá nám to vizuální vzhled herního automatu.

    :param columns: Náhodně vygenerované znaky rozdělené do 3 sloupců v listu
    """
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")
        print()


def deposit():
    """
    Kolik chce uživatel vložit peněz do herního automatu
    """
    while True:
        amount = input("Kolik chceš dobít na účet? $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Hodnota musí být větší než 0.")
        else:
            print("Prosím vlož číslo.")

    return amount


def get_number_of_lines():
    """
    Na kolik řádků chce uživatel vsadit, vždycky se řádky počítejí pouze od vrchu
    """
    while True:
        lines = input(
            "Na kolik lajn chceš vsadit? (1-" + str(MAX_LINES) + ")? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Vlož hodnotu v rozsahu lajn.")
        else:
            print("Prosím vlož číslo.")

    return lines


def get_bet():
    """
    Kolik chce uživatel vsadit na každý řádek, pokud si jich vybral více.
    """
    while True:
        amount = input("Kolik chceš vsadit na lajnu? $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Hodnota musí být mezi ${MIN_BET} - ${MAX_BET}.")
        else:
            print("Prosím vlož číslo.")

    return amount


def spin(balance):
    """
    Kontrola jestli sázka je menší než balance, výpis kolik vsadil a na co,
    výpis kolik uživatel vyhrál a na jakém řádku

    :param balance: Vložená částka uživatelem
    """
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(
                f"Nemáte dost na vsazení této částky, váš aktuální zůstatek je: ${balance}")
            if balance == 0:
                main()
        else:
            break
    if lines == 1:
        print(f"Vsázíš ${bet} na {lines} lajnu. Celková sázka se rovná: ${total_bet}")
    else:
        print(f"Vsázíš ${bet} na {lines} lajny. Celková sázka se rovná: ${total_bet}")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    if winnings == 0:
        print("Nevyhrál jsi!")
    else:
        print(f"Vyhrál jsi ${winnings}.")
        print(f"Vyhrál jsi na lajně:", *winning_lines)
    return winnings - total_bet


def main():
    """
    Hlavní cyklus, ptá se na chod hry a vypisuje balance
    """
    balance = deposit()
    while True:
        print(f"Aktuální zůstatek je ${balance}")
        answer = input("Zmáčkni ENTER pokud chceš hrát (k pro ukončení).").lower()
        if answer == "k":
            break
        balance += spin(balance)

    print(f"Odešel si s ${balance}")


main()
