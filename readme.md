# Boîte à outils numérique de la Gouvernance Intégrative

Ceci est une pale tentative de numériser la boîte à outils de la [Gouvernance Intégrative](https://gouvernanceintegrative.com/) créée par Sacha Epp.

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

## Todolist

* [ ] Insérer la licence et la paternité sur toutes les pages (bas de page).
* [ ] Intégrer les autres processus.
* [ ] Faire une page de résultat de recherche plus parlante, avec des médailles et/ou un tableau.
* [x] faire une première fonction de recherche basique.
