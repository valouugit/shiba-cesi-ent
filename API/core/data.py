import sqlite3, os
from core.error import *

class ShibaData():

    def __init__(self, email, ville):
        self.email = email
        self.ville = ville
        self.db = sqlite3.connect('db/cesi.db')
        self.cursor = self.db.cursor()
        self.wallet, self.manager = None, None

    def login(self):
        
        def name_split():
            names = self.email.split('@')
            names = names[0].split('.')
            prenom, nom = names
            return prenom.title(), nom.upper()


        result = self.cursor.execute("SELECT Manager, Wallet FROM USER WHERE email='%s'" % self.email).fetchone()
        
        if result == None:

            result = self.cursor.execute("SELECT ID_BDE FROM BDE WHERE city='%s'" % self.ville).fetchone()
            if result == None:
                bde = 0
            else:
                bde = result[0]

            prenom, nom = name_split()

            self.cursor.execute("INSERT INTO USER ('LastName','FirstName','Email','ID_BDE', 'Manager', 'Wallet') VALUES ('%s', '%s', '%s', '%s', 'False', 0)" % (nom, prenom, self.email, bde))
            self.db.commit()

        else:
            self.manager = True if result[0] == 'True' else False
            self.wallet = result[1]
            return True