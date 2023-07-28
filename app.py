# source de l'exercice :
# https://www.digitalocean.com/community/tutorials/how-to-create-your-first-web-application-using-flask-and-python-3

import sqlite3
from os import path
from flask import Flask
from flask import render_template
from flask import request

PROJECT_ROOT = path.dirname(path.realpath(__file__))
DATABASE_PATH = path.join(PROJECT_ROOT, "database.db")

app = Flask(__name__)


# La liste des critères avec leur nom interne et leur nom d'affichage
criteres = [
    {
        "id": "rapidite",
        "nom": "Rapidité",
    },
    {
        "id": "enjeu",
        "nom": "Pour enjeu",
    },
    {
        "id": "simplicite",
        "nom": "Simplicité",
    },
    {
        "id": "taille_groupe",
        "nom": "Pour taille de groupe",
    },
    {
        "id": "adhesion",
        "nom": "Niveau d'adhésion généré",
    },
]
# toutes les caractéristiques qui peuvent être affichées dans un processus
caracteristiques = [
    {
        "id": "avantages",
        "nom": "Avantages",
        "couleur": "lightgreen",
    },
    {
        "id": "adapte",
        "nom": "Adapté",
        "couleur": "lightblue",
    },
    {
        "id": "risques",
        "nom": "Risques",
        "couleur": "#fce1bb",
    },
    {
        "id": "inconvenients",
        "nom": "Inconvénients",
        "couleur": "lightcoral",
    },
    {
        "id": "deconseille",
        "nom": "Déconseillé",
        "couleur": "#ff9259",
    },
    {
        "id": "points_cles",
        "nom": "Points clés",
        "couleur": "lightgoldenrodyellow",
    },
]


def debug_var(var):
    """pour débuguer les variables."""
    print("=============== DEBUG ==============")
    print(f"type(var) = {type(var)}")
    print(f"var = {var}")
    print("================ FIN ===============")


@app.template_filter()
def crit_filter(crit):
    """Renvoie la valeur de l'opacité en fonction du code du critère."""
    result = {
        "0": "0",
        "1": "0.5",
        "2": "1",
    }
    return result[crit]


def get_db_connection():
    """Renvoie une connexion à la base de données."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def retourne_un_processus(id_processus) -> dict:
    """Retourne uniquement un processus.
    Prend l'ID du processus en argument.
    Renvoie un dictionnaire"""
    conn = get_db_connection()
    req_select = """SELECT *
    FROM processus
    WHERE id = ?
    LIMIT 1"""
    result = conn.execute(req_select, [id_processus]).fetchall()
    conn.close()
    return result


def retourne_toutes_les_familles() -> list:
    """Retourne tous les processus de la base de données.
    Renvoie une liste de dictionnaire."""
    conn = get_db_connection()
    req_select = """SELECT *
    FROM processus
    WHERE id % 100 = 0"""
    result = conn.execute(req_select).fetchall()
    conn.close()
    return result


def retourne_tous_les_processus_dune_famille(id_famille) -> list:
    """Retourne tous les processus de la base de données.
    Renvoie une liste de dictionnaire."""
    conn = get_db_connection()
    req_select = """SELECT *
    FROM processus
    WHERE id > ?
    AND id < ?"""
    parameters = [id_famille, id_famille + 100]
    result = conn.execute(req_select, parameters).fetchall()
    conn.close()
    return result


def retourne_tous_les_processus() -> list:
    """Retourne tous les processus de la base de données.
    Renvoie une liste de dictionnaire."""
    conn = get_db_connection()
    req_select = """SELECT *
    FROM processus"""
    result = conn.execute(req_select).fetchall()
    conn.close()
    return result


def retourne_les_processus_par_famille() -> dict:
    """Retourne tous les processus par famille, classé dans un dictionnaire :
    {
        <famille 100>: [<processus 101>, <processus 102>, ...],
        <famille 200>: [],
        ...
    }
    """
    retour = {}
    for famille in retourne_toutes_les_familles():
        retour[famille] = retourne_tous_les_processus_dune_famille(famille["id"])
    return retour


@app.route("/")
@app.route("/index/")
@app.route("/index.html")
def index():
    """Renvoie la page d'accueil"""
    processus_par_famille = retourne_les_processus_par_famille()
    return render_template(
        "index.html",
        processus_par_famille=processus_par_famille,
    )


@app.route("/processus/<id_processus>")
def get_processus(id_processus):
    """Affiche le détail d'un processus."""
    result = retourne_un_processus(id_processus)
    if len(result) > 0:
        processus = result[0]
        return render_template(
            "processus.html",
            processus=processus,
            caracteristiques=caracteristiques,
            criteres=criteres,
        )
    return "processus introuvable."


