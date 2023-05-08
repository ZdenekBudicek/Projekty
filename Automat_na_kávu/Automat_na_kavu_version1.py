from Source_Automat_kava import MENU
from Source_Automat_kava import resources

new_rescources = {}


def machine(supplies, roster, new_supplies):
    choice = input("Co by jste si dal/a? (espresso/latte/cappuccino): ").lower()
    # Admin
    if choice == "report":
        for supply in supplies:
            print(f"{supply}: {supplies[supply]}")
        machine(resources, MENU, new_rescources)

    # odečtení surovin
    elif choice == "espresso" or choice == "latte" or choice == "cappuccino":
        for one_supply in supplies:
            new_supplies[one_supply] = supplies[one_supply] - roster[choice]["ingredients"][one_supply]

        # Testovací výpis
        # print(new_supplies)

        # Podmínka na suroviny
        if new_supplies["water"] >= 0 and new_supplies["milk"] >= 0 and new_supplies["coffee"] >= 0:
            print(f"Na váš nápoj máme dostatek ingrediencí.")

            # Zkontroluj jestli uživatel zadal číslici
            def checkint(message):
                while True:
                    try:
                        coin = int(input(message))
                    except ValueError:
                        print("Nezadal jsi číselnou hodnotu! Zkus to znovu.")
                        continue
                    else:
                        return coin

            druhy_mince = [1, 2, 5, 10, 20, 50]
            result = 0
            price = roster[choice]['cost']

            # Mince
            print(f"Cena je: {price} Kč.")
            print(f"Prosím vložte mince 1, 2, 5, 10, 20, 50.")
            for cena in druhy_mince:
                mince = checkint(f"Kolik {cena} Kč chcete vložit?: ")
                mince_nasobeni = cena * mince
                result += mince_nasobeni
            print(f"Vložili jste {result} Kč.")

            if price > result:
                print("Vložili jste málo mincí, vracíme vám peníze a vyberte si nápoj znovu!")
                machine(resources, MENU, new_rescources)
            elif price == result:
                print("Váš nápoj připravujeme.")
                for supp in supplies:
                    supplies[supp] = new_supplies[supp]
                machine(resources, MENU, new_rescources)
            else:
                print("Váš nápoj připravujeme.")
                back = result - price
                print(f"Zde jsou peníze zpět: {back} Kč")
                for supp in supplies:
                    supplies[supp] = new_supplies[supp]
                machine(resources, MENU, new_rescources)
        else:
            print(f"Je mi líto na váš nápoj nemáme dostatek ingrediencí.")
    else:
        print(f"Špatně napsaný nápoj, zkus to znovu!")
        machine(resources, MENU, new_rescources)


machine(resources, MENU, new_rescources)
