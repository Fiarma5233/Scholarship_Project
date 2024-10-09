

import os
import psycopg2
import ast
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def get_db_connection():
    """Crée et retourne une connexion à la base de données PostgreSQL."""
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )
    return conn

def convert_conditions_to_list(bourses):
    """Convertit le champ 'Conditions' en liste s'il contient des crochets, sinon laisse tel quel."""
    for index, bourse in enumerate(bourses):
        try:
            # Essaye de convertir le champ Conditions
            conditions = bourse[8]  # Remplace 8 par l'index correct si nécessaire
            if isinstance(conditions, str) and (conditions.startswith('[') and conditions.endswith(']')):
                # Si c'est une chaîne qui ressemble à une liste
                conditions_list = ast.literal_eval(conditions)
                # Conserve seulement les 2 premiers liens
                bourses[index] = (*bourse[:8], conditions_list[:2], *bourse[9:])  # Remplace l'index 8 par la liste
            else:
                # Sinon, laisse le champ tel quel
                bourses[index] = (*bourse[:8], conditions, *bourse[9:])
        except Exception as e:
            print(f"Erreur lors de la conversion des conditions: {e}")
    return bourses

def get_all_bourses(search_term=None):
    """Récupère toutes les bourses, stages et formations de la base de données, avec possibilité de recherche."""
    conn = get_db_connection()
    cur = conn.cursor()

    # Exécuter la requête pour récupérer toutes les bourses
    cur.execute('SELECT * FROM opportunities_etudes')
    toutes_les_bourses = cur.fetchall()
    toutes_les_bourses = convert_conditions_to_list(toutes_les_bourses)

    # Récupérer les bourses, stages et formations
    cur.execute("SELECT * FROM opportunities_etudes WHERE type = 'Bourse'")
    bourses = cur.fetchall()

    cur.execute("SELECT * FROM opportunities_etudes WHERE type = 'Stage'")
    stages = cur.fetchall()

    cur.execute("SELECT * FROM opportunities_etudes WHERE type = 'Formation'")
    formations = cur.fetchall()

    # Fermer le curseur et la connexion
    cur.close()
    conn.close()

    # Filtrer les résultats si un terme de recherche est fourni
    if search_term:
        toutes_les_bourses = [
            bourse for bourse in toutes_les_bourses 
            if search_term.lower() in (bourse[1].lower(), bourse[2].lower(), bourse[5].lower())
        ]
        bourses = [
            bourse for bourse in bourses 
            if search_term.lower() in (bourse[1].lower(), bourse[2].lower(), bourse[5].lower())
        ]

        
        stages = [
            stage for stage in stages 
            if search_term.lower() in (stage[1].lower(), stage[2].lower(), stage[5].lower())
        ]
        formations = [
            formation for formation in formations 
            if search_term.lower() in (formation[1].lower(), formation[2].lower(), formation[5].lower())
        ]

    # Retourner un dictionnaire contenant toutes les bourses
    return {
        'toutes_les_bourses': convert_conditions_to_list(toutes_les_bourses),
        'bourses': convert_conditions_to_list(bourses),
        'stages': convert_conditions_to_list(stages),
        'formations': convert_conditions_to_list(formations)
    }




import ast

def convert_conditions_to_liste(bourse):
    """Convertit le champ 'Conditions' de la bourse en liste s'il contient des crochets, sinon le laisse tel quel."""
    try:
        # Essaye de convertir le champ Conditions
        conditions = bourse[8]  # Remplace 8 par l'index correct si nécessaire
        if isinstance(conditions, str) and (conditions.startswith('[') and conditions.endswith(']')):
            # Si c'est une chaîne qui ressemble à une liste
            conditions_list = ast.literal_eval(conditions)
            # Conserve seulement les 2 premiers liens
            return (*bourse[:8], conditions_list[:2], *bourse[9:])  # Remplace l'index 8 par la liste
        else:
            # Sinon, laisse le champ tel quel
            return (*bourse[:8], conditions, *bourse[9:])
    except Exception as e:
        print(f"Erreur lors de la conversion des conditions: {e}")
        return bourse  # Retourne la bourse d'origine en cas d'erreur


# def get_db_connection():
#     """Crée et retourne une connexion à la base de données PostgreSQL."""
#     conn = psycopg2.connect(
#         host=os.getenv('DB_HOST'),
#         database=os.getenv('DB_NAME'),
#         user=os.getenv('DB_USER'),
#         password=os.getenv('DB_PASSWORD'),
#         port=os.getenv('DB_PORT')
#     )
#     return conn

def get_bourse_by_id(bourse_id):
    """Récupère une bourse de la base de données en fonction de son ID."""
    conn = get_db_connection()
    cur = conn.cursor()

    # Exécuter la requête pour récupérer la bourse par ID
    cur.execute("SELECT * FROM opportunities_etudes WHERE id = %s", (bourse_id,))
    bourse = cur.fetchone()
    bourse = convert_conditions_to_liste(bourse)

    # Fermer le curseur et la connexion
    cur.close()
    conn.close()

    return bourse
