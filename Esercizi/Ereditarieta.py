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




#altro esempio --------------------------------------------------------


class Persona:

    def __init__(self, nome, cognome, età, residenza):
        self.nome = nome
        self.cognome = cognome
        self.età = età
        self.residenza = residenza

    def scheda_personale(self):
        scheda = f"""
        Nome: {self.nome}
        Cognome: {self.cognome}
        Età: {self.età}
        Residenza: {self.residenza}\n"""
        return scheda

    def modifica_scheda(self):
        print("""Modifica Scheda:
        1 - Nome
        2 - Cognome
        3 - Età
        4 - Residenza""")
        scelta = input("Cosa Desideri modificare?")
        if scelta == "1":
            self.nome = input("Nuovo Nome--> ")
        elif scelta == "2":
            self. cognome = input("Nuovo Cognome --> ")
        elif scelta == "3":
            self.età = int(input("Nuova età --> "))
        elif scelta == "4":
            self.residenza = input("Nuova Residenza --> ")

class Studente(Persona):
    profilo = "Studente"

    def __init__(self,nome, cognome, età, residenza, corso_di_studio):
        super().__init__(nome, cognome, età, residenza)
        self.corso_di_studio = corso_di_studio

    def scheda_personale(self):
        scheda = f"""
        Profilo:{Studente.profilo}
        Corso di Studi:{self.corso_di_studio}
        ***"""
        return super().scheda_personale() + scheda

    def cambio_corso(self,corso):
        self.corso_di_studio = corso
        print(f"Corso Aggiornato")


class Insegnante(Persona):
    profilo = "Insegnante"

    def __init__(self,nome, cognome, età, residenza, materie=None):
        super().__init__(nome, cognome, età, residenza)
        if materie is None:
            self.materie = []
        else:
            self.materie = materie

    def scheda_personale(self):
        scheda = f"""
        Profilo:{Insegnante.profilo}
        Materie Insegnate:{self.materie}
        ***"""
        return super().scheda_personale() + scheda

    def aggiungi_materia(self,nuova):
        if nuova not in self.materie:
            self.materie.append(nuova)
        print("Elenco Aggiornato")