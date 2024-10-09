# execute_scheduler.py
# from scrapping.scheduler import job

# def main():
#     job()


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


if __name__ == '__main__':
    job()