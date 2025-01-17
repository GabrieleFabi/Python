stud1 = {
    "nome": "Gabriele",
    "cognome": "Fabi",
    "classe": "5A",
    "voti": [6, 7, 4, 6, 6.5, 8, 4]
}

stud2 = {
    "nome": "Paolo",
    "cognome": "Brugnola",
    "classe": "5A",
    "voti": [7, 7, 9, 9, 8.5, 7, 8]
}

stud3 = {
    "nome": "Simone",
    "cognome": "Tami",
    "classe": "5A",
    "voti": [4, 4, 3, 6, 5.5, 4, 7]
}

scuola = [stud1, stud2, stud3]

def myScuola(lista):
    for n in lista:
        print(n["nome"])
        media = sum(n["voti"]) / len(n["voti"])
        print("la sua media è: ", media)

myScuola(scuola)