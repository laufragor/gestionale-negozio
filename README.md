# Software gestionale di un negozio di alimentari
Progetto finale del corso in Python all'interno del Data Science Professional Path di ProfessionAI.  

Il software gestionale deve avere le seguenti funzionalità:
* Registrare nuovi prodotti, con nome, quantità, prezzo di vendita e prezzo di acquisto
* Elencare tutti i prodotti presenti
* Registrare le vendite effettuate
* Mostrare i profitti lordi e netti
* Mostrare un menu di aiuto con tutti i comandi disponibili


![img magazzino](warehouse.png)

I comandi disponibili sono i seguenti:
* **aggiungi**: aggiungi un prodotto al magazzino
* **elenca**: elenca i prodotti in magazzino
* **vendita**: registra una vendita effettuata
* **profitti**: mostra i profitti totali
* **aiuto**: mostra i possibili comandi
* **chiudi**: esci dal programma

Il programma è persistente e crea i file `stock.csv` e `balance.txt` per tenere traccia rispettivamente dei prodotti in magazzino e dei profitti. Inoltre ci si assicura che gli input inseriti dall'utente siano validi, ad esempio che i numeri siano effettivamente numeri, e vengono gestiti i casi non validi con eccezioni e messagi di errore.

### Esempio di interazione

```


Inserisci un comando: aggiungi
Nome del prodotto: latte
Quantità: 20
Prezzo di acquisto: 0.80
Prezzo di vendita: 1.40
AGGIUNTO: 20 X latte

Inserisci un comando: aggiungi
Nome del Prodotto: salmone
Quantità: 10
Prezzo di acquisto: 2.20
Prezzo di vendita: 4.19
AGGIUNTO: 10 X salmone

Inserisci un comando: aggiungi
Nome del prodotto: bistecca
Quantità: 5
Prezzo di acquisto: 3
Prezzo di vendita: 5.49
AGGIUNTO: 5 X bistecca

Inserisci un comando: elenca
PRODOTTO QUANTITÀ PREZZO
latte 20 €1.4
salmone 10 €4.19
bistecca 5 €5.49

Inserisci un comando: vendita
Nome del prodotto: latte
Quantità: 5
Aggiungere un altro prodotto? (si/no): si
Nome del prodotto: salmone
Quantità: 2
Aggiungere un altro prodotto? (si/no): no
VENDITA REGISTRATA
5 X latte: €1.40
2 X salmone: €4.19
Totale: €15.38

Inserisci un comando: elenca
PRODOTTO QUANTITÀ PREZZO
latte 15 €1.4
salmone 8 €4.19
bistecca 5 €5.49

Inserisci un comando: vendita
Nome del prodotto: bistecca
Quantità: 5
Aggiungere un altro prodotto? (si/no): no
VENDITA REGISTRATA
5 X bistecca: €5.49
Totale: €27.45

Inserisci un comando: elenca
PRODOTTO QUANTITÀ PREZZO
latte 15 €1.4
salmone 8 €4.19

Inserisci un comando: profitti
Profitto: lordo = €42.83 netto = €19.43

Inserisci un comando: storna
Comando non valido.
I comandi disponibili sono i seguenti:
- aggiungi: aggiungi un prodotto al magazzino
- elenca: elenca i prodotto in magazzino
- vendita: registra una vendita effettuata
- profitti: mostra i profitti totali
- aiuto: mostra i possibili comandi
- chiudi: esci dal programma

Inserisci un comando: chiudi
Bye bye
```
