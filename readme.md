# Boîte à outils numérique de la Gouvernance Intégrative

Ceci est une tentative de numériser la boîte à outils de la [Gouvernance Intégrative](https://gouvernanceintegrative.com/) créée par Sacha Epp.

Version : 2.1

## Todolist

* [ ] Rajouter le texte des processus d'après le PDf de la boite à outils.
* [ ] Voir avec Sacha s'il ne faudrait pas rajouter quelques processus dans chaque famille ou presque.
* [ ] Faire une nouvelle fonction de recherche en 2 ou 3 questions ("quelle est la taille du groupe ?", puis "quel est l'enjeu principal ? temps, adhésion, peu formé, etc" et peut-être question secondaire si applicable.)
* [ ] Réfléchir à rajouter des processus d'élection.
* [ ] faire une vérification des données insérées en base lors de l'import via `init_db.py`.
* [ ] Faire une plus belle page d'erreur lorsque le processus n'est pas trouvé (fonction `get_processus`).
* [ ] Prendre en compte l'ID ou le slug pour trouver un processus (fonction `get_processus`).
* [x] Intégrer les modifications de Sacha du 26/12/2023.
* [x] Convertir tous les processus pour tester les nouveaux critères de Sacha.
* [x] Refaire la fonction de recherche
* [x] Il est plus facile de rajouter des processus (via des fichiers JSON dans le répertoire `data`), même si ce n'est pas encore accessible à tout le monde.
* [x] Insérer la licence et la paternité sur toutes les pages (bas de page).
* [x] Intégrer les autres processus.
* [x] Faire une page de résultat de recherche plus parlante, avec des médailles et/ou un tableau.
* [x] faire une première fonction de recherche basique.

## Développement

Pour le moment, le backend est fait avec flask, et le frontend utilise [Bulma](https://bulma.io/) et aucun Javascript.

Pour formater le code selon les normes de black :

``` bash
make format
```

Pour lancer un serveur local de développement (qui relance l'application lorsqu'un fichier est modifié) :

``` bash
make dev_server
```

### Choix de développement

#### ID des processus

J'ai décidé de la chose suivante pour classer les familles de processus VS les processus :

* id = x00 → c'est une famille de processus ;
* id = xyy où yy > 0 → c'est un processus qui appartient à la famille x00.

ça permet d'écrire les requêtes suivantes pour trouver les familles :

``` sql
select id, titre from processus where id % 100 = 0
```

et ça pour trouver les processus :

``` sql
select id, titre from processus where id % 100 != 0
```
