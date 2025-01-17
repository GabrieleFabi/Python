def forma():
    print("quadrato: q")
    print("rettangolo: r")
    print("cerchio: c")
    print("triangolo: t")
    char = input("di che forma vuoi calcolare l'area? ")

    if char == "q":
        l = float(input("dammi un lato: "))
        return  l * l
    elif char == "r":
        b = float(input("dammi la base: "))
        a = float(input("dammi l'altezza: "))
        return b * a
    elif char == "c":
        r = float(input("dammi il raggio: "))
        return (r ** 2) * 3.14
    elif char == "t":
        bt = float(input("dammi la base: "))
        at = float(input("dammi l'altezza: "))
        return (bt * at) / 2

print(forma())