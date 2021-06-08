from core.ent import CesiAuth
from core.error import *
import tabula, json, requests
from pathlib import Path
from bs4 import BeautifulSoup

class ShibaJudge():

    def __init__(self):
        self.discord_id = None
        self.email, self.passord = None, None
        self.token, self.server = None, None
        self.ville = None

    def log(self, message):
        print("[Shiba] %s" % message)

    def set_discord(self, discord_id):
        self.discord_id = discord_id

    def set_login(self, email, password):
        self.email = email
        self.passord = password

    def get_token(self):
        return self.token
    
    def get_ville(self):
        return self.ville

    def auth(self, email, password):
        if self.email == None or self.passord == None:
            self.set_login(email, password)
        cesi = CesiAuth()
        try:
            self.token, self.server, self.ville = cesi.ent_auth(email, password)
            return True
        except UnknownLogin:
            return False
        except:
            raise ErrorFatal

    def download(self):
        
        if self.token == None:
            if self.email != None:
                if self.auth(self.email, self.passord):
                    self.download()
                return True
            else:
                return False
        else:
            try:
                # Récupération du codepersonne
                res = requests.request("GET", "https://ent.cesi.fr/mon-compte/mes-notes/", headers={'Cookie': 'JSESSIONID=%s; SERVERID=%s' % (self.token, self.server)})

                soup = BeautifulSoup(res.text, 'html.parser')
                code = soup.find('div', {'class': 'semestres js-semestres'}).get('data-code-personne')

                # Récupération des pdf
                res = requests.request("GET", "https://ent.cesi.fr/api/semestre/all?codePersonne=%s" % code, headers={'Cookie': 'JSESSIONID=%s; SERVERID=%s' % (self.token, self.server)})
                res = res.json()
                
                directory = Path("data/%s" % self.email)
                directory.mkdir(parents=True, exist_ok=True)

                semestres_list = res[0]["semestres"]
                for semestre in semestres_list:
                    pdf = requests.request("GET", url=semestre["urlDossier"], headers={'Cookie': 'JSESSIONID=%s; SERVERID=%s; sso=true' % (self.token, self.server)}, stream=True)
                    with open('data/%s/semestre%s.pdf' % (self.email, semestre["numeroSemestre"]), 'wb') as f:
                        f.write(pdf.content)
                return True
            except:
                return False
        
    def pdf(self, detailed=False):

        if self.email == None:
            print("ERROR {%s} Besoin de l'email pour lire pdf")

        files = ["semestre1.pdf","semestre2.pdf"]

        A = 0
        B = 0
        C = 0
        D = 0
        error = 0
        rattrapage = 0
        detail = []

        for file in files:
            tabula.convert_into("data/%s/%s" % (self.email, file), "data/%s/temp.json" % self.email, output_format="json", pages='all')
            with open("data/%s/temp.json" % self.email, 'r') as file:
                res = json.load(file)
            for bloc_list_stock in res:
                bloc_list = bloc_list_stock["data"]
                for bloc in bloc_list:
                    noted = False
                    header = bloc[0]
                    if int(header['width']) == 397:
                        note_bloc = bloc[1]
                        note_bloc = note_bloc['text']
                        name_bloc = bloc[0]
                        name_bloc = name_bloc['text']
                        if note_bloc != "":
                            detail.append("\n**%s   %s**\n" % (note_bloc, name_bloc))
                    elif int(header['width']) == 209:
                        note = bloc[2]
                        note = note['text']
                        name = bloc[0]
                        name = name['text']
                        if note == "A":
                            A += 1
                            noted = True
                        elif note == "B":
                            B += 1
                            noted = True
                        elif note == "C":
                            C += 1
                            noted = True
                        elif note == "D":
                            D += 1
                            noted = True
                        else:
                            if note.find("A") != -1:
                                A += 1
                                noted = True
                                note = "A"
                                rattrapage += 1
                            elif note.find("B") != -1:
                                B += 1
                                noted = True
                                note = "B"
                                rattrapage += 1
                            elif note.find("C") != -1:
                                C += 1
                                noted = True
                                note = "C"
                                rattrapage += 1
                            elif note.find("D") != -1:
                                D += 1
                                noted = True
                                note = "D"
                                rattrapage += 1
                            else:
                                error += 1
                        if noted:
                            #detail.append("**%s** %s" % (note, name))
                            #detail.append(name)
                            pass

        if detailed:
            return detail
        else:
            return A,B,C,D,rattrapage
        

