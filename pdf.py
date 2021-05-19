import tabula, json

def pdf(email):
    files = ["semestre1.pdf","semestre2.pdf"]

    A = 0
    B = 0
    C = 0
    D = 0
    error = 0
    rattrapage = 0

    for file in files:

        #tables = tabula.read_pdf("%s/%s" % (email, file), pages = "all", multiple_tables = True)

        tabula.convert_into("data/%s/%s" % (email, file), "data/%s/temp.json" % email, output_format="json", pages='all')

        with open("data/%s/temp.json" % email, 'r') as file:
            res = json.load(file)
     
        for bloc_list_stock in res:
            bloc_list = bloc_list_stock["data"]
            for bloc in bloc_list:

                header = bloc[0]
                if int(header['width']) == 397:
                    note = bloc[1]
                    note = note['text']
                    name = bloc[0]
                    name = name['text']
                    #print("%s %s" % (note, name))
                elif int(header['width']) == 209:
                    note = bloc[2]
                    note = note['text']
                    name = bloc[0]
                    name = name['text']
                    if note == "A":
                        A += 1
                    elif note == "B":
                        B += 1
                    elif note == "C":
                        C += 1
                    elif note == "D":
                        D += 1
                    else:
                        if note.find("A") != -1:
                            A += 1
                            rattrapage += 1
                        elif note.find("B") != -1:
                            B += 1
                            rattrapage += 1
                        elif note.find("C") != -1:
                            C += 1
                            rattrapage += 1
                        elif note.find("D") != -1:
                            D += 1
                            rattrapage += 1
                        else:
                            error += 1

    return A,B,C,D,rattrapage