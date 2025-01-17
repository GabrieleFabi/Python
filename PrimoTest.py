print("hello, world!")

if 5 > 2:
    print("five is bigger than two")


x = 3
y = "stringa as variable"

#nome = input("inserisci un nome: ") #li puoi passare una stringa da stampare prima di prendere il valore, aspetta invio 
#input restituisce una stringa, se voglio salvare numeri o altro devo usare il casting
#numero = input("inserisci un numero: ")
#print(type(numero))
#n = int(numero) #salvo il numero su n come int
#print(n)

#commento


#divisione intera vs float
num1 = 8
num2 = 3
num3 = 2
ris1 = num1 / num2
ris2 = num1 // num3
ris3 = num1 / num3
print(type(ris1), "div con /: ", ris1)
print(type(ris1), "div con / e risultato int: ", ris3)
print(type(ris2), "div con //: ", ris2)

x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0
k = int('4')

y = int(2.8) # y will be 2, il cast di float va sempre arrotondando per min


#TUPLE
t = 'abc', 123, 45.67  # la virgola crea la tupla
t  # la rappresentazione di una tupla include sempre le ()
('abc', 123, 45.67)
type(t)

tp = ('abc', 123, 45.67)  # le () evitano ambiguità
t == tp  # il risultato è equivalente
True
len((1, 'a', 2.3))  # in questo caso le () sono necessarie


t = 'abc',  # tupla di un solo elemento
t
('abc',)
tv = ()  # tupla vuota, senza elementi
tv
()
type(tv)  # verifichiamo che sia una tupla

len(tv)  # verifichiamo che abbia 0 elementi


t = ('abc', 123, 45.67)
t[0]  # le tuple supportano indexing
'abc'
t[:2]  # slicing
('abc', 123)
123 in t  # gli operatori di contenimento "in" e "not in"
True
t + ('xyz', 890)  # concatenazione (ritorna una nuova tupla)
('abc', 123, 45.67, 'xyz', 890)
t * 2  # ripetizione (ritorna una nuova tupla)
('abc', 123, 45.67, 'abc', 123, 45.67)




print(k)
#print(k+"4") this wont work

x = "John"
# is the same as, non c'è differenza sono entrambe stringhe
x = 'John'

x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)
#sopra: variabili diverse. | sotto: variabili uguali
x = y = z = "Orange"
print(x)
print(y)
print(z)

#unpacking, assegna i valori di una lista alle variabili
fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)
print(y)
print(z)

#appende
x = "Python "
y = "is "
z = "awesome"
print(x + y + z)

#se devi stampare variabile + stringa usa la virgola
x = 5
y = "John"
print(x, y)


#variabili globali e funzioni
x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x) #variabile locale

myfunc()

print("Python is " + x) #variabile globale


#sovrascrive la variabile globale
x = "awesome"

def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x) #fantastic, anche se fuori da funzione



x = 5
print(type(x)) #ottieni il tipo della variabile


x = 1    # int
y = 2.8  # float
z = 1j   # complex


import random

print(random.randrange(1, 10))

"""
#ciclo for con range, range mi da una sqenza da 0 a n, o da range(start, stop).
#uso range per ciclare un numero specifico di volte
n = 8
for x in range(3):
  guess = int(input('Inserisci un numero da 1 a 10: '))
  if guess == n:
    print('Hai indovinato!')
    break  # numero indovinato, interrompi il ciclo
  else:
    print('Tentativi finiti. Non hai indovinato')
"""

#quotare tra virgolette
print("It's alright")
print("He is called 'Johnny'")
print('He is called "Johnny"') 


#assegnare più rige di string a una variabile con 3 virgolette o signole virgole, """ '''
a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)


#ogni singolo carattere è un array di string lungo 1, non esistono char in pythone
a = "Hello, World!"
print(a[1])



#loop in una stringa
for x in "banana":
  print(x)


#lungezza
a = "Hello, World!"
print(len(a))

#vedere se parola in frase
txt = "The best things in life are free!"
print("free" in txt)

txt = "The best things in life are free!"
if "free" in txt:
  print("Yes, 'free' is present.")



#slicing, prende i caratteri da 2 a 5 (esclusi)
b = "Hello, World!"
print(b[2:5])

#==ma da start a posizione 5
b = "Hello, World!"
print(b[:5])



#ritorna stringa in maiuscolo
a = "Hello, World!"
print(a.upper())

#ritorna stringa in minuscolo
a = "Hello, World!"
print(a.lower())


#rimpiazza H con J
a = "Hello, World!"
print(a.replace("H", "J"))



#unitre string con int
age = 36
txt = f"My name is John, I am {age}"
print(txt)

#le {} sono placeholders, possono contenere variabili, calcoli e funzioni

#fa il calcolo
txt = f"The price is {20 * 59} dollars"
print(txt)

#mette due decimali
price = 59 
txt = f"The price is {price:.2f} dollars" #59.00
print(txt)


