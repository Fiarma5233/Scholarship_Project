

CREATE TABLE IF NOT EXISTS opportunities_etudes (
    id SERIAL PRIMARY KEY,
    pays VARCHAR(255) NOT NULL,
    titre TEXT NOT NULL,
    type VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    niveau VARCHAR(255) NOT NULL,
    financement TEXT NOT NULL,
    date_limite TEXT,
    conditions TEXT NOT NULL,
    nombre_de_bourses TEXT NOT NULL,
    domaine_concerne TEXT NOT NULL,
    duree_d_etude TEXT NOT NULL,
    pays_eligibles TEXT NOT NULL,
    send BOOLEAN DEFAULT FALSE, -- Nouvelle colonne booléenne ajoutée

    

    CONSTRAINT  unique_combination UNIQUE (pays, titre)
);