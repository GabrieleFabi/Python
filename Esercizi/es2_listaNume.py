x = 0

listaNume = [int(input("dammi un numero: "))]

while x==0:
    txt = input("vuoi inserire un'altro numero? (y/n)")
    if txt == "y":
        num = int(input("dammi un numero: "))
        listaNume.append(num)
        print(listaNume)
    else:
        x = 1

print(sum(listaNume))