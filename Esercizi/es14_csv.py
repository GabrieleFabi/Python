import csv

def crea_file_csv(dizionario, nome_file):
    with open(nome_file, 'w', newline='') as file_csv:
        writer = csv.writer(file_csv)
        writer.writerow(['username', 'password', 'email', 'data_registrazione'])
        for utente in dizionario.values():
            writer.writerow([utente['username'], utente['password'], utente['email'], utente['data_registrazione']])

def leggi_file_csv(nome_file):
    with open(nome_file, 'r') as file_csv:
        reader = csv.reader(file_csv)
        for row in reader:
            print(row)


utenti = {
    1: {"username" : "ghostgga", "password": "Cia10", "email": "scimmiettarara@gmail.com", "data_registrazione": "15/01/25"},
    2: {"username" : "TostaPasta", "password": "Salto35", "email": "SimonePasta@gmail.com", "data_registrazione": "12/11/24"},
    3: {"username" : "Emiliano", "password": "Pischelle", "email": "EmiliaRomagna@gmail.com", "data_registrazione": "11/02/15"}
}

# Crea il file CSV
crea_file_csv(utenti, 'utenti.csv')

# Legge il file CSV e stampa i dati a schermo
leggi_file_csv('utenti.csv')