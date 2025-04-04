import sqlite3
from os import path
from flask import Flask
from flask import render_template
from flask import request
from re import compile

PROJECT_ROOT = path.dirname(path.realpath(__file__))
DATABASE_PATH = path.join(PROJECT_ROOT, "database.db")

__VERSION__ = "2.3"
base_info = {
    "version": __VERSION__,
}

app = Flask(__name__)

conf = {
    # La liste des critères avec leur nom interne et leur nom d'affichage
    "criteres": [
        {
            "id": "temps",
            "nom": "Temps nécessaire",
            "echelle": [
                "Secondes",
                "Minutes",
                "",
                "Heures",
                "",
                "Jours",
                "Semaines",
            ],
        },
        {
            "id": "enjeu",
            "nom": "Niveau d'enjeu",
            "echelle": [
                "Faible",
                "",
                "",
                "",
                "",
                "",
                "Fort",
            ],
        },
        {
            "id": "simplicite",
            "nom": "Simplicité",
            "echelle": [
                "Groupe novice sans facilitateur expérimenté",
                "",
                "Groupe avec facilitateur expérimenté",
                "",
                "Participants et facilitateur expérimentés / formés",
            ],
        },
        {
            "id": "taille_groupe",
            "nom": "Pour taille de groupe",
            "echelle": [
                "1",
                "4",
                "8",
                "16",
                "Dizaines",
                "Centaines",
                "Milliers",
                "Millions",
            ],
        },
        {
            "id": "adhesion",
            "nom": "Niveau d'adhésion nécessaire",
            "echelle": [
                "Faible (être informé)",
                "",
                "Moyen (Accepter)",
                "",
                "Fort (Mettre en oeuvre spontanément = sans pression)",
            ],
        },
        {
            "id": "creativite",
            "nom": "Besoin de créativité",
            "echelle": [
                "Faible",
                "",
                "Modérée",
                "",
                "Forte",
            ],
        },
    ],
    # les critères optionnels
    "criteres_optionnels": [
        {
            "id": "besoin_trancher",
            "nom": "Besoin de trancher",
            "help": "",
        },
        {
            "id": "sujet_conflictuel",
            "nom": "Sujet conflictuel",
            "help": "",
        },
        {
            "id": "asynchrone",
            "nom": "Asynchrone",
            "help": "(faisable sans être réuni au même moment)",
        },
    ],
    # toutes les caractéristiques qui peuvent être affichées dans un processus
    "caracteristiques": [
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
    ],
}


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
        "1": "0.3",
        "2": "0.6",
        "3": "1",
    }
    return result[crit]


@app.template_filter()
def note_critere(note):
    """Renvoie l'affichage de la note du critère optionnel.
    Si le critère n'est pas renseigné, il est à `-1`, sinon, il est un nombre entre 0 et 12 inclus."""
    if (not isinstance(note, int)) or note > 12 or note < -1:
        return "Erreur : note incorrecte"
    if note == -1:
        return "Non spécifié"
    else:
        return f"{note} / 12"


@app.template_filter()
def pourcent_critere(note):
    """Renvoie la note ramenée sur 100.
    Si le critère n'est pas renseigné, il est à `-1`, sinon, il est un nombre entre 0 et 12 inclus.
    Par exemple, si le critère est à 7, le résultat sera `7 * 100 / 12 = 58`"""
    if (not isinstance(note, int)) or note > 12 or note < -1:
        return "Erreur : note incorrecte"
    if note == -1:
        return "Non spécifié"
    else:
        return int(note * 100 / 12)


@app.template_filter()
def p_type_el(processus):
    """Affiche "Le processus" ou "La famille de processus" en fonction du type de processus passé en paramètre."""
    if processus["id"] % 100 == 0:
        # c'est une famille
        return "La famille de processus"
    # c'est un processus
    return "Le processus"


def get_db_connection():
    """Renvoie une connexion à la base de données."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def retourne_un_processus(id_processus: int) -> dict:
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


def retourne_un_processus_via_slug(slug: str) -> dict:
    """Retourne uniquement un processus.
    Prend le slug du processus en argument.
    Renvoie un dictionnaire"""
    conn = get_db_connection()
    req_select = """SELECT *
    FROM processus
    WHERE slug = ?
    LIMIT 1"""
    result = conn.execute(req_select, [slug]).fetchall()
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
        base_info=base_info,
        conf=conf,
        processus_par_famille=processus_par_famille,
    )


@app.route("/processus/<slug>")
def get_processus(slug):
    """Affiche le détail d'un processus."""
    result = retourne_un_processus_via_slug(slug)
    if len(result) > 0:
        processus = result[0]
        return render_template(
            "processus.html",
            base_info=base_info,
            conf=conf,
            processus=processus,
        )
    return render_template(
        "resultats_recherche_vide.html",
        base_info=base_info,
        message="Ce processus est introuvable.",
        recherche_par_mot_cle=False,
    )


