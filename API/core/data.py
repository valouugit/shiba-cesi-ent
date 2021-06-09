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

    def product(self,action=None, name=None, price=None, stock=None, id_product=None):

        if self.manager:
            id_bde = self.cursor.execute("SELECT ID_BDE FROM BDE NATURAL JOIN USER WHERE Email='%s'" % self.email).fetchone()
            if action == 'create':
                self.cursor.execute("INSERT INTO PRODUCT ('Name','Price','Stock','Active', 'ID_BDE') VALUES ('%s', '%s', 0, 'True', '%s')" % (name, price, id_bde[0]))
                self.db.commit()
            if action == 'update':
                self.cursor.execute("UPDATE PRODUCT SET Price='%s', Stock='%s' WHERE ID_PRODUCT='%s'" % (price, stock, id_product))
                self.db.commit()
            if action == 'delete':
                self.cursor.execute("UPDATE PRODUCT SET Active = 'False' WHERE ID_PRODUCT='%s'" % (id_product))
                self.db.commit()
        else:
            raise Forbidden()