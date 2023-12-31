import csv
import json


def dico(csvReader, type):
    '''
    créer une dictionnaire de 'type' contenant des cibles comme les clés 
    et une liste des sources comme leur valeur.
    '''
    dico = {}
    for row in csvReader:
        if row[1] == type:
            dico[row[0]] = dico.get(row[0], []) + [row[2]]
    return dico

with open('data_arcs.csv','r',encoding='utf-8') as fich:
    csvReader = csv.reader(fich, delimiter=',')
    titres = csvReader.__next__()
    csvReader = list(csvReader)
    for i in range(len(csvReader)):
        csvReader[i] = csvReader[i][0].split(';')

dico_fav = dico(csvReader, 'favorise')
dico_defav = dico(csvReader, 'defavorise')
dico_attire = dico(csvReader, 'attire')
dico_repousse = dico(csvReader, 'repousse')


jar = ['melon', 'laitue', 'haricot', 'mais', 'haricot']


# 2. Analyser le jardin:
dico_jar_def = {}
for x in jar:
    x_defav = dico_defav.get(x)
    if x_defav != None:
        for y in jar:
            if y in x_defav:
                dico_jar_def[x] = y

print('les interactions négatives entre les parcelles')
print(dico_jar_def)
print()

# 3. rechercher les impacts des insectes sur les ingrédients.
with open('data_sommets_categories.csv','r',encoding='utf-8') as fich:
    csvReader = csv.reader(fich, delimiter=',')
    titres = csvReader.__next__()
    csvReader = list(csvReader)
    for i in range(len(csvReader)):
        csvReader[i] = csvReader[i][0].split(';')
    
dico_catégorie = {}
for (a,b) in csvReader:
    dico_catégorie[a] = b

# 3. Savoir si les parcelles attirent les auxiliaires ou les nuisibles:
dico_jar_att = {}
for c in jar:
    if c in dico_attire.keys():
        l = dico_attire[c]
        v = []
        for val in l:
            v.append([val,dico_catégorie[val]])
        dico_jar_att[c] = dico_attire[c]

print('Savoir si les parcelles attirent les auxiliaires')
print(dico_jar_att)
print()

# 4.Trouver les autres parcelles qui favorisent le jardin:
dico_jar_est_fav = {}
for c in jar:
    v = []
    for (c1,v1) in dico_fav.items():
        if c in v1:
            v.append(c1)
    dico_jar_est_fav[c] = v

print('Trouver les autres parcelles qui favorisent le jardin:')
# print(dico_jar_est_fav)
print()

# 5. Trouver les autres parcelles qui favorisent le jardin 
# sans défavoriser aucune autre parcelle dans le cercle
l_fav = [] # liste des parcelles qui favorisent le jardin 
# sans défavoriser aucune autre parcelle dans le cercle.
for v in dico_jar_est_fav.values():
    for val in v:
        if val not in l_fav and val not in jar:
            l_fav.append(val)
# print(len(l_fav))
            
# enlever si elle défavorise les parcelles dans le cercle.
for val in l_fav:
    if val in dico_defav.keys():
        v = dico_defav[val]
        i = 0
        enleve = False
        while i < len(jar) and not enleve:
            if jar[i] in v:
                l_fav.remove(val)
                enleve = True
            i += 1
            
print(len(l_fav))
print('Liste des parcelles qui favorisent le jardin ')
# print(l_fav)
print()
#######
# poid
with open('data_arcs_poids.csv','r',encoding='utf-8') as fich:
    csvReader = csv.reader(fich, delimiter=',')
    titres = csvReader.__next__()
    csvReader = list(csvReader)
    for i in range(len(csvReader)):
        csvReader[i] = csvReader[i][0].split(';')

interaction = {} # un dictionnaire des interactions de chaque espèce avec ses cibles.
for row in csvReader:
    if row[0] not in interaction.keys():
        interaction[row[0]] = {}
    if row[1] not in interaction[row[0]].keys():
        interaction[row[0]][row[1]] = {}
    interaction[row[0]][row[1]][row[2]] = row[3]

with open('interaction.json','w') as mon_fichier:
    json.dump(interaction,mon_fichier) 

#######
# 6. Trouver les autres parcelles qui attirent les auxiliaires:
dico = {}
for c in l_fav:
    if 'attire' in interaction[c].keys():
        dico[c] = interaction[c]

for v in dico.values():
    if 'mais' not in v['favorise'].keys() and 'melon' not in v['favorise'].keys():
        v.pop('favorise', None)
    com = 0
    if 'defavorise' in v.keys():
        for c1 in v['defavorise'].keys():
            if c1 not in dico.keys() and c1 not in jar:
                com += 1
        if com == len(v['defavorise'].keys()):
            del v['defavorise']

with open('dico.json','w') as mon_fichier:
    json.dump(dico,mon_fichier) 

#######
for i in range(len(jar)):
    if i == len(jar) - 1:
        i = -1
    print(f"{jar[i]} --> {jar[i+1]} {interaction[jar[i]]['favorise'][jar[i+1]]}")

dico_mais = {}
for (c,v) in interaction.items():
    if 'favorise' in v.keys():
        if 'mais' in v['favorise']:
            dico_mais[c] = v['favorise']['mais']

print(dico_mais)
# interaction entre les parcelles.