import sqlite3, os
from core.error import *

class ShibaData():

    def __init__(self, email):
        self.email = email
        self.db = sqlite3.connect('/home/valouu/Documents/shiba/API/db/cesi.db')
        self.cursor = self.db.cursor()

    """
    
        Permet de se connecter à la bdd de manière dynamique,
        Création du compte automatiquement si il n'existe pas encore,
        La fonction doit être utilisée si l'authentification est déjà réalisée

    """

    def login(self):
        
        # Extrait le nom/prénom depuis l'email

        def name_split():
            names = self.email.split('@')
            names = names[0].split('.')
            prenom, nom = names
            return prenom.title(), nom.upper()

        # Push le compte dans la base de données
        # {prenom_nom} tableau avec ['prenom', 'nom'] venant de la fonction name_split()

        def register_in_db(prenom_nom , bde):
            self.cursor.execute("INSERT INTO USER ('LastName','FirstName','Email') VALUES ('%s', '%s', '%s')" % (prenom_nom[0], prenom_nom[1], self.email))
            self.db.commit()

        # Récupere les données de l'utilisateur
        # {result} retourne 'None' si le compte est non engregistré

        result = self.cursor.execute("SELECT Manager, Wallet FROM USER WHERE email='%s'" % self.email).fetchone()
        
        if result == None:

            # Enregistre le nouveau compte dans la base de données

            register_in_db(name_split())