def get_processus_score_criteres(processus, criteres_voulus, criteres_optionnels_voulus) -> int:
    """Retourne le score d'un processus par rapport aux critères voulus.
    le processus est l'objet retourné par fetchall() de la DB
    Les criteres_voulus sont de cette forme :
    criteres_voulus = {
        "rapidite": 4,
        "enjeu": 7,
    }
    La valeur pour les critères voulus doit être comprise entre 0 et 13 compris.

    Pour chaque critère, le processus gagne les points suivants :
        - 15 si c'est = 3 (vert foncé) ;
        - 10 si c'est = 2 ;
        - 5 si c'est = 1 ;
        - -5 si c'est = 0 (blanc).
    + pour chaque carré adjacent (à 1 de distance) :
        - 6 si c'est = 3 (vert foncé) ;
        - 4 si c'est = 2 ;
        - 2 si c'est = 1 ;
        - -2 si c'est = 0 (blanc) ;
    + pour chaque carré à 2 de distance :
        - 3 si c'est = 3 (vert foncé) ;
        - 2 si c'est = 2 ;
        - 1 si c'est = 1 ;
        - -1 si c'est = 0 (blanc)

    Exemple : je veux une rapidité de 5 :

    00022310000000
        ^
    indice voulu

    alors score = 10 + 4 + 6 - 1 + 1 = 20


    pour les critères optionnels, le score gagné est de 6 - la distance entre la valeur souhaitée et la valeur du critère.
    Si le critère est à -1 (non spécifié), il n'est pas pris en compte dans le calcul.
    La distance maximale sera de 12 (environ), donc le score prendra une valeur comprise entre -6 et +6.
    Exemple, je veux un besoin de trancher à 10/12 (fort) mais le processus testé a un besoin de trancher à 3, le score sera de 6 - (10 - 3) = -1
    Si le processus d'après a un besoin de trancher à 9, alors le score sera de 6 - (10 - 9) = 5.
    """

    def get_affinity(critere_processus, indice_voulu, adjacent=0) -> int:
        scoring = {
            # sur le bon indice (0 de distance)
            0: {
                # couleur du carré = score
                3: 15,
                2: 10,
                1: 5,
                0: -5,
            },
            # à 1 de distance
            1: {
                3: 6,
                2: 4,
                1: 2,
                0: -2,
            },
            # à 2 de distance
            2: {
                3: 3,
                2: 2,
                1: 1,
                0: -1,
            },
        }
        return scoring[abs(adjacent)][int(critere_processus[indice_voulu + adjacent])]

    score = 0
    for critere_voulu in criteres_voulus:
        # obtention du score pour la valeur demandée
        indice_voulu = int(criteres_voulus[critere_voulu])
        print(f"je veux l'indice {indice_voulu}")
        print(f"processus[critere_voulu] = {processus[critere_voulu]}")
        score += get_affinity(processus[critere_voulu], indice_voulu)
        # évolution du score grâce aux valeurs adjacentes (à 1 de distance)
        if indice_voulu > 0:
            score += get_affinity(processus[critere_voulu], indice_voulu, -1)
        if indice_voulu < (len(processus[critere_voulu]) - 1):
            score += get_affinity(processus[critere_voulu], indice_voulu, 1)
        # évolution du score grâce aux valeurs adjacentes (à 2 de distance)
        if indice_voulu > 1:
            score += get_affinity(processus[critere_voulu], indice_voulu, -2)
        if indice_voulu < (len(processus[critere_voulu]) - 2):
            score += get_affinity(processus[critere_voulu], indice_voulu, 2)

    # calcul du score pour les critères optionnels
    for critere_optionnel_voulu, valeur_voulue in criteres_optionnels_voulus.items():
        # si le critère n'est pas défini, on passe (il est optionnel)
        valeur_du_processus = int(processus[critere_optionnel_voulu])
        if valeur_du_processus > 12 or valeur_du_processus < 0:
            continue
        score += 6 - abs(valeur_du_processus - int(valeur_voulue))
    return score


