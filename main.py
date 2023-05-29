import utils


utils.load_data_from_files()
cmd = None

while True:
    cmd = input("Inserisci un comando: ")
    
    if cmd == "aiuto":
        utils.show_help_message()
    
    elif cmd == "aggiungi":
        utils.menu_add_product_to_stock()
        
    elif cmd == "elenca":
        utils.list_all_available_products()
        
    elif cmd == "vendita":
        utils.menu_sell_products()
        
    elif cmd == "profitti":
        utils.list_all_profits()
        
    elif cmd == "chiudi":
        utils.close_product_management_software()
        
    else:
        print("\nComando non valido.")
        utils.show_help_message()