#definisco un parametro di default, se non passo il parametro la funzione usera quello di def
def say_hello(name='World'):
  print('Hello {}!'.format(name))
  say_hello()

  say_hello('Python')

  say_hello(name='Python')



#escape characters
txt = "We are the so-called \"Vikings\" from the north."




a = 200
b = 33

if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")



#lista
thislist = ["apple", "banana", "cherry"]
print(thislist)

#lista che contiene tipi diversi
list1 = ["abc", 34, True, 40, "male"]


#if()else if()
a = 33
b = 33
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")



a = 200
b = 33
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")
else:
  print("a is greater than b")


#se hai solo uno statement
if a > b: print("a is greater than b")

#se hai solo uno statemnet con if else
a = 330
b = 330
print("A") if a > b else print("=") if a == b else print("B")


#or
a = 200
b = 33
c = 500
if a > b or a > c:
  print("At least one of the conditions is True")



#if nestled
x = 41

if x > 10:
  print("Above ten,")
  if x > 20:
    print("and also above 20!")
  else:
    print("but not above 20.")


#se hai un if vuoto e non vuoi avere errori
a = 33
b = 200

if b > a:
  pass




#while
i = 1
while i < 6:
  print(i)
  i += 1



#continiue, come un jump, evita di eseguire quando avviene quello
i = 0
while i < 6:
  i += 1
  if i == 3:
    continue
  print(i)




#convert from Json to Python
import json

# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York"}'

# parse x:
y = json.loads(x)

# the result is a Python dictionary:
print(y["age"])



#convert from Python to Json
import json

# a Python object (dict):
x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

# convert into JSON:
y = json.dumps(x)

# the result is a JSON string:
print(y)



#dizionario
thisdict = {
  "brand": "Ford",
  "electric": False,
  "year": 1964,
  "colors": ["red", "white", "blue"]
}

print(thisdict)


"""
#FILING
#read a file
f = open("demofile.txt") #ritorno un oggetto file con una funzione read()
print(f.read())

#different location
f = open("D:\\myfiles\welcome.txt", "r")
print(f.read())

#leggi solo i primi 5 caratteri
f = open("demofile.txt", "r")
print(f.read(5))

#legge una linea
f = open("demofile.txt", "r")
print(f.readline())

#loopa leggendo linea per linea 
f = open("demofile.txt", "r")
for x in f:
  print(x)

#chiudi file
f = open("demofile.txt", "r")
print(f.readline())
f.close()


#WRITE/CREATE
#Append
f = open("demofile2.txt", "a")
f.write("Now the file has more content!") 
f.close()

#open and read the file after the appending:
f = open("demofile2.txt", "r")
print(f.read())

#Overwrite
f = open("demofile3.txt", "w")
f.write("Woops! I have deleted the content!")
f.close()

#open and read the file after the overwriting:
f = open("demofile3.txt", "r")
print(f.read())


#crea nuovo file
f = open("myfile.txt", "x")



#DELETE
#rimuovi file
import os
os.remove("demofile.txt")

#controlla se esiste poi rimuovi
import os
if os.path.exists("demofile.txt"):
  os.remove("demofile.txt")
else:
  print("The file does not exist")

#elimina cartella, puo SOLO eliminare cartelle vuote
import os
os.rmdir("myfolder")
"""


#ECCEZIONI
#genera eccezione, perchè x non è definita
try:
  print(x)
except:
  print("An exception occurred")

#genera eccezione con errore
try:
  print(x)
except NameError:
  print("Variable x is not defined")
except:
  print("Something else went wrong")

#eccezione con if 
try:
  print("Hello")
except:
  print("Something went wrong")
else:
  print("Nothing went wrong")

#finally viene svolto in ogni caso, sia se l'eccezione è avvenuta o no
try:
  print(x)
except:
  print("Something went wrong")
finally:
  print("The 'try except' is finished")



# definiamo una classe che rappresenta un rettangolo generico
class Rectangle:
  def __init__(self, base, height):
    """Initialize the base and height attributes."""
    self.base = base
    self.height = height
  def calc_area(self):
    """Calculate and return the area of the rectangle."""
    return self.base * self.height
  def calc_perimeter(self):
    """Calculate and return the perimeter of a rectangle."""
    return (self.base + self.height) * 2
  

# creiamo un'istanza della classe Rectangle con base 3 e altezza 5
myrect = Rectangle(3, 5)
print(myrect.base)  # l'istanza ha una base

print(myrect.height)  # l'istanza ha un'altezza

print(myrect.calc_area())  # è possibile calcolare l'area direttamente

print(myrect.calc_perimeter())  # e anche il perimetro

#divisione tra float ed int
div1 = 2
div2 = 3.4
risDiv = div1 / div2
print(risDiv)
print(type(risDiv))

#puoi ritornare due variabili con lo stesso return
def midpoint(x1, y1, x2, y2):
  """Return the midpoint between (x1; y1) and (x2; y2)."""
  xm = (x1 + x2) / 2
  ym = (y1 + y2) / 2
  return xm, ym
x, y = midpoint(2, 4, 8, 12)
print(x)
print(y)
