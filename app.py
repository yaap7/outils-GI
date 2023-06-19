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


def get_processus_score(processus, criteres_voulus):
    """Retourne le score d'un processus par rapport aux critères voulus.
    le processus est l'objet retourné par fetchall() de la DB
    Les criteres_voulus sont de cette forme :
    criteres_voulus = {
        "rapidite": 4,
        "enjeu": 7,
    }
    La valeur pour les critères voulus doit être comprise entre 0 et 13 compris.

    Pour chaque critère, le processus gagne les points suivants :
    - 3 si c'est du vert foncé ;
    - 1 si c'est du vert clair ;
    - -1 si c'est du blanc.
    """

    def get_affinity(critere_processus, critere_voulu):
        if critere_processus[critere_voulu] == "0":
            return -1
        elif critere_processus[critere_voulu] == "1":
            return 1
        elif critere_processus[critere_voulu] == "2":
            return 3
        else:
            return -9000

    score = 0
    for critere_voulu in criteres_voulus:
        score += get_affinity(
            processus[critere_voulu], int(criteres_voulus[critere_voulu])
        )
    return score


@app.route("/recherche")
def get_recherche():
    """Fonction de recherche. à améliorer."""
    id_criteres = [i["id"] for i in criteres]
    criteres_voulus = {}
    for id_critere in id_criteres:
        if id_critere in request.args:
            criteres_voulus[id_critere] = request.args.get(id_critere)
    score_processus = {}
    for processus in retourne_tous_les_processus():
        score = get_processus_score(processus, criteres_voulus)
        score_processus[processus] = score
    processus_triees = []
    for processus, score in sorted(
        score_processus.items(), key=lambda x: x[1], reverse=True
    ):
        processus_triees.append((processus, score))
    return render_template(
        "recherche.html",
        processus_triees=processus_triees,
    )
