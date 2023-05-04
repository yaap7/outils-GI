# source de l'exercice :
# https://www.digitalocean.com/community/tutorials/how-to-create-your-first-web-application-using-flask-and-python-3

import sqlite3
from flask import abort
from flask import Flask
from flask import render_template
from markupsafe import escape

app = Flask(__name__)


@app.template_filter()
def crit_filter(crit):
    result = {
        "0": "0",
        "1": "0.5",
        "2": "1",
    }
    return result[crit]


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/famille/<id_famille>")
def index(id_famille=1):
    """La page d'accueil
    return the default web page of a familly"""
    # toutes les caractéristiques qui peuvent être affichées dans une famille
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
    conn = get_db_connection()
    request = f"""SELECT *
    FROM familles
    WHERE id = {id_famille}
    LIMIT 1"""
    famille = conn.execute(request).fetchall()[0]
    conn.close()
    return render_template(
        "famille.html",
        famille=famille,
        caracteristiques=caracteristiques,
        criteres=criteres,
    )


# test d'apprentissage


@app.route("/")
@app.route("/index/")
def hello():
    return "<h1>Hello, World!</h1>"


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
