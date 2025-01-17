def contoAllaRovescia(n):
    if n <= 0:
        print("via!")
    else:
        print(n)
        contoAllaRovescia(n-1)

contoAllaRovescia(5)


#altro esempio

def stampa_n(s, n):
    if n <= 0:
        return
    print(s)
    stampa_n(s, n-1)

stampa_n(5, 10)