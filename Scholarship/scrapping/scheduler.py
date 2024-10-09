# import logging
# #from scrapping.study_opportunities import scrape_and_store_data
# from scrapping.insertion import insert_data_to_postgres
# from users.send_email import get_new_opportunities, send_stages_email_to_users, get_users, mark_opportunities_as_sent

# logging.basicConfig(filename='fiarma.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# def job():
#     try:
#         # logging.info("Scraping des données...")
#         # scrape_and_store_data()
#         # logging.info("Tâche de Scraping des terminée.")

#         print()

#         logging.info("Insertion des données dans PostgreSQL...")
#         insert_data_to_postgres('opportunities_etudes.csv', './databases/postgres_create_tables.sql')
#         logging.info("Tâche  d'insertion des données dans PostgreSQL terminée.")

#         print()

#         logging.info("Recuperation de nouvelles opportunites disponibles")
#         new_opportunities = get_new_opportunities()  # Récupérer les nouvelles opportunités
#         logging.info("Tâche de Recuperation de nouvelles opportunites disponibles terminée")

#         logging.info("Recuperation de tous les utilisateurs")
#         users = get_users()
#         logging.info("Tâche de Recuperation de tous les utilisateurs terminée")

#         print()

#         # Vérifier que new_opportunities n'est pas vide (si c'est une liste)
#         if new_opportunities and len(new_opportunities) > 0:
#             # Extraire la liste des IDs des nouvelles opportunités
#             logging.info("Extraire la liste des IDs des nouvelles opportunités")
#             opportunity_ids = [opportunity['id'] for opportunity in new_opportunities]  # Assurez-vous que chaque 'opportunity' est un dict avec 'id'
#             logging.info(" Tâche d'Extraction de la liste des IDs des nouvelles opportunités terminée")
       
#             # Envoyer les e-mails aux utilisateurs
#             logging.info("Envoyer les e-mails aux utilisateurs")
#             success = send_stages_email_to_users(opportunites=new_opportunities, users=users)  # Remplace par ta fonction d'envoi d'emails

#             if success:  # Si l'envoi des e-mails a réussi
#                 logging.info(" Tâche d'envoi des e-mails aux utilisateurs terminée")


#                 print()

#                 # Marquer les opportunités comme envoyées
#                 logging.info("Marquer les opportunités comme envoyées; mise a jours des donnees")
#                 mark_opportunities_as_sent(opportunity_ids)
#                 logging.info(" Tâche de mise a jours des donnees terminée")
#             else:
#                 logging.error("Échec de l'envoi des e-mails, les opportunités ne seront pas marquées comme envoyées.")
#         else:
#             logging.info("Aucune nouvelle opportunité à envoyer.")
#             # Optionnel : Envoi d'un email pour informer qu'il n'y a pas de nouvelles opportunités
#             # send_no_new_opportunities_email()  # Remplace par ta fonction d'envoi d'email

    
#     except Exception as e:
#         logging.error(f"Une erreur s'est produite : {str(e)}")


import logging
from scrapping.study_opportunities import scrape_and_store_data

from scrapping.insertion import insert_data_to_postgres
from users.send_email import get_new_opportunities, send_stages_email_to_users, get_users, mark_opportunities_as_sent

# Configuration du logging pour utiliser 'app.log' et afficher également dans la console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Remplacement par 'app.log'
        logging.StreamHandler()  # Ajoute la sortie console
    ]
)

def job():
    try:
        # Début de la tâche
        logging.info("Début de la tâche")

        print()

        logging.info("Scraping des données...")
        scrape_and_store_data()
        logging.info("Tâche de Scraping des terminée.")

        print()

        # Insertion des données dans PostgreSQL
        logging.info("Insertion des données dans PostgreSQL...")
        insert_data_to_postgres('opportunities_etudes.csv', './databases/postgres_create_tables.sql')
        logging.info("Tâche d'insertion des données dans PostgreSQL terminée.")

        # Récupération des nouvelles opportunités
        logging.info("Récupération de nouvelles opportunités disponibles")
        new_opportunities = get_new_opportunities()
        logging.info("Tâche de récupération des nouvelles opportunités terminée")

        # Récupération des utilisateurs
        logging.info("Récupération de tous les utilisateurs")
        users = get_users()
        logging.info("Tâche de récupération des utilisateurs terminée")

        # Vérification et envoi d'emails
        if new_opportunities and len(new_opportunities) > 0:
            logging.info("Nouvelles opportunités détectées")
            opportunity_ids = [opportunity[0] for opportunity in new_opportunities]  # Remplacez 0 par l'indice correct si nécessaire
            
            logging.info(f"Opportunités à marquer comme envoyées : {opportunity_ids}")

            success = send_stages_email_to_users(opportunites=new_opportunities, users=users)

            if success:
                logging.info("Envoi d'emails réussi")

                logging.info("Mise à jour des données ")
                mark_opportunities_as_sent(opportunity_ids)
                logging.info("Mise à jour des données terminée")
            else:
                logging.error("Échec de l'envoi des e-mails")
        else:
            logging.info("Aucune nouvelle opportunité à envoyer")

    except Exception as e:
        logging.error(f"Une erreur s'est produite : {str(e)}")

