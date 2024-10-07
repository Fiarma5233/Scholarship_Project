# import logging
# import os
# import pandas as pd
# from sqlalchemy import create_engine
# from dotenv import load_dotenv

# # Charger les variables d'environnement
# load_dotenv()

# # Configuration du logging
# logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# def engine():
#     db_host = os.getenv('DB_HOST')
#     db_port = os.getenv('DB_PORT')
#     db_user = os.getenv('DB_USER')
#     db_password = os.getenv('DB_PASSWORD')
#     db_name = os.getenv('DB_NAME')
#     engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

#     return engine

# def get_new_opportunities():
#     # Récupérer les informations de connexion depuis les variables d'environnement
#     # db_host = os.getenv('DB_HOST')
#     # db_port = os.getenv('DB_PORT')
#     # db_user = os.getenv('DB_USER')
#     # db_password = os.getenv('DB_PASSWORD')
#     # db_name = os.getenv('DB_NAME')

    

#     # # Vérification des valeurs d'environnement
#     # if not all([db_host, db_port, db_user, db_password, db_name]):
#     #     logging.error("Certaines variables d'environnement pour la base de données sont manquantes.")
#     #     return pd.DataFrame()  # Retourner un DataFrame vide en cas d'erreur

#     # Connexion à la base de données PostgreSQL
#     try:
#         engine = engine()
#         logging.info("Connexion réussie à la base de données.")
#     except Exception as e:
#         logging.error(f"Erreur de connexion à la base de données : {e}")
#         return pd.DataFrame()  # Retourner un DataFrame vide en cas d'erreur

#     # Exécuter la requête pour récupérer les nouvelles opportunités
#     try:
#         query = 'SELECT * FROM opportunities_etudes WHERE send = FALSE;'
#         df_new_opportunities = pd.read_sql(query, con=engine)
#         logging.info(f"Récupération réussie de {len(df_new_opportunities)} nouvelles opportunités.")
#         print(df_new_opportunities.head())
#         return df_new_opportunities
#     except Exception as e:
#         logging.error(f"Erreur lors de la récupération des nouvelles opportunités : {e}")
#         return pd.DataFrame()  # Retourner un DataFrame vide en cas d'erreur

# # Appel de la fonction
# get_new_opportunities()



# def mark_opportunities_as_sent(opportunity_ids):
#     """Marque les opportunités comme envoyées dans la base de données."""
#     try:
#         engine = engine()
#         logging.info("Connexion réussie à la base de données.")
#     except Exception as e:
#         logging.error(f"Erreur de connexion à la base de données : {e}")
#         return False

#     try:
#         with engine.connect() as conn:
#             update_query = "UPDATE opportunities_etudes SET envoye = TRUE WHERE id = ANY(%s);"
#             conn.execute(update_query, (opportunity_ids,))
#             logging.info(f"Opportunités marquées comme envoyées pour les IDs : {opportunity_ids}")
#         return True
#     except Exception as e:
#         logging.error(f"Erreur lors de la mise à jour des opportunités envoyées : {e}")
#         return False



from users.send_email import get_new_opportunities, send_stages_email_to_users, get_users, mark_opportunities_as_sent, get_stages_and_users
stages, users = get_stages_and_users()

def essai():
    new_opportunities = get_new_opportunities()
    opportunity_ids = [opportunity[0] for opportunity in new_opportunities]  # Remplacez 0 par l'indice correct si nécessaire
    print("Mise à jour des données ")
    mark_opportunities_as_sent(opportunity_ids)
    print("Mise à jour des données terminée")

if __name__ == '__main__':
   
    #send_stages_email_to_users( get_new_opportunities(), get_users())
    #send_stages_email_to_users( stages, users)

    #get_new_opportunities()
    essai()

