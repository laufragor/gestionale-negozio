import csv
import os
from sys import exit


CWD = os.getcwd()
STOCK_FILE = CWD + "/stock.csv"
STOCK_HEADERS = "nome,quantità,prezzo vendita,prezzo acquisto"
BALANCE_FILE = CWD + "/balance.txt"
BALANCE_FILE_SKELETON = "profitto_lordo 0\n" + "margine_netto_sulle_vendite 0\n" + "spese 0"


balance = {}
stock = {}


def load_data_from_files():
    """
    Loads stock data and shop balance data from files (which are created if not existing) into this software.
    """

    load_stock_from_file()
    load_balance_from_file()


def load_stock_from_file():
    """
    Loads the stock data from STOCK_FILE (which is created if not existing) into this software.
    """
    global stock
    stock = {}

    if not os.path.exists(STOCK_FILE):
        with open(STOCK_FILE, "w") as stock_file:
            stock_file.write(STOCK_HEADERS+"\n")
    
    with open(STOCK_FILE) as stock_file:
        csv_reader = csv.DictReader(stock_file)

        for product_details in csv_reader:
            stock[product_details["nome"]] = {
                "name":       product_details["nome"],
                "quantity":   int(product_details["quantità"]),
                "buy_price":  float(product_details["prezzo acquisto"]),
                "sell_price": float(product_details["prezzo vendita"])
            }

        print(stock)


def load_balance_from_file():
    """
    Loads the shop balance data from BALANCE_FILE (which is created if not existing) into this software.
    """
    global balance
    balance = {}

    if not os.path.exists(BALANCE_FILE):
        with open(BALANCE_FILE, "w") as balance_file:
            balance_file.write(BALANCE_FILE_SKELETON)
    
    with open(BALANCE_FILE) as balance_file:

        for line in balance_file.readlines():
            balance_entry, amount = line.split()
            amount = float(amount)

            if balance_entry == "profitto_lordo":
                balance["gross_profit"] = amount
            elif balance_entry == "margine_netto_sulle_vendite":
                balance["net_margin_on_sales"] = amount
            elif balance_entry == "spese":
                balance["expenses"] = amount


def translate_en_it(field: str):
    
    if field == "gross_profit":
        return "profitto_lordo"
    elif field == "net_margin_on_sales":
        return "margine_netto_sulle_vendite"
    elif field == "expenses":
        return "spese"
    

def get_valid_quantity():
    """
    Gets a valid integer quantity for a product.
    """

    quantity = None
    while quantity is None:
        try:
            quantity = int(input("Quantità: "))
        except Exception:
            print("Quantità non valida! Riprovare.")

    return quantity


def get_valid_price(prompt_msg: str):
    price = None
    while price is None:
        try:
            price = float(input(prompt_msg))
        except Exception:
            print("Prezzo non valido! Riprovare.")
    return price


def show_purchase_details(purchase_list: list):

    print("VENDITA REGISTRATA")
    for purchase_entry in purchase_list:
        product_name, quantity, unit_price, tot_price = purchase_entry
        print(f"{quantity} X {product_name}: €{unit_price:.2f}")

    print(f"Totale: €{sum(x[-1] for x in purchase_list):.2f}")


def is_purchase_finished():
    purchase_finished = None

    while purchase_finished is None:
        sell_another = input("Aggiungere un altro prodotto? (si/no): ")
        if sell_another == "no":
            purchase_finished = True
        elif sell_another == "si":
            purchase_finished = False
        else:
            print("Scelta non valida, riprovare.")

    return purchase_finished
        
    
def update_balance_file(field_to_update: str, amount_to_add: float):
    """
    Updates the given field of the shop balance by adding the given amount to it.
    """

    field_to_update = translate_en_it(field_to_update)
    lines = []

    with open(BALANCE_FILE) as balance_file:
        lines = balance_file.readlines()

        for i, line in enumerate(lines):

            if line.startswith(field_to_update):
                entry, amount = line.split()
                new_amount = str(float(amount) + amount_to_add)
                new_line = line.replace(amount, new_amount)
                # print(amount, new_amount, new_line)
                lines[i] = new_line
    
    with open(BALANCE_FILE, "w") as balance_file:
        balance_file.writelines(lines)


def add_to_stock_file(is_new_product: bool, product_name: str, quantity: int, sell_price: float=None, buy_price: float=None):
    """
    Adds one product to stock, and updates the shop balance accordingly.
    """

    if is_new_product:
        with open(STOCK_FILE, "a") as stock_file:
            csv_writer = csv.writer(stock_file)
            csv_writer.writerow([product_name, quantity, sell_price, buy_price])
    else:
        TMP_FILE_FOR_WRITING = STOCK_FILE + ".tmp.csv"

        with open(STOCK_FILE) as stock_file_in, open(TMP_FILE_FOR_WRITING, "w") as stock_file_out:
            csv_reader = csv.reader(stock_file_in)
            csv_writer = csv.writer(stock_file_out)

            for line in csv_reader:
                if line[0] == product_name:
                    line[1] = int(line[1]) + quantity
                    
                csv_writer.writerow(line)

            os.remove(STOCK_FILE)
            os.rename(TMP_FILE_FOR_WRITING, STOCK_FILE)         


