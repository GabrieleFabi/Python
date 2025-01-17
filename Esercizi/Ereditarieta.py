# definiamo una classe Person
class Person:
     # definiamo un __init__ che assegna nome e cognome all'istanza
     def __init__(self, name, surname):
         self.name = name
         self.surname = surname
     # definiamo un metodo "eat" che stampa un messaggio
     def eat(self, food):
         print(self.name, 'is eating', food)
     # definiamo un metodo "sleep" che stampa un messaggio
     def sleep(self):
         print(self.name, 'is sleeping')

# creiamo un'istanza di Person specificando nome e cognome
p = Person('Ezio', 'Melotti')
# verifichiamo il valore degli attributi name e surname

# verifichiamo che i metodi funzionino
p.eat('pizza')

p.sleep()


# definiamo una classe Employee che eredita da Person
class Employee(Person):
     # definiamo un nuovo __init__ che accetta nome/cognome/lavoro
     def __init__(self, name, surname, job):
         # chiamiamo l'__init__ della classe base (o superclasse)
         # che assegna nome e cognome all'istanza
         super().__init__(name, surname)
         # assegniamo il lavoro all'istanza
         self.job = job
     # definiamo un metodo aggiuntivo che stampa un messaggio
     def work(self):
         print(self.name, 'is working as a', self.job)

# creiamo un'istanza di Employee specificando nome/cognome/lavoro
e = Employee('Ezio', 'Melotti', 'developer')
# verifichiamo il valore degli attributi name e surname
e.name
'Ezio'
e.surname
'Melotti'
# verifichiamo il valore del nuovo attributo "job"
e.job
'developer'
# verifichiamo che i metodi ereditati da Person funzionino
e.eat('pizza')

e.sleep()

# verifichiamo che il nuovo metodo funzioni
e.work()