@app.route("/recherche_criteres")
def get_recherche_criteres():
    """Fonction de recherche par critères."""
    # récupération des critères souhaités
    id_criteres = [i["id"] for i in conf["criteres"]]
    criteres_voulus = {}
    for id_critere in id_criteres:
        if id_critere in request.args:
            criteres_voulus[id_critere] = request.args.get(id_critere)
    # récupération des critères optionnels souhaités
    id_criteres_optionnels = [i["id"] for i in conf["criteres_optionnels"]]
    criteres_optionnels_voulus = {}
    for id_critere in id_criteres_optionnels:
        if id_critere in request.args:
            criteres_optionnels_voulus[id_critere] = request.args.get(id_critere)
    # calcul des scores
    score_processus = {}
    try:
        for processus in retourne_tous_les_processus():
            score = get_processus_score_criteres(processus, criteres_voulus, criteres_optionnels_voulus)
            score_processus[processus] = score
    except IndexError:
        # pour palier à un attaquant qui mettrait un nombre en dehors du champ
        return render_template(
            "resultats_recherche_vide.html",
            base_info=base_info,
            message="Un nombre invalide a été reçu.",
            recherche_par_mot_cle=False,
        )
    return tri_et_retourne_resultats(criteres_voulus, score_processus, False)


def __get_score(mot_cle: str, phrase: str, score: int):
    if mot_cle is None or phrase is None:
        return 0
    r_tag = compile(r"<[^>]*>")
    r_espace = compile(r"[\s,;:.!?'()]+")
    # suppression des tags HTML
    _phrase = r_tag.sub(" ", phrase.lower())
    # dédoublonage des espaces et ponctuation
    _phrase = r_espace.sub(" ", _phrase)
    mots = _phrase.split(" ")
    if mot_cle.lower() in mots:
        return score
    return 0


@app.route("/recherche_mots-cles")
def get_recherche_mots_cles():
    """Fonction de recherche par mots clés."""
    if "mots-cles" not in request.args or request.args["mots-cles"] is None or request.args["mots-cles"] == "":
        return render_template(
            "resultats_recherche_vide.html",
            base_info=base_info,
            message="Aucun mot-clé reçu.",
            recherche_par_mot_cle=False,
        )
    mots_de_liaison = [
        "le",
        "la",
        "un",
        "les",
        "du",
        "de",
        "des",
        "à",
        "a",
        "mais",
        "ou",
        "et",
        "donc",
        "or",
        "ni",
        "car",
        "dont",
    ]
    mots_cles = request.args["mots-cles"].split(" ")
    score_processus = {}
    for processus in retourne_tous_les_processus():
        score = 0
        for mot_cle in mots_cles:
            if mot_cle.lower() in mots_de_liaison:
                continue
            score += __get_score(mot_cle, processus["titre"], 50)
            score += __get_score(mot_cle, processus["adapte"], 10)
            score += __get_score(mot_cle, processus["avantages"], 10)
            score += __get_score(mot_cle, processus["points_cles"], 2)
            score += __get_score(mot_cle, processus["description"], 1)
        score_processus[processus] = score
    return tri_et_retourne_resultats(mots_cles, score_processus, True)


def tri_et_retourne_resultats(criteres, score_processus, recherche_par_mot_cle: bool):
    """Fonction qui trie les processus par score et renvoie la page de résultat de la recherche."""
    processus_triees = []
    for processus, score in sorted(score_processus.items(), key=lambda x: x[1], reverse=True):
        processus_triees.append((processus, score))
    # détermination du gagnant
    meilleur_score = processus_triees[0][1]
    if meilleur_score <= 0:
        return render_template(
            "resultats_recherche_vide.html",
            base_info=base_info,
            message="Votre recherche n'a renvoyé aucun résultat.",
            recherche_par_mot_cle=recherche_par_mot_cle,
        )
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
        if processus[1] == 0:
            continue
        if processus[1] <= 0:
            p_deconseille.append(processus)
        elif processus[1] < float(meilleur_score) * 0.8:
            p_autres.append(processus)
        else:
            p_pertinents.append(processus)

    return render_template(
        "resultats_recherche.html",
        base_info=base_info,
        criteres=criteres,
        p_gagnant=p_gagnant,
        p_pertinents=p_pertinents,
        p_autres=p_autres,
        p_deconseille=p_deconseille,
    )
