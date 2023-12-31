import csv, json, math

# 1. contruire le jardin:
def initialisation(v, s_deb, evite):
    attente = v.copy()
    for e in evite:
        if e in attente:
            attente.remove(e)

    d, parent = {}, {}
    for s in v:
        d[s] = math.inf
        parent[s] = None
    d[s_deb] = 0

    return attente, d, parent

def trouve_min(attente, d):
    arc_min = math.inf
    s_min = ''
    for s in attente:
        if d[s] < arc_min:
            arc_min = d[s]
            s_min = s
    return s_min

def maj_distances(s1, s2, d, poids, parent):
    if d[s2] > d[s1] + int(poids[s1][s2]):
        d[s2] = d[s1] + int(poids[s1][s2])
        parent[s2] = s1

def dijkstra(v, poids, s_deb, evite): 
    attente, d, parent = initialisation(v, s_deb, evite)

    while len(attente) > 0:
        s1 = trouve_min(attente, d)
        attente.remove(s1)

        if s1 in poids.keys():
              for s2 in poids[s1].keys():
                maj_distances(s1, s2, d, poids, parent)

    return d, parent

def plus_court_chemin(s1, s2, poids, v, evite):
    d, parent = dijkstra(v, poids, s1, evite)
    poid = d[s2]

    chemin = [s2]
    while parent[s2] != None:
        chemin.insert(0, parent[s2])
        s2 = parent[s2]

    return chemin, poid

with open('data_arcs_poids.csv','r',encoding='utf-8') as fich:
    csvReader = csv.reader(fich, delimiter=',')
    titres = csvReader.__next__()
    csvReader = list(csvReader)
    for i in range(len(csvReader)):
        csvReader[i] = csvReader[i][0].split(';')

dico_fav = {} # un dictionnaire des interactions de chaque espèce avec ses cibles.
for row in csvReader:
    if row[1] == 'favorise':
        if row[0] not in dico_fav.keys():
            dico_fav[row[0]] = {}
        dico_fav[row[0]][row[2]] = row[3]

with open('data_sommets_categories.csv','r',encoding='utf-8') as fich:
    csvReader = csv.reader(fich, delimiter=',')
    titres = csvReader.__next__()
    csvReader = list(csvReader)
    for i in range(len(csvReader)):
        csvReader[i] = csvReader[i][0].split(';')

s1, s2 = 'mais', 'carotte'
v = []
for row in csvReader:
    if row[1] != 'auxiliaire' and row[1] != 'nuisible':
        v.append(row[0])

print(dijkstra(v, dico_fav, s1, []))
# print(len(v))
chemin, poid = plus_court_chemin(s1, s2, dico_fav, v, [])
# evite = chemin[1:len(chemin) - 1]
# print(chemin,'-',poid)

# print(dico_fav['melon']['laitue'])
# print(dico_fav['laitue']['haricot'])
# print(dico_fav['haricot']['mais'])

# print()

# chemin, poid = plus_court_chemin('carotte', 'mais', dico_fav, v, [])
# print(chemin,'-',poid)

# print(dico_fav['mais']['pois'])
# print(dico_fav['pois']['coriandre'])
# print(dico_fav['coriandre']['carotte'])

# jar = ['melon', 'laitue', 'haricot', 'mais', 'haricot']