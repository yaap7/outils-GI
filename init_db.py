import sqlite3

connection = sqlite3.connect("database.db")

# Regénération du schéma de la base de données
with open("schema.sql", encoding="utf-8") as f:
    connection.executescript(f.read())

cur = connection.cursor()

corrections = """
Page 8 : dans ne => dans une
Page 10 : pareil
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
        "id": 100,
        "titre": "Votes à choix multiples",
        "description": """Les votes à choix multiples sont une famille de processus de décision dont le point commun est, sur un sujet donnée, de :
        <ul>
        <li>faire émerger plusieurs propositions, les personnes impliquée se positionnent sur chaque proposition, celle avec la plus haute adhésion est validée</li>
        <li>ou de faire évoluer une proposition par une série de votes (amendements) jusqu’à sa validation.</li>
        </ul>""",
        "avantages": """<ul>
            <li>maîtrise du temps</li>
            <li>forte intelligence collective</li>
            <li>équité</li>
            <li>met les participants dans une posture constructive</li>
            <li>simple pour les participants</li>
            </ul>""",
        "adapte": """<ul>
            <li>décision demandant de la créativité</li>
            <li>trancher les sujets conflictuels</li>
            <li>les votants maîtrisent le sujet</li>
            </ul>""",
        "inconvenients": """<ul>
            <li>énergivore (se perdre dans toutes les possibilités)</li>
            <li>parfois délicat à faciliter</li>
            </ul>""",
        "points_cles": """""",
        "rapidite": "00011111111000",
        "enjeu": "00011122222211",
        "simplicite": "00011111111111",
        "taille_groupe": "01222222222222",
        "adhesion": "00001111222221",
    },
    {
        "id": 101,
        "titre": "Vote pondéré",
        "description": """<b>Processus</b>, en réunion :<br>
        <ol>
        <li>Tour de clarification du sujet, partage des faits</li>
        <li>Tour de parole pour faire émerger les besoins et l’intelligence collective</li>
        <li>Tour de propositions (4-5 max)</li>
        <li>Chacun-e note toutes les propositions</li>
        <li>La proposition avec la plus haute note est retenue</li>
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
            <li>étape 3 délicate à faciliter (risque de se perdre dans toutes les possibilités)</li>
            <li>énergivore</li>
            </ul>""",
        "points_cles": """<ul>
            <li>nécessite un facilitateur compétent</li>
            <li>les étapes peuvent être réparties sur plusieurs réunions</li>
            <li>l’étape 3 peut être préférable en sous-groupe</li>
            </ul>""",
        "rapidite": "00011122100000",
        "enjeu": "00000000112222",
        "simplicite": "00000000112222",
        "taille_groupe": "01222222222222",
        "adhesion": "00000001222221",
    },
    {
        "id": 102,
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
        "id": 200,
        "titre": "Vote à la majorité",
        "description": """<b>Processus</b>, en réunion :
            <ol>
                <li>Une proposition est mise à l’ordre du jour.</li>
                <li>Clarification de la proposition, partage des faits.</li>
                <li>Chacun·e vote «pour » ou « contre» la proposition.</li>
                <li>La proposition est validée au dessus de 50% de «pour »</li>
            </ol>""",
        "avantages": """<ul>
            <li>plutôt rapide</li>
            <li>équité dans le vote</li>
            <li>possible à distance</li>
            </ul>""",
        "adapte": """<ul>
            <li>sujet binaire</li>
            </ul>""",
        "inconvenients": """<ul>
            <li>clivant</li>
            <li>faible intelligence collective</li>
            <li>pas de prise en compte de la minorité</li>
            <li>non application de la décision par la minorité</li>
            </ul>""",
        "points_cles": """<ul>
            <li>La personne qui formule la proposition a un pouvoir énorme, risque de manipulation.</li>
            </ul>""",
        "rapidite": "00000001210000",
        "enjeu": "00011122221100",
        "simplicite": "22100000000000",
        "taille_groupe": "01222222222222",
        "adhesion": "00011222211000",
    },
    {
        "id": 300,
        "titre": "Processus consultatifs",
        "description": """Une personne (le décideur) décide seul d’un sujet après avoir demandé leurs opinions aux personnes concernées ou compétentes.<br>
