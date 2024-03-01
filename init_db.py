#!/usr/bin/env python3

import json
import sqlite3

from os import path
from os import listdir


def main():
    """main function"""
    connection = sqlite3.connect("database.db")

    # Regénération du schéma de la base de données
    with open("schema.sql", encoding="utf-8") as f:
        connection.executescript(f.read())

    # import des données
    cur = connection.cursor()
    requete_import = "INSERT INTO processus (id, slug, titre, description, avantages, adapte, risques, inconvenients, deconseille, points_cles, temps, enjeu, simplicite, taille_groupe, adhesion, creativite, besoin_trancher, sujet_conflictuel, asynchrone ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    data_dir = path.join(path.dirname(path.realpath(__file__)), "data")
    for filename in listdir(data_dir):
        fullpath_filename = path.join(data_dir, filename)
        # on n'importe que les fichiers json
        if path.isfile(fullpath_filename) and filename[-5:] == ".json":
            with open(fullpath_filename, "rt", encoding="UTF-8") as process_file:
                try:
                    processus = json.load(process_file)
                except Exception as e:
                    print(f"Erreur dans le fichier {filename}")
                    raise e
                cur.execute(
                    requete_import,
                    (
                        processus.get("id"),
                        processus.get("slug"),
                        processus.get("titre"),
                        processus.get("description"),
                        processus.get("avantages"),
                        processus.get("adapte"),
                        processus.get("risques"),
                        processus.get("inconvenients"),
                        processus.get("deconseille"),
                        processus.get("points_cles"),
                        processus.get("temps"),
                        processus.get("enjeu"),
                        processus.get("simplicite"),
                        processus.get("taille_groupe"),
                        processus.get("adhesion"),
                        processus.get("creativite"),
                        processus.get("besoin_trancher"),
                        processus.get("sujet_conflictuel"),
                        processus.get("asynchrone"),
                    ),
                )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    main()
