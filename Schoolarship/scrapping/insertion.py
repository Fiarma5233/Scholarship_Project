

import os
import pandas as pd
import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

def insert_data_to_postgres(csv_file, sql_create_table_file):
    """
    Cette fonction lit un fichier CSV, transforme les données, crée une table dans PostgreSQL si elle n'existe pas,
    puis insère les données dans la base de données.
    
    Les informations de connexion à la base de données sont extraites des variables d'environnement.
    """
    
    # Récupérer les informations de connexion depuis les variables d'environnement
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')

    # Charger les données depuis le fichier CSV dans un DataFrame Pandas
    df = pd.read_csv(csv_file)

    # Supprimer la colonne "Unnamed: 0" si elle existe
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])

    # Renommer les colonnes du DataFrame pour qu'elles correspondent aux champs de la table SQL
    df.rename(columns={
        'Pays': 'pays',
        'Titre': 'titre',
        'Type': 'type',
        'Description': 'description',
        'Niveau': 'niveau',
        'Financement': 'financement',
        'Date Limite': 'date_limite',
        'Conditions': 'conditions',
        'Nombre de bourses': 'nombre_de_bourses',
        'Domaine Conserné': 'domaine_concerne',
        'Durée d\'étude': 'duree_d_etude',
        'Pays éligibles': 'pays_eligibles'
    }, inplace=True)

    # Connexion à la base de données PostgreSQL avec les paramètres spécifiés
    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name
        )
        print("Connexion réussie à la base de données.")
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return

    # Créer un curseur pour exécuter des requêtes SQL
    cursor_postgres = conn.cursor()

    # Charger et lire la requête SQL pour créer la table depuis le fichier SQL
    try:
        with open(sql_create_table_file, 'r') as file:
            create_table_query = file.read()

        cursor_postgres.execute(create_table_query)
        conn.commit()  # Valider les modifications
        print("La table a été créée ou existe déjà.")
    except Exception as e:
        print(f"Erreur lors de la création de la table: {e}")
        conn.rollback()  # Annuler les modifications en cas d'erreur

    # Préparer la requête d'insertion SQL
    insert_query = sql.SQL("""
        INSERT INTO opportunities_etudes (
            pays, titre, type, description, niveau, financement, date_limite,
            conditions, nombre_de_bourses, domaine_concerne, duree_d_etude, pays_eligibles,send
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
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
    """)

    # Convertir le DataFrame en une liste de tuples pour l'insertion
    data = list(df.itertuples(index=False, name=None))

    # Insérer les données dans la table PostgreSQL
    try:
        cursor_postgres.executemany(insert_query, data)  # Utiliser executemany pour insérer plusieurs lignes
        conn.commit()  # Valider les modifications
        print("Les données ont été insérées avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'insertion des données: {e}")
        conn.rollback()  # Annuler les modifications en cas d'erreur

    # Utiliser SQLAlchemy pour lire les données si nécessaire
    engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    try:
        df_read = pd.read_sql("SELECT * FROM opportunities_etudes;", con=engine)
        print(df_read.head())
    except Exception as e:
        print(f"Erreur lors de la lecture des données : {e}")

    # Fermer le curseur et la connexion à la base de données
    cursor_postgres.close()
    conn.close()
    print("Connexion fermée.")


#insert_data_to_postgres('opportunities_etudes.csv', './databases/postgres_create_tables.sql')