def remove_from_stock_file(product_name: str, quantity: int):
    """
    Removes the given quantity of a product from the stock.csv file.
    """

    TMP_FILE_FOR_WRITING = STOCK_FILE + ".tmp.csv"

    with open(STOCK_FILE) as stock_file_in, open(TMP_FILE_FOR_WRITING, "w") as stock_file_out:
        csv_reader = csv.reader(stock_file_in)
        csv_writer = csv.writer(stock_file_out)

        headers = next(csv_reader)
        csv_writer.writerow(headers)

        for line in csv_reader:
            if line[0] == product_name:
                line[1] = int(line[1]) - quantity            
            if int(line[1]) > 0:
                csv_writer.writerow(line)

        os.remove(STOCK_FILE)
        os.rename(TMP_FILE_FOR_WRITING, STOCK_FILE)       


def is_product_in_stock(product_name: str):
    return product_name in stock.keys()


def add_new_product_to_stock(product_name: str, quantity: int, sell_price: float, buy_price: float):
    """
    Adds to stock a product that was not in stock, and updates the shop expenses.
    """

    stock[product_name] = {
        "name": product_name, "quantity": quantity, "sell_price": sell_price, "buy_price": buy_price
    }

    money_spent = quantity * buy_price
    balance["expenses"] += money_spent

    add_to_stock_file(is_new_product=True, product_name=product_name,
                      quantity=quantity, sell_price=sell_price, buy_price=buy_price)
    update_balance_file(field_to_update="expenses", amount_to_add=money_spent)


def add_existing_product_to_stock(product_name: str, quantity: int):
    """
    Adds some quantity to a product already in stock, and updates the shop expenses.
    """

    stock[product_name]["quantity"] += quantity

    money_spent = quantity * stock[product_name]["buy_price"]
    balance["expenses"] += money_spent

    add_to_stock_file(is_new_product=False, product_name=product_name, quantity=quantity)
    update_balance_file(field_to_update="expenses", amount_to_add=money_spent)


def sell_product_from_stock(product_name: str, quantity: int):
    """
    Gets one product and its quantity from user input, updates the shop balance and removes it from the stock.
    """

    if not is_product_in_stock(product_name):
        print("Prodotto non disponibile")
        return None
    
    if stock[product_name]["quantity"] < quantity:
        print("Errore: sono disponibili {} prodotti (richiesti {}). Vendita non effettuata.".format(
            stock[product_name]["quantity"], quantity
        ))
        return None

    # Update balance
    unit_price = stock[product_name]["sell_price"]
    cumulative_price = quantity * unit_price
    balance["gross_profit"] += cumulative_price

    cumulative_cost = quantity * stock[product_name]["buy_price"]
    balance["net_margin_on_sales"] += cumulative_price - cumulative_cost

    update_balance_file(field_to_update="gross_profit", amount_to_add=cumulative_price)
    update_balance_file(field_to_update="net_margin_on_sales", amount_to_add=cumulative_price-cumulative_cost)

    # Update stock
    if stock[product_name]["quantity"] == quantity:
        del stock[product_name]
    else:
        stock[product_name]["quantity"] -= quantity

    remove_from_stock_file(product_name, quantity)

    return [product_name, quantity, unit_price, cumulative_price]


###############################################################################
### All high-level functions are below
###############################################################################


def show_help_message():
    """
    Shows a help message with all the available commands.
    """
    
    print(
        """I comandi disponibili sono i seguenti:
        - aggiungi: aggiungi un prodotto al magazzino
        - elenca: elenca i prodotto in magazzino
        - vendita: registra una vendita effettuata
        - profitti: mostra i profitti totali
        - aiuto: mostra i possibili comandi
        - chiudi: esci dal programma
        """
    )


def menu_add_product_to_stock():
    """
    Gets one product from user input, adds it to the stock and updates the shop expenses.
    """
    
    product_name = input("Nome del prodotto: ")
    quantity = get_valid_quantity()  

    if is_product_in_stock(product_name):
        add_existing_product_to_stock(product_name, quantity)
    else:
        buy_price = get_valid_price(prompt_msg="Prezzo d'acquisto: ")
        sell_price = get_valid_price(prompt_msg="Prezzo di vendita: ")
        add_new_product_to_stock(product_name, quantity, sell_price, buy_price)
    
    print(f"AGGIUNTO: {quantity} X {product_name}")


def list_all_available_products():
    """
    Lists all the available products in stock.
    """
    
    if not stock:
        print("Nessun prodotto presente in magazzino.")
        return
    
    print("PRODOTTO QUANTITÀ PREZZO")

    for product_details in stock.values():
        print(product_details["name"],
              product_details["quantity"],
              "€%.2f" % product_details["sell_price"])


def menu_sell_products():
    """
    Gets products to purchase from user input and updates the stock and the profits accordingly.
    """
    
    purchase_list = []
    purchase_finished = False

    while not purchase_finished:
        product_name = input("Nome del prodotto: ")
        quantity = get_valid_quantity()
        
        purchase = sell_product_from_stock(product_name, quantity)
        if purchase:
            purchase_list.append(purchase)

        purchase_finished = is_purchase_finished()

    if purchase_list:
        show_purchase_details(purchase_list)
    else:
        print("Nessun prodotto comprato.")


def list_all_profits():
    """
    Lists gross and net profits for the shop.
    """
    
    gross_profit = float(balance["gross_profit"])
    net_margin_on_sales = float(balance["net_margin_on_sales"])

    print("Profitto: lordo = €{:.2f}, netto = €{:.2f}".format(
        gross_profit, net_margin_on_sales
    ))


def close_product_management_software():
    """
    Exits the software after showing a message.
    """
    
    print("Arrivederci!")
    exit(0)
