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
        "titre": "Votes binaires",
        "description": """TODO""",
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
        "id": 201,
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
        "rapidite": "11111222110000",
        "enjeu": "00011112222222",
        "simplicite": "01111111111111",
        "taille_groupe": "22222111100000",
        "adhesion": "00001122222222",
    },
    {
        "id": 401,
        "titre": "Consensus",
        "description": """<p>Il existe de nombreuses variantes du consensus, en voilà une.</p>
            <p><b>Processus</b> :
            <ol>
                <li>Tour de clarification du sujet, partage des faits</li>
                <li>Tour de parole pour faire émerger les besoins et l’intelligence collective</li>
                <li>Une personne / un sous-groupe fait une proposition</li>
                <li>Tour de ressenti sur la proposition</li>
                <li>Le proposeur peut modifier sa proposition</li>
                <li>Tour de positionnement : soutenir, s’opposer ou s’abstenir</li>
                <li>La proposition est validée s’il n’y a pas d’opposition et moins de x% d’abstention.</li>
            </ol></p>""",
        "avantages": """<ul>
            <li>grande adhésion</li>
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
            <li>nécessite une posture coopérative des participants</li>
            <li>nécessite un objectif commun, un bon facilitateur</li>
            </ul>""",
        "rapidite": "01111222110000",
        "enjeu": "00000001112222",
        "simplicite": "01122110000000",
        "taille_groupe": "22211100000000",
        "adhesion": "00000001112222",
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
        "rapidite": "01111222110000",
        "enjeu": "00000001112222",
        "simplicite": "00000000122210",
        "taille_groupe": "22211100000000",
        "adhesion": "00000001112222",
    },
    {
        "id": 500,
        "titre": "Mode de décisions libertaires",
        "description": """<p>Chacun·e est libre de prendre sa propre décision ou des initiatives. Cela peut être sur un sujet précis ou être un mode de fonctionnement permanent de l’organisation (autogestion, do-ocratie, stigmergie, …).</p>
            <p>Il n’y a pas de processus, il peut ou pas y avoir des échanges.</p>
            <p>Même si ce n’est pas un fonctionnement légitimé dans l’organisation. La liberté et les initiatives individuelles existeront forcément de manière informelle.</p>""",
        "avantages": """<ul>
            <li>extrêmement économe en énergie, quasi instantané</li>
            <li>créativité individuelle</li>
            <li>connexion de l'individu à son enthousiasme</li>
            <li>possible sans être réunis</li>
            </ul>""",
        "adapte": """<ul>
            <li>décision urgente sans besoin de coordination</li>
            <li>sujet du ressort de l'individu</li>
            <li>enjeux faibles</li>
            </ul>""",
        "risques": """<ul>
            <li>individualisme et conflits</li>
            <li>confusion, chaos</li>
            <li>pas d'intelligence collective</li>
            <li>prise en compte des autres faible ou aléatoire</li>
            </ul>""",
        "rapidite": "00000000011222",
        "enjeu": "22221110000000",
        "simplicite": "22100000000000",
        "taille_groupe": "22222221111111",
        "adhesion": "22110000000000",
    },
    {
        "id": 501,
        "titre": "Règle de trois",
        "description": """<p><strong>Note importante</strong> : Ce processus a été rajouté par Guillaume G, et n'est pas contenu dans la boîte à outils originale de la Gouvernance Intégrative. Par conséquent, il est possible que les critères listés ici ne soit pas autant objectifs que pour les autres processus, et cette page devrait être soumis à relecture par Sacha. Elle est basé sur la règle de trois défini par la Fresque du Climat et décrite en détails ici : <a href="https://fresqueduclimat.org/projet/association/regle-de-trois/" target="_blank">https://fresqueduclimat.org/projet/association/regle-de-trois/</a>.</p>
        <p><b>Principe</b> : Le principe de base est que si 3 personnes sont convaincus qu'une initiative est bonne, ils peuvent prendre la décision de la mettre en œuvre (principe de la do-ocratie : ce sont ceux qui font qui décident)</p>
        <p><b>Processus</b> : Quand une personne a une proposition ou une idée, il en parle à 2 personnes <b>qu’il juge légitimes pour valider la proposition</b>.<br>
        Les 2 personnes en charge de se positionner peuvent répondre comme suit  :<br>
        <ul>
            <li><i>Joker</i> : Je passe mon tour car le sujet ne m’intéresse pas, je n’ai pas d’avis, je n’ai pas le temps, …</li>
            <li><b>Oui</b> : c'est une bonne idée, je valide → +1 point pour le décompte</li>
            <li><strong>Non</strong> : je ne valide pas → STOP : l'idée est alors rejeté immédiatement et n'ira pas plus loin avec la règle de trois. Il faudra trouver un autre processus pour la faire valider autrement.</li>
            <li>Peut-être → 0 point pour le décompte. Il faut alors trouver une autre personne qui puisse légitimement donner son avis sur la question. La personne qui dit « peut-être » peut recommander de consulter une personne en particulier. Dans ce cas, la recommandation doit être suivie.</li>
        </ul>
        Au bout de 3 “Oui”, l’idée est adoptée.<br>
        Au bout de 3 « peut-être » (et pas de non), soit on décide d’abandonner l’idée, soit on réunit les 3 personnes ayant dit « peut-être » pour comparer les arguments. Cela pourra aboutir soit sur une décision, soit sur une nouvelle proposition qui repart à zéro, soit vers le choix d'un autre processus de décision.</p>
        <p>⚠️ Ce processus doit être cadré (pour les décisions réversible, qui engage un montant maximum de XXX €, …) et la décision doit être communiqué de manière proportionnelle à son niveau d'engagement (qu'elle soit positive ou négative).</p>""",
        "avantages": """<ul>
            <li>responsabilise</li>
            <li>redonne de la liberté d'action</li>
            <li>créativité individuelle</li>
            <li>connexion de l'individu à son enthousiasme</li>
            </ul>""",
        "adapte": """<ul>
            <li>sujet du ressort de l'individu</li>
            <li>enjeux faibles</li>
            </ul>""",
        "risques": """<ul>
            <li>individualisme et conflits</li>
            <li>confusion, chaos</li>
            <li>moins d'intelligence collective</li>
            <li>prise en compte des autres modérée</li>
            </ul>""",
        "points_cles": """<ul>
            <li>son utilisation doit être encadrée pour ne pas donner trop de pouvoirs à un petit groupe</li>
            <ul>""",
        "rapidite": "00001122221100",
        "enjeu": "22221110000000",
        "simplicite": "11222100000000",
        "taille_groupe": "22222221111111",
        "adhesion": "22211100000000",
    },
    {
        "id": 600,
        "titre": "Décisions algorithmiques",
        "description": """<p><b>Processus</b> :</p>
            <ol>
                <li>Échanger sur le sujet</li>
                <li>Créer un « algorithme » pertinent (une formule)</li>
                <li>Chacun⋅e donne sa réponse</li>
                <li>Les réponses sont compilées grâce à l'algorithme, cela donne la décision</li>
            </ol>
            <p>Exemple : quel budget consacrons-nous à cet événement ?<br>
                => Faire la moyenne des réponses de chacun⋅e</p>""",
        "avantages": """<ul>
            <li>équitable, impartial</li>
            <li>possible à distance</li>
            <li>extrêmement rapide une fois l'algorithme validé</li>
            <li>facile de remodifier la décision</li>
            </ul>""",
        "adapte": """<ul>
            <li>limité à des critères mesurables et objectifs</li>
            </ul>""",
        "inconvenients": """<ul>
            <li>très rationnel et froid : pas de place pour l'émotionnel, la créativité, le lien, les cas particuliers</li>
            <li>peut être sensible aux manipulations</li>
            </ul>""",
        "points_cles": """<ul>
            <li>le pouvoir le plus important se situe dans le choix de l'algorithme</li>
            </ul>""",
        "rapidite": "00000011221100",
        "enjeu": "00111122222110",
        "simplicite": "11222111111111",
        "taille_groupe": "01222222222222",
        "adhesion": "00111222222111",
    },
    {
        "id": 700,
        "titre": "Hasard",
        "description": """<p><b>Processus</b> : La décision est prise suivant le résultat d’un test au résultat aléatoire, non sujet à interprétation.<br>
            Tirage à la courte paille, au dés, pile ou face, …</p>""",
        "avantages": """<ul>
            <li>impartialité totale</li>
            <li>possible à distance</li>
            <li>très économe en énergie</li>
            </ul>""",
        "adapte": """<ul>
            <li>quand les possibilités sont bien identifiées et équivalentes</li>
            <li>quand le mental est dépassé</li>
            <li>pour départager en cas d'égalité</li>
            <li>pour attribuer des rôles avec une excellente représentativité</li>
            </ul>""",
        "inconvenients": """<ul>
            <li>déresponsabilisation</li>
            <li>peu de réflexion</li>
            <li>créativité limitée</li>
            </ul>""",
        "points_cles": """<ul>
            <li>le véritable pouvoir est celui de déterminer les différentes options</li>
            </ul>""",
        "rapidite": "00000000011222",
        "enjeu": "22211000000000",
        "simplicite": "22110000000000",
        "taille_groupe": "22222222222222",
        "adhesion": "11111111111111",
    },
    {
        "id": 800,
        "titre": "Suivre un signe",
        "description": """<p>Décider en fonction de l’interprétation de signes (tirage de cartes, synchronicité, divination, astrologie, ressenti énergétique, pendule, …)<br>
            L’interprétation du signe peut être lié, à une personne dont la compétence est reconnue (chaman, astrologue, …) ou à une « règle » (Si le pendule tourne dans tel sens alors …).<br>
            Est souvent utilisé à titre individuel (ce qui n’est pas notre sujet).<br>
            A été très utilisé pendant des millénaires.</p>""",
        "avantages": """<ul>
            <li>souvent rapide</li>
            <li>économe en énergie (intuitif plutôt que mental)</li>
            <li>se sentir guidé ou connecté à une source de sagesse supérieure</li>
            </ul>""",
        "adapte": """<ul>
            <li>uniquement aux groupes avec croyances communes</li>
            <li>quand le mental est dépassé</li>
            </ul>""",
        "inconvenients": """<ul>
            <li>prise de pouvoir de la personne qui interprète</li>
            <li>déresponsabilisation</li>
            <li>pas ou peu d'intelligence collective</li>
            </ul>""",
        "points_cles": """<ul>
            <li></li>
            </ul>""",
        "rapidite": "11111112222222",
        "enjeu": "11111111111111",
        "simplicite": "00011111111111",
        "taille_groupe": "11111111111111",
        "adhesion": "00000000111111",
    },
    {
        "id": 900,
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
    {
        "id": 1000,
        "titre": "Non-choix",
        "description": """<p>Ne pas prendre de décision. Il peut y avoir une multitude de raisons :</p>
            <ul>
                <li>reporter la décision</li>
                <li>rejeter le thème (hors-sujet ou dépendant d’une autre instance)</li>
                <li>oubli</li>
                <li>accepter l’issue naturelle</li>
                <li>incapacité à se réunir</li>
                <li>incapacité à se mettre d’accord</li>
                <li>…</li>
            </ul>
            <p>Une distinction majeure est de savoir si cette absence de décision est subie (ce qui est douloureux) ou choisie…</p>""",
        "avantages": """<ul>
            <li>économie d'énergie</li>
            <li>prendre le temps</li>
            </ul>""",
        "risques": """<ul>
            <li>frustrations</li>
            <li>inertie</li>
            </ul>""",
        "points_cles": """<ul>
            <li></li>
            </ul>""",
        "rapidite": "11111111111111",
        "enjeu": "11111111111111",
        "simplicite": "11100000000000",
        "taille_groupe": "11111111111111",
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
                    risques,
                    inconvenients,
                    deconseille,
                    points_cles,
                    rapidite,
                    enjeu,
                    simplicite,
                    taille_groupe,
                    adhesion
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
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
            process.get("rapidite"),
            process.get("enjeu"),
            process.get("simplicite"),
            process.get("taille_groupe"),
            process.get("adhesion"),
        ),
    )

connection.commit()
connection.close()
