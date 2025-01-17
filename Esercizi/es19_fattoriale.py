def fattoriale(n):
    if n == 0:
        return 1
    else:
        ricors = fattoriale(n-1)
        ris = n * ricors
        return ris
    
print(fattoriale(3))