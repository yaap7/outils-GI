# source de l'exercice :
# https://www.digitalocean.com/community/tutorials/how-to-create-your-first-web-application-using-flask-and-python-3

import sqlite3
from flask import abort
from flask import Flask
from flask import render_template
from flask import request
from os import path
from markupsafe import escape

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
# toutes les caractéristiques qui peuvent être affichées dans une famille
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
        "id": "inconvenients",
        "nom": "Inconvénients",
        "couleur": "lightcoral",
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


def retourne_une_famille(id_famille):
    """Retourne uniquement une famille.
    Prend l'ID de la famille en argument.
    Renvoie un dictionnaire"""
    conn = get_db_connection()
    req_select = """SELECT *
    FROM familles
    WHERE id = ?
    LIMIT 1"""
    result = conn.execute(req_select, [id_famille]).fetchall()
    conn.close()
    return result


def retourne_toutes_les_familles():
    """Retourne toute les familles de la base de données.
    Renvoie une liste de dictionnaire."""
    conn = get_db_connection()
    req_select = """SELECT *
    FROM familles"""
    result = conn.execute(req_select).fetchall()
    conn.close()
    return result


@app.route("/")
@app.route("/index/")
@app.route("/index.html")
def index():
    """Renvoie la page d'accueil"""
    familles = retourne_toutes_les_familles()
    return render_template(
        "index.html",
        familles=familles,
    )


@app.route("/famille/<id_famille>")
def get_famille(id_famille):
    """Affiche le détail d'une famille."""
    result = retourne_une_famille(id_famille)
    if len(result) > 0:
        famille = result[0]
        return render_template(
            "famille.html",
            famille=famille,
            caracteristiques=caracteristiques,
            criteres=criteres,
        )
    else:
        return "famille introuvable."


def get_famille_score(famille, criteres_voulus):
    """Retourne le score d'une famille par rapport aux critères voulus.
    La famille est l'objet retourné par fetchall() de la DB
    Les criteres_voulus sont de cette forme :
    criteres_voulus = {
        "rapidite": 4,
        "enjeu": 7,
    }
    La valeur pour les critères voulus doit être comprise entre 0 et 13 compris.

    Pour chaque critère, la famille gagne les points suivants :
    - 3 si c'est du vert foncé ;
    - 1 si c'est du vert clair ;
    - -1 si c'est du blanc.
    """

    def get_affinity(critere_famille, critere_voulu):
        if critere_famille[critere_voulu] == "0":
            return -1
        elif critere_famille[critere_voulu] == "1":
            return 1
        elif critere_famille[critere_voulu] == "2":
            return 3
        else:
            return -9000

    score = 0
    for critere_voulu in criteres_voulus:
        score += get_affinity(
            famille[critere_voulu], int(criteres_voulus[critere_voulu])
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
    print(criteres_voulus)
    score_familles = {}
    for famille in retourne_toutes_les_familles():
        score = get_famille_score(famille, criteres_voulus)
        print(f"le score de la famille {famille['titre']} = {score}")
        score_familles[famille] = score
    debug_var(score_familles)
    famille_triees = []
    for famille, score in sorted(
        score_familles.items(), key=lambda x: x[1], reverse=True
    ):
        famille_triees.append((famille, score))
    return render_template(
        "recherche.html",
        famille_triees=famille_triees,
    )


# test d'apprentissage


@app.route("/about/")
def about():
    return "<h3>This is a Flask web application.</h3>"


@app.route("/capitalize/<word>/")
def capitalize(word):
    return f"<h1>{escape(word.capitalize())}</h1>"


@app.route("/add/<int:n1>/<int:n2>/")
def add(n1, n2):
    return f"<h1>{n1 + n2}</h1>"


@app.route("/users/<int:user_id>/")
def greet_user(user_id):
    users = ["Bob", "Jane", "Adam"]
    try:
        return f"<h2>Hi {users[user_id]}</h2>"
    except IndexError:
        abort(404)
