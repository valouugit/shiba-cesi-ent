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
        
        def name_split(email):
            names = email.split('@')
            names = names[0].split('.')
            prenom, nom = names
            return prenom.title(), nom.upper()

        result = self.cursor.execute("SELECT Manager, Wallet FROM USER WHERE email='%s'" % self.email).fetchone()
        
        if result == None:
            result = self.cursor.execute("SELECT ID_BDE FROM BDE WHERE city='%s'" % self.ville).fetchone()
            if result == None:
                raise BDENotFound()
            else:
                prenom, nom = name_split(self.email)
                bde = result[0]
                self.cursor.execute("INSERT INTO USER ('LastName','FirstName','Email','ID_BDE', 'Manager', 'Wallet') VALUES ('%s', '%s', '%s', '%s', 'False', 0)" % (nom, prenom, self.email, bde))
                self.db.commit()
                return True
        else:
            self.manager = True if result[0] == 'True' else False
            self.wallet = result[1]
            return True

    def product(self,action=None, name=None, price=None, id=None):

        if self.manager:
            if action == 'create':
                id_bde = self.cursor.execute("SELECT ID_BDE FROM BDE NATURAL JOIN USER WHERE Email='%s'" % self.email).fetchone()
                self.cursor.execute("INSERT INTO PRODUCT ('Name','Price','Stock','Active', 'ID_BDE') VALUES ('%s', '%s', 0, 'True', '%s')" % (name, price, id_bde[0]))
                self.db.commit()
            if action == 'update':
                pass
        else:
            raise Forbidden()