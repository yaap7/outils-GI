DROP TABLE IF EXISTS processus;

CREATE TABLE processus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    description TEXT NOT NULL,
    -- textes :
    -- ce sont des textes contenant du HTML
    -- au format <ul><li>...</li></ul>
    -- car ce sont de simples listes
    avantages TEXT,
    adapte TEXT,
    risques TEXT,
    inconvenients TEXT,
    deconseille TEXT,
    points_cles TEXT,
    -- critères :
    -- ils sont au format de 14 caractères
    -- chaque caractère représente une case
    -- 0 = blanc
    -- 1 = vert pale
    -- 2 = vert foncé
    rapidite TEXT NOT NULL,
    enjeu TEXT NOT NULL,
    simplicite TEXT NOT NULL,
    taille_groupe TEXT NOT NULL,
    adhesion TEXT NOT NULL
);
