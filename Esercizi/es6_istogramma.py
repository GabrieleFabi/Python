"""
def istogramma(valori):
    disegno = ""
    a = 0
    for n in valori:
        while a < n:
            disegno += "*"
            a += 1
        print(disegno)
        disegno = ""
        a = 0

lista = [1, 2, 3, 2, 1]
istogramma(lista)
"""

lista = [1, 2, 3, 2, 1]

def istogramma(lista):
    for numero in lista:
        print("*" * numero)

istogramma(lista)       