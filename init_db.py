#!/usr/bin/env python3

import sqlite3

connection = sqlite3.connect("database.db")

# Regénération du schéma de la base de données
with open("schema.sql", encoding="utf-8") as f:
    connection.executescript(f.read())

cur = connection.cursor()

corrections = """
Page 8 : dans ne => dans une
Page 10 : pareil
Page 34 : Tour de bonifications des objections => Bonification ou retrait de la proposition
Page 36 aussi.
Page 39 : fiche récap de processus => fiche récap de famille de processus
Page 44 : à source de sagesse => à une source de sagesse
Page 47 : probablement pas le bon contenu
"""

explications = """
Je crois que j'ai décidé de la chose suivante pour classer les familles de processus VS les processus :
id = x00 => c'est une famille de processus ;
id = xyy où yy > 0 => c'est un processus qui appartient à la famille x00.

ça permet d'écrire les requêtes suivantes pour trouver les familles :
``` sql
select id, titre from processus where id % 100 = 0
```

et ça pour trouver les processus :
``` sql
select id, titre from processus where id % 100 != 0
```
"""

processus = [
    {
        "id": 400,
        "titre": "Processus de décision horizontaux - égalitaires",
        "description": """<p>L’objectif est de prendre le temps de s’écouter et de construire une proposition commune afin de prendre des décisions qui conviennent à tous les membres de l’organisation.</p>
            <p><b>Liste de processus</b> : Consentement, consentement à proposition multiples, unanimité, consensus, consensus informel, consensus-n, …</p>""",
        "avantages": """<ul>
            <li>grande adhésion</li>
            <li>forte intelligence collective</li>
            <li>respect de chacun⋅e</li>
            <li>nourrit le lien</li>
            </ul>""",
        "adapte": """<ul>
            <li>décision demandant peu d'actions des autres</li>
            </ul>""",
        "risques": """<ul>
            <li>inertie, paralysie</li>
            <li>épuisement</li>
            <li>décision « molle »</li>
            <li>pression sur les individus pour être au niveau</li>
            </ul>""",
        "deconseille": """<ul>
            <li>les sujets urgents</li>
            <li>quand des avis irréconciliables coexistent</li>
            </ul>""",
        "points_cles": """<ul>
            <li>nécessite une posture coopérative des participants</li>
            <li>nécessite un objectif commun</li>
            </ul>""",
        "temps": "0123321",
        "enjeu": "0123332",
        "simplicite": "01233",
        "taille_groupe": "03332210",
        "adhesion": "01332",
        "creativite": "01310",
        # critères optionnels notés sur 12
        # -1 si le critère est vide
        "besoin_trancher": -1,
        "sujet_conflictuel": 10,
        "asynchrone": 8,
    },
    {
        "id": 402,
        "titre": "Consentement",
        "description": """<p><b>Processus</b>, en réunion :
            <ol>
                <li>Tour de clarification du sujet, partage des faits</li>
                <li>Écoute du centre pour faire émerger les besoins et l’intelligence collective</li>
                <li>Une personne / un sous-groupe fait une proposition</li>
                <li>Tour de clarification de la proposition</li>
                <li>Tour de ressenti sur la proposition</li>
                <li>Amendement : Le proposeur peut modifier sa proposition</li>
                <li>Tour d'objections</li>
                <li>Pour chaque objection :<ul>
                    <li>Test de l'objection</li>
                    <li>Bonification ou retrait de la proposition par le proposeur</li>
                </ul></li>
                <li>La proposition est validée lorsqu'il n'y a plus d'objections.</li>
            </ol></p>""",
        "avantages": """<ul>
            <li>bonne adhésion</li>
            <li>forte intelligence collective</li>
            <li>respect de chacun⋅e</li>
            <li>nourrit le lien</li>
            </ul>""",
        "adapte": """<ul>
            <li>sujet irréversible</li>
            </ul>""",
        "risques": """<ul>
            <li>inertie, paralysie</li>
            <li>épuisement</li>
            <li>décision « molle »</li>
            <li>pression sur les individus pour avoir la bonne posture</li>
            </ul>""",
        "deconseille": """<ul>
            <li>les sujets urgents</li>
            <li>quand des avis irréconciliables coexistent</li>
            </ul>""",
        "points_cles": """<ul>
            <li>nécessite formation et posture coopérative des participants</li>
            <li>nécessite un objectif commun, un excellent facilitateur</li>
            </ul>""",
        "temps": "0123321",
        "enjeu": "0123332",
        "simplicite": "01233",
        "taille_groupe": "03332210",
        "adhesion": "01332",
        "creativite": "01310",
        # critères optionnels notés sur 12
        # -1 si le critère est vide
        "besoin_trancher": -1,
        "sujet_conflictuel": 10,
        "asynchrone": 8,
    },
]

for process in processus:
    cur.execute(
        """INSERT INTO processus (
                    id,
                    titre,
                    description,
                    avantages,
                    adapte,
                    risques,
                    inconvenients,
                    deconseille,
                    points_cles,
                    temps,
                    enjeu,
                    simplicite,
                    taille_groupe,
                    adhesion,
                    creativite,
                    besoin_trancher,
                    sujet_conflictuel,
                    asynchrone
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            process.get("id"),
            process.get("titre"),
            process.get("description"),
            process.get("avantages"),
            process.get("adapte"),
            process.get("risques"),
            process.get("inconvenients"),
            process.get("deconseille"),
            process.get("points_cles"),
            process.get("temps"),
            process.get("enjeu"),
            process.get("simplicite"),
            process.get("taille_groupe"),
            process.get("adhesion"),
            process.get("creativite"),
            process.get("besoin_trancher"),
            process.get("sujet_conflictuel"),
            process.get("asynchrone")
        ),
    )

connection.commit()
connection.close()