def get_processus_score_criteres(processus, criteres_voulus) -> int:
    """Retourne le score d'un processus par rapport aux critères voulus.
    le processus est l'objet retourné par fetchall() de la DB
    Les criteres_voulus sont de cette forme :
    criteres_voulus = {
        "rapidite": 4,
        "enjeu": 7,
    }
    La valeur pour les critères voulus doit être comprise entre 0 et 13 compris.

    Pour chaque critère, le processus gagne les points suivants :
        - 10 si c'est du vert foncé ;
        - 5 si c'est du vert clair ;
        - -5 si c'est du blanc.
    + pour chaque carré adjacent (à 1 de distance) :
        - 6 si c'est du vert foncé ;
        - 2 si c'est du vert clair ;
        - -2 si c'est du blanc ;
    + pour chaque carré à 2 de distance :
        - 3 si c'est du vert foncé ;
        - 1 si c'est du vert clair ;
        - -1 si c'est du blanc.

    Exemple : je veux une rapidité de 5 :

    00022100000000
        ^
    indice voulu

    alors score = 10 + 6 + 2 - 1 - 1 = 16
    """

    def get_affinity(critere_processus, indice_voulu, adjacent=0) -> int:
        scoring = {
            # sur le bon indice (0 de distance)
            0: {
                # couleur du carré = score
                2: 10,
                1: 5,
                0: -5,
            },
            # à 1 de distance
            1: {
                2: 6,
                1: 2,
                0: -2,
            },
            # à 2 de distance
            2: {
                2: 3,
                1: 1,
                0: -1,
            },
        }
        return scoring[abs(adjacent)][int(critere_processus[indice_voulu + adjacent])]

    score = 0
    for critere_voulu in criteres_voulus:
        # obtention du score pour la valeur demandée
        indice_voulu = int(criteres_voulus[critere_voulu])
        score += get_affinity(processus[critere_voulu], indice_voulu)
        # évolution du score grâce aux valeurs adjacentes (à 1 de distance)
        if indice_voulu > 0:
            score += get_affinity(processus[critere_voulu], indice_voulu, -1)
        if indice_voulu < 13:
            score += get_affinity(processus[critere_voulu], indice_voulu, 1)
        # évolution du score grâce aux valeurs adjacentes (à 2 de distance)
        if indice_voulu > 1:
            score += get_affinity(processus[critere_voulu], indice_voulu, -2)
        if indice_voulu < 12:
            score += get_affinity(processus[critere_voulu], indice_voulu, 2)
    return score


def get_processus_score_mots_cles(processus, mots_cles):
    score = 0
    for mot_cle in mots_cles:
        if mot_cle in processus["titre"]:
            score += 50
        if mot_cle in processus["adapte"]:
            score += 10
        if mot_cle in processus["avantages"]:
            score += 10
        if mot_cle in processus["points_cles"]:
            score += 2
        if mot_cle in processus["description"]:
            score += 1
    return score


@app.route("/recherche_criteres")
def get_recherche_criteres():
    """Fonction de recherche par critères."""
    id_criteres = [i["id"] for i in criteres]
    criteres_voulus = {}
    for id_critere in id_criteres:
        if id_critere in request.args:
            criteres_voulus[id_critere] = request.args.get(id_critere)
    score_processus = {}
    for processus in retourne_tous_les_processus():
        score = get_processus_score_criteres(processus, criteres_voulus)
        score_processus[processus] = score
    return tri_et_retourne_resultats(score_processus)


@app.route("/recherche_mots-cles")
def get_recherche_mots_cles():
    """Fonction de recherche par mots clés."""
    if (
        "mots-cles" not in request.args
        or request.args["mots-cles"] is None
        or request.args["mots-cles"] == ""
    ):
        return render_template(
            "resultats_recherche_mots-cles.html",
            args="rien reçu !",
        )
    mots_cles = request.args["mots-cles"].split(" ")
    score_processus = {}
    for processus in retourne_tous_les_processus():
        score = 0
        for mot_cle in mots_cles:
            print(f"je cherche le mot clé {mot_cle}.")
            print(f"le titre = {processus['titre']}.")
            if processus["titre"] is not None and mot_cle in processus["titre"]:
                score += 50
            if processus["adapte"] is not None and mot_cle in processus["adapte"]:
                score += 10
            if processus["avantages"] is not None and mot_cle in processus["avantages"]:
                score += 10
            if processus["points_cles"] is not None  and mot_cle in processus["points_cles"]:
                score += 2
            if processus["description"] is not None  and mot_cle in processus["description"]:
                score += 1
        score_processus[processus] = score
        print(f"mon score final = {score}")
    return tri_et_retourne_resultats(score_processus)


def tri_et_retourne_resultats(score_processus):
    """Fonction qui trie les processus par score et renvoie la page de résultat de la recherche."""
    processus_triees = []
    for processus, score in sorted(
        score_processus.items(), key=lambda x: x[1], reverse=True
    ):
        processus_triees.append((processus, score))
    # détermination du gagnant
    meilleur_score = processus_triees[0][1]
    print("=====================")
    print(f"processus_triees = {processus_triees}")
    print("=====================")
    if meilleur_score <= 0:
        return render_template("resultats_recherche_vide.html")
    p_gagnant = processus_triees[0]
    # détermination des autres process
    p_pertinents = []
    # 1. les processus pertinents sont ceux qui ont au moins
    # un score supérieur ou égal à 80% du meilleur score
    p_autres = []
    # 2. les autres processus sont ceux qui ont un score positif
    # mais inférieur à 80% du meilleur score
    p_deconseille = []
    # 3. enfin, le reste est négatif ou égal à 0 et n'est pas recommandé
    for processus in processus_triees[1:]:
        if processus[1] <= 0:
            p_deconseille.append(processus)
        elif processus[1] < float(meilleur_score) * 0.8:
            p_autres.append(processus)
        else:
            p_pertinents.append(processus)

    return render_template(
        "resultats_recherche.html",
        p_gagnant=p_gagnant,
        p_pertinents=p_pertinents,
        p_autres=p_autres,
        p_deconseille=p_deconseille,
    )
