-- INSERT INTO opportunities_etudes (
--             Pays, Titre, Type, Description, Niveau, Financement, Conditions,
--             Domaine_Concerne, Durée_d_étude, Pays_éligibles, Date_Limite, Nombre_de_bourses
--         ) VALUES %s
--         ON CONFLICT (Pays, Titre) 
--         DO UPDATE SET
--             Type = EXCLUDED.Type,
--             Description = EXCLUDED.Description,
--             Niveau = EXCLUDED.Niveau,
--             Financement = EXCLUDED.Financement,
--             Conditions = EXCLUDED.Conditions,
--             Domaine_Concerne = EXCLUDED.Domaine_Concerne,
--             Durée_d_étude = EXCLUDED.Durée_d_étude,
--             Pays_éligibles = EXCLUDED.Pays_éligibles,
--             Date_Limite = EXCLUDED.Date_Limite,
--             Nombre_de_bourses = EXCLUDED.Nombre_de_bourses;

-- INSERT INTO opportunities_etudes (
--     pays, titre, type, description, niveau, financement, conditions,
--     domaine_concerne, duree_d_etude, pays_elegibles, date_limite, nombre_de_bourses
-- ) VALUES(%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)
-- ON CONFLICT (pays, titre)
-- DO UPDATE SET
--     type = EXCLUDED.type,
--     description = EXCLUDED.description,
--     niveau = EXCLUDED.niveau,
--     financement = EXCLUDED.financement,
--     date_limite = EXCLUDED.date_limite,
--     conditions = EXCLUDED.conditions,
--     nombre_de_bourses = EXCLUDED.nombre_de_bourses,
--     domaine_concerne = EXCLUDED.domaine_concerne,
--     duree_d_etude = EXCLUDED.duree_d_etude,
--     pays_elegibles = EXCLUDED.pays_elegibles;
    
    
INSERT INTO opportunities_etudes (
    pays, titre, type, description, niveau, financement, conditions,
    domaine_concerne, duree_d_etude, pays_eligibles, date_limite, nombre_de_bourses
) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (pays, titre)
DO UPDATE SET
    type = EXCLUDED.type,
    description = EXCLUDED.description,
    niveau = EXCLUDED.niveau,
    financement = EXCLUDED.financement,
    date_limite = EXCLUDED.date_limite,
    conditions = EXCLUDED.conditions,
    nombre_de_bourses = EXCLUDED.nombre_de_bourses,
    domaine_concerne = EXCLUDED.domaine_concerne,
    duree_d_etude = EXCLUDED.duree_d_etude,
    pays_eligibles = EXCLUDED.pays_eligibles;
