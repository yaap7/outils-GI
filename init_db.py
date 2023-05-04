import sqlite3

connection = sqlite3.connect("database.db")

# Regénération du schéma de la base de données
with open("schema.sql", encoding="utf-8") as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Ajout des familles "vote par approbation" et "tradition/habitude"

familles = [
    {
        "titre": "Vote par approbation",
        "description": """<b>Processus</b>, en réunion :
            <ol>
                <li>Tour de clarification du sujet, partage des faits</li>
                <li>Tour de parole pour faire émerger les besoins et l’intelligence collective</li>
                <li>Tour de propositions (4-5 max)</li>
                <li>Chacun-e vote pour toutes les propositions qu’il soutient</li>
                <li>La proposition avec la plus haute adhésion est retenue</li>
            </ol>""",
        "avantages": """<ul>
            <li>maitrise du temps</li>
            <li>forte intelligence collective</li>
            <li>équité</li>
            <li>met les participants dans une posture constructive</li>
            </ul>""",
        "adapte": """<ul>
            <li>décision demandant de la créativité</li>
            <li>trancher les sujets conflictuels</li>
            <li>les votants maîtrisent le sujet</li>
            </ul>""",
        "inconvenients": """<ul>
            <li>tour de proposition délicat à faciliter (risque de se perdre dans toutes les possibilités)</li>
            <li>énergivore</li>
            </ul>""",
        "points_cles": """<ul>
            <li>nécessite un facilitateur compétent</li>
            <li>les étapes peuvent être réparties sur plusieurs réunions</li>
            <li>le tour de proposition est déconseillé à plus que 8 personnes</li>
            </ul>""",
        "rapidite": "00011122100000",
        "enjeu": "00000000112222",
        "simplicite": "00000000112222",
        "taille_groupe": "01222222222222",
        "adhesion": "00000001222221",
    },
    {
        "titre": "Tradition, habitudes",
        "description": """<b>Processus</b>Cela peut être un choix conscient : « on fait comme d’habitude ». Mais la plupart du temps c’est une manière inconsciente de ne pas (re)prendre une décision.""",
        "avantages": """<ul>
            <li>extrêmement rapide, voir instantané</li>
            <li>gain d’énergie énorme</li>
            <li>contribue à un sens de l’identité</li>
            </ul>""",
        "adapte": """<ul>
            <li>aux décisions répétitives dont les conditions sont stables dans le temps</li>
            <li>quand le temps ou l’envie manque pour formaliser</li>
            <li>dans l’urgence quand rien n’est prévu</li>
            </ul>""",
        "inconvenients": """<ul>
            <li>immobilisme</li>
            <li>absence de créativité</li>
            <li>ne prend pas en compte les besoins individuels</li>
            </ul>""",
        "points_cles": """<ul>
            <li>Nécessite que le groupe partage une culture commune</li>
            </ul>""",
        "rapidite": "00000000000222",
        "enjeu": "22222222222111",
        "simplicite": "22110000000000",
        "taille_groupe": "22222222222222",
        "adhesion": "11111111111111",
    },
]

for famille in familles:
    cur.execute(
        """INSERT INTO familles (
                    titre,
                    description,
                    avantages,
                    adapte,
                    inconvenients,
                    points_cles,
                    rapidite,
                    enjeu,
                    simplicite,
                    taille_groupe,
                    adhesion
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            famille["titre"],
            famille["description"],
            famille["avantages"],
            famille["adapte"],
            famille["inconvenients"],
            famille["points_cles"],
            famille["rapidite"],
            famille["enjeu"],
            famille["simplicite"],
            famille["taille_groupe"],
            famille["adhesion"],
        ),
    )

connection.commit()
connection.close()
