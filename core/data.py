import sqlite3, os
from core.error import *

class ShibaData():

    def __init__(self, email, ville):
        self.email = email
        self.ville = ville
        self.db = sqlite3.connect('db/bde.db')
        self.cursor = self.db.cursor()

    def login(self):
        
        def name_split(email):
            names = email.split('@')
            names = names[0].split('.')
            prenom, nom = names
            return prenom.title(), nom.upper()

        result = self.cursor.execute("SELECT * FROM USER WHERE email='%s'" % self.email).fetchone()
        
        if result == None:
            result = self.cursor.execute("SELECT ID_BDE FROM BDE WHERE city='%s'" % self.ville).fetchone()
            if result == None:
                raise BDENotFound()
            else:
                prenom, nom = name_split(self.email)
                bde = result[0]
                self.cursor.execute("INSERT INTO USER ('LastName','FirstName','Email','ID_BDE') VALUES ('%s', '%s', '%s', '%s')" % (nom, prenom, self.email, bde))
                self.db.commit()
                return True
        else:
            return True