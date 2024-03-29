DROP TABLE IF EXISTS processus;

CREATE TABLE processus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL,
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
    temps TEXT NOT NULL,
    enjeu TEXT NOT NULL,
    simplicite TEXT NOT NULL,
    taille_groupe TEXT NOT NULL,
    adhesion TEXT NOT NULL,
    creativite TEXT NOT NULL,
    besoin_trancher INTEGER NOT NULL,
    sujet_conflictuel INTEGER NOT NULL,
    asynchrone INTEGER NOT NULL
);
