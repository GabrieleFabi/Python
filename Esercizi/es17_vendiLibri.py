scaffale = {"l'amore nel gielo": 7, "un anno nell'altipiano": 10, "ultimo giorno": 1, "due giorni": 2 }
ordini = []

def vendiLibri(scaffale, libro):
    vendita = False
    if libro in scaffale:
        vendita = True
        scaffale[libro] -= 1
        print(f"il libro '{libro}' è stato venduto")
        if scaffale[libro] == 0:
            del scaffale[libro]
            print("i volumi di questo libro sono finiti, li sto riordinando")
            ordini.append(libro)
    else:
        print(f"il libro richiesto: '{libro}' non è disponibile, sto effetuando l'ordine")
        ordini.append(libro)
    print("ecco il nuovo elenco: ")
    print(scaffale)
    print("ecco gli ordini")
    print(ordini)
    return vendita

vendiLibri(scaffale, "giorno")