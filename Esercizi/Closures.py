#la funzione interna non è capace di prendere il valore della funzione esterna
"""def transmit_to_space(message):
    "This is the enclosing function"
    def data_transmitter():
        "The nested function"
        print(message)

    data_transmitter()

print(transmit_to_space("Test message"))"""

#per modificare la variabile passata alla funzione esterna  si usa nonlocal, che sovrascrive il valore
"""def print_msg(number):
    def printer():
        "Here we are using the nonlocal keyword"
        nonlocal number
        number=3
        print(number)
    printer()
    print(number)

print_msg(9)"""

#il vaore viene salvato visto che il risultato è la funzione(oggetto) stesso
def transmit_to_space(message):
  "This is the enclosing function"
  def data_transmitter():
      "The nested function"
      print(message)
  return data_transmitter

fun2 = transmit_to_space("Burn the Sun!")
fun2()

#la Closure mi permette di salvare il valore di una funzione anche dopo il suo termine

#esercizio
"""
def multiplier_of(n):
    def multiplier(number):
        return number*n
    return multiplier

multiplywith5 = multiplier_of(5)
print(multiplywith5(9))
"""

#chiamando odd sto chiamando la funzione interna, il valore di num è salvato quindi sale
#nel momento in cui chiamo odd2 sto chiamando la funzione esterna nuovamente, il che richrea la sua
#variabile num da 0 quindi vienere resettata
def calculate():
    num = 1
    def inner_func():
        nonlocal num
        num += 2
        return num
    return inner_func

# call the outer function
odd = calculate()

# call the inner function
print(odd())
print(odd())
print(odd())

# call the outer function again
odd2 = calculate()
print(odd2())
print(odd()) #il veccho numero continua a salire, non viene resettato