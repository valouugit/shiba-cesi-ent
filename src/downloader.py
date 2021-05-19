import requests
from pathlib import Path
from bs4 import BeautifulSoup

def download_pdf(token, server, email):
  try:
    # Récupération du codepersonne

    url = "https://ent.cesi.fr/mon-compte/mes-notes/"

    headers = {
      'Cookie': 'JSESSIONID=%s; SERVERID=%s' % (token, server)
    }

    res = requests.request("GET", url, headers=headers)

    soup = BeautifulSoup(res.text, 'html.parser')
    code = soup.find('div', {'class': 'semestres js-semestres'}).get('data-code-personne')

    # Récupération des pdf

    url = "https://ent.cesi.fr/api/semestre/all?codePersonne=%s" % code

    headers = {
      'Cookie': 'JSESSIONID=%s; SERVERID=%s' % (token, server)
    }

    res = requests.request("GET", url, headers=headers)
    res = res.json()
    semestres_list = res[0]["semestres"]

    directory = Path("data/%s" % email)
    directory.mkdir(parents=True, exist_ok=True)

    for semestre in semestres_list:
      headers = {
        'Cookie': 'JSESSIONID=%s; SERVERID=%s; sso=true' % (token, server)
      }
      pdf = requests.request("GET", url=semestre["urlDossier"], headers=headers, stream=True)
      with open('data/%s/semestre%s.pdf' % (email, semestre["numeroSemestre"]), 'wb') as f:
        f.write(pdf.content)
  except:
    return "error"