Le processus de consultation peut être informel, souvent oral ou formalisé et mis par écrit (sur un tableau ou sur informatique).<br>
<b>Liste de processus</b> : Sollicitation d’avis, partage d’intention, consultation présentielle,...""",
        "avantages": """<ul>
            <li>assez économe en énergie</li>
            <li>grande créativité</li>
            <li>possible sans être réunis !</li>
            </ul>""",
        "adapte": """<ul>
            <li>décision demandant peu d’actions des autres</li>
            </ul>""",
        "inconvenients": """<ul>
            <li>individualisme et conflis</li>
            <li>écarts de pouvoir</li>
            </ul>""",
        "points_cles": """<ul>
            <li>Requiert un décideur avec une bonne capacité d’écoute et de synthèse et qui ose décider</li>
            <li>Demande un bon niveau de confiance dans le groupe et vis à vis du décideur</li>
            <li>Savoir identifier si une décision nécessite de consulter et qui consulter</li>
            </ul>""",
        "rapidite": "00111111111000",
        "enjeu": "00111111111100",
        "simplicite": "01111111000000",
        "taille_groupe": "11111111111100",
        "adhesion": "00111111111000",
    },
    {
        "id": 301,
        "titre": "Sollicitation d’avis",
        "description": """Une personne (le décideur) est souveraine pour décider d’un sujet, mais elle a l’obligation de consulter toutes les personnes concernées ou compétentes. Une fois les consultations finies, elle décide seule et annonce sa décision au groupe.<br>
        La personne peut se saisir d’un sujet de sa propre initiative ou celui-ci peut lui être confié par le groupe.""",
        "avantages": """<ul>
            <li>assez économe en énergie</li>
            <li>grande créativité</li>
            <li>possible sans être réunis !</li>
            </ul>""",
        "adapte": """<ul>
            <li>décision demandant peu d’actions des autres</li>
            </ul>""",
        "inconvenients": """<ul>
            <li>individualisme et conflis</li>
            <li>écarts de pouvoir</li>
            </ul>""",
        "points_cles": """<ul>
            <li>Requiert d’assumer de décider</li>
            <li>Demande un bon niveau de confiance dans le groupe et vis à vis du décideur</li>
            <li>Dépendant de la capacité d’écoute et de synthèse du décideur</li>
            </ul>""",
        "rapidite": "00112221000000",
        "enjeu": "00122222222100",
        "simplicite": "01222211000000",
        "taille_groupe": "22222222110000",
        "adhesion": "00111222111000",
    },
    {
        "id": 302,
        "titre": "Partage d’intention",
        "description": """La personne qui veut prendre une décision l’annonce en réunion, sur un tableau ou sur informatique.<br>
        Le principe est « qui ne dit mot consent », en l’absence de retour, elle met en œuvre sa décision. De préférence, si la décision n’est pas réversible, elle attend avant de la mettre en œuvre.""",
        "avantages": """<ul>
            <li>très économe en énergie</li>
            <li>possible sans être réunis</li>
            </ul>""",
        "adapte": """<ul>
            <li>décisions réversibles</li>
            </ul>""",
        "inconvenients": """<ul>
            <li>conflits, particulièrement avec les absents</li>
            <li>manque d’intelligence collective</li>
            </ul>""",
        "points_cles": """<ul>
            <li>requiert un temps ou un espace pour partager son intention</li>
            <li>bien formuler « J’ai l’intention de ... » plutôt que « J’ai décidé de... »</li>
            <li>demande de l’ouverture de la part du décideur et du courage de la part des timides.</li>
            </ul>""",
        "rapidite": "00112221000000",
        "enjeu": "01222100000000",
        "simplicite": "22100000000000",
        "taille_groupe": "22222211100000",
        "adhesion": "12211000000000",
    },
    {
        "id": 303,
        "titre": "Consultation présentielle",
        "description": """<b>Processus</b> : Une personne, le décideur, a la responsabilité d’une décision. Lors d’une réunion a lieu :<br>
        <ol>
        <li>Echange d’informations, clarification du sujet ou de la proposition</li>
        <li>Tour de parole</li>
        <li>Le décideur prend seul la décision (plutôt après la réunion) puis annonce sa décision</li>
        </ol>""",
        "avantages": """<ul>
            <li>bonne créativité</li>
            <li>forte intelligence collective</li>
            <li>tour de parole détendu, sans l’enjeu de converger</li>
            <li>nourrit la cohésion</li>
            </ul>""",
        "adapte": """""",
        "inconvenients": """<ul>
            <li>écarts de pouvoir (souvent les mêmes décideurs)</li>
            <li>nécessite d’être réunis</li>
            </ul>""",
        "points_cles": """<ul>
            <li>requiert d’assumer de décider</li>
            <li>demande un bon niveau de confiance dans le groupe et vis à vis du décideur</li>
            <li>dépendant de la capacité d’écoute et de synthèse du décideur</li>
            </ul>""",
        "rapidite": "00000012210000",
        "enjeu": "00001112222222",
        "simplicite": "01221000000000",
        "taille_groupe": "22222110000000",
        "adhesion": "00000011222211",
    },
    # TODO : to be continued at "Processus de décision horizontaux - égalitaires"
    {
        "id": 888,
        "titre": "",
        "description": """""",
        "avantages": """<ul>
            <li></li>
            </ul>""",
        "adapte": """<ul>
            <li></li>
            </ul>""",
        "inconvenients": """<ul>
            <li></li>
            </ul>""",
        "points_cles": """<ul>
            <li></li>
            </ul>""",
        "rapidite": "00112221000000",
        "enjeu": "01222100000000",
        "simplicite": "22100000000000",
        "taille_groupe": "22222211100000",
        "adhesion": "12211000000000",
    },
    {
        "id": 999,  # TODO change this ID
        "titre": "Tradition, habitudes",
        "description": """<b>Processus</b><br>
            Cela peut être un choix conscient : « on fait comme d’habitude ». Mais la plupart du temps c’est une manière inconsciente de ne pas (re)prendre une décision.""",
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

for process in processus:
    cur.execute(
        """INSERT INTO processus (
                    id,
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
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            process["id"],
            process["titre"],
            process["description"],
            process["avantages"],
            process["adapte"],
            process["inconvenients"],
            process["points_cles"],
            process["rapidite"],
            process["enjeu"],
            process["simplicite"],
            process["taille_groupe"],
            process["adhesion"],
        ),
    )

connection.commit()
connection.close()
