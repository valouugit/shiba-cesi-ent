import requests
from bs4 import BeautifulSoup
from core.error import *

class CesiAuth():

  def __init__(self):
    self.email, self.password = None, None

  def find_campus(self, html):

    # Le nom de la ville du campus se trouve dans la variable html

    if html.find("Reims"):
      return "Reims"
    else:
      return None

  def find_promo(self, html):

    # Le nom de la promo de l'élève se trouve dans la variable html

    pass

  def ent_auth(self, email, password):
    
    """
    
      Cette section contient 4 requêtes  http pour se connecter à l'ent
      Elle est masquée pour des raisons de sécurité
      Elle génère l'erreur UnknownLogin lorsque les identifiants sont incorrects
    
    """

    soup = BeautifulSoup(res.text, 'html.parser')
    ville_html = soup.find('a', {'class': 'sidebar-lien'}).get_text()
    
    ville = self.find_campus(ville_html)

    if res.status_code == 200:
      ent_cookie = session.cookies.get_dict()
      ENT_JSESSION_ID = ent_cookie['JSESSIONID']
      ENT_SERVER_ID = ent_cookie['SERVERID']
      self.email = email
      self.password = password
      return ENT_JSESSION_ID, ENT_SERVER_ID, ville

