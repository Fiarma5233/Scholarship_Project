from flask import Flask, request, redirect, url_for, flash
import os
import psycopg2
import smtplib
import requests
import logging
import pandas as pd
from sqlalchemy import create_engine
from email.mime.text import MIMEText
from dotenv import load_dotenv
from databases.db import get_db_connection, convert_conditions_to_list
# Charger les variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Configuration pour l'envoi d'e-mails
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = os.getenv("SMTP_USERNAME")  # Ton adresse Gmail
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # Ton mot de passe ou App Password

def get_opportunities_and_users():
    # Connexion à la base de données PostgreSQL
    conn = get_db_connection()
    
    cur = conn.cursor()
    
    # Récupérer tous les stages
    cur.execute("SELECT * FROM opportunities_etudes")
    opportunities = cur.fetchall()
    
    # Récupérer les emails et noms des utilisateurs
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return opportunities, users


from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader




# def send_stages_email_to_users():
#     # Récupérer les stages et les utilisateurs
#     stages, users = get_stages_and_users()
    
#     # Configuration de l'environnement Jinja2 pour charger les templates
#     env = Environment(loader=FileSystemLoader('templates'))
#     env.globals['url_for'] = url_for  # Ajoute url_for aux globals de Jinja2

#     template = env.get_template('email.html')  # Template HTML créé auparavant
    
#     # Connexion au serveur SMTP
#     try:
#         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
#         server.starttls()
#         server.login(SMTP_USERNAME, SMTP_PASSWORD)
#     except smtplib.SMTPException as e:
#         print(f"Erreur lors de la connexion au serveur SMTP : {e}")
#         return
    
#     for user in users:
#         email = user[1]  # Assumant que l'email est dans la deuxième colonne (index 1)
#         name = user[2]   # Assumant que le nom est dans la troisième colonne (index 2)
        
#         # Préparation du sujet et du contenu de l'email
#         subject = "Dernières opportunités de stage disponibles"
        
#         # Rendu du template avec les données utilisateur et stages
#         html_content = template.render(nom=name, stages=stages)
        
#         # Création du message
#         msg = MIMEMultipart("alternative")
#         msg["Subject"] = subject
#         msg["From"] = SMTP_USERNAME
#         msg["To"] = email
        
#         # Attacher le contenu HTML à l'email
#         msg.attach(MIMEText(html_content, 'html'))
        
#         # Envoi de l'email
#         try:
#             server.sendmail(SMTP_USERNAME, email, msg.as_string())
#             print(f"E-mail envoyé avec succès à {email}")
#         except smtplib.SMTPException as e:
#             print(f"Erreur lors de l'envoi de l'e-mail à {email}: {e}")
    
#     # Fermer la connexion SMTP
#     server.quit()


# if __name__ == '__main__':
#     get_stages_and_users()
#     send_stages_email_to_users()

##########################################

def get_users():
    # Connexion à la base de données PostgreSQL
    conn = get_db_connection()
    
    cur = conn.cursor()
    
    
    # Récupérer les emails et noms des utilisateurs
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return  users


# def send_stages_email_to_users(opportunites, users):
#     """
#     Envoie des emails aux utilisateurs avec les informations des stages.
    
#     :param stages: Liste des stages à inclure dans l'email
#     :param users: Liste des utilisateurs (chaque utilisateur étant une liste contenant l'email et le nom)
#     """
#     # Configuration de l'environnement Jinja2 pour charger les templates
#     env = Environment(loader=FileSystemLoader('templates'))
#     env.globals['url_for'] = url_for  # Ajoute url_for aux globals de Jinja2

#     template = env.get_template('email.html')  # Template HTML créé auparavant
    
#     # Connexion au serveur SMTP
#     try:
#         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
#         server.starttls()
#         server.login(SMTP_USERNAME, SMTP_PASSWORD)
#     except smtplib.SMTPException as e:
#         print(f"Erreur lors de la connexion au serveur SMTP : {e}")
#         return
    
#     for user in users:
#         email = user[1]  # Assumant que l'email est dans la deuxième colonne (index 1)
#         name = user[2]   # Assumant que le nom est dans la troisième colonne (index 2)
        
#         # Préparation du sujet et du contenu de l'email
#         subject = "Dernières opportunités de stage disponibles"
        
#         # Rendu du template avec les données utilisateur et stages
#         html_content = template.render(nom=name, opportunites=opportunites)
        
#         # Création du message
#         msg = MIMEMultipart("alternative")
#         msg["Subject"] = subject
#         msg["From"] = SMTP_USERNAME
#         msg["To"] = email
        
#         # Attacher le contenu HTML à l'email
#         msg.attach(MIMEText(html_content, 'html'))
        
#         # Envoi de l'email
#         try:
#             server.sendmail(SMTP_USERNAME, email, msg.as_string())
#             print(f"E-mail envoyé avec succès à {email}")
#         except smtplib.SMTPException as e:
#             print(f"Erreur lors de l'envoi de l'e-mail à {email}: {e}")
    
#     # Fermer la connexion SMTP
#     server.quit()


def send_stages_email_to_users(opportunites, users):
    """
    Envoie des emails aux utilisateurs avec les informations des stages.
    
    :param opportunites: Liste des opportunités à inclure dans l'email
    :param users: Liste des utilisateurs (chaque utilisateur étant une liste contenant l'email et le nom)
    :return: True si tous les e-mails ont été envoyés avec succès, sinon False
    """
    env = Environment(loader=FileSystemLoader('templates'))
    env.globals['url_for'] = url_for

    template = env.get_template('email.html')
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
    except smtplib.SMTPException as e:
        print(f"Erreur lors de la connexion au serveur SMTP : {e}")
        return False  # Retourne False en cas d'échec de connexion

    all_success = True  # Indicateur pour suivre le succès des envois

    for user in users:
        email = user[1]
        name = user[2]
        
        subject = "Dernières opportunités de stage disponibles"
        html_content = template.render(nom=name, opportunites=opportunites)
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SMTP_USERNAME
        msg["To"] = email
        msg.attach(MIMEText(html_content, 'html'))
        
        try:
            server.sendmail(SMTP_USERNAME, email, msg.as_string())
            print(f"E-mail envoyé avec succès à {email}")
        except smtplib.SMTPException as e:
            print(f"Erreur lors de l'envoi de l'e-mail à {email}: {e}")
            all_success = False  # Si un e-mail échoue, mettre à jour l'indicateur

    server.quit()
    return all_success  # Retourne True si tous les e-mails ont été envoyés avec succès


# def engine():
#     db_host = os.getenv('DB_HOST')
#     db_port = os.getenv('DB_PORT')
#     db_user = os.getenv('DB_USER')
#     db_password = os.getenv('DB_PASSWORD')
#     db_name = os.getenv('DB_NAME')
#     engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

#     return engine

# def get_new_opportunities():
    
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
#             update_query = "UPDATE opportunities_etudes SET send = TRUE WHERE id = ANY(%s);"
#             conn.execute(update_query, (opportunity_ids,))
#             logging.info(f"Opportunités marquées comme envoyées pour les IDs : {opportunity_ids}")
#         return True
#     except Exception as e:
#         logging.error(f"Erreur lors de la mise à jour des opportunités envoyées : {e}")
#         return False


def create_engine_connection():
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
    engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    return engine

# def get_new_opportunities():
#     # Connexion à la base de données PostgreSQL
#     try:
#         #engine = create_engine_connection()
#         conn = get_db_connection()
#         logging.info("Connexion réussie à la base de données.")
#     except Exception as e:
#         logging.error(f"Erreur de connexion à la base de données : {e}")
#         return pd.DataFrame()  # Retourner un DataFrame vide en cas d'erreur

#     # Exécuter la requête pour récupérer les nouvelles opportunités
#     try:
#         # query = 'SELECT * FROM opportunities_etudes WHERE send = FALSE;'
#         # df_new_opportunities = pd.read_sql(query, con=engine)
#         # logging.info(f"Récupération réussie de {len(df_new_opportunities)} nouvelles opportunités.")
#         # print(df_new_opportunities.head())
#         # print(f"le 4e element est: {df_new_opportunities[3]}")
#         # print("Colonnes du DataFrame :", df_new_opportunities.columns.tolist())
#         # Connexion à la base de données PostgreSQL
#         #conn = get_db_connection()
    
#         cur = conn.cursor()
        
#         # Récupérer tous les stages
#         cur.execute('SELECT * FROM opportunities_etudes WHERE send = FALSE;')
#         df_new_opportunities = cur.fetchall()
        
#         # Récupérer les emails et noms des utilisateurs
#         # cur.execute("SELECT * FROM users")
#         # users = cur.fetchall()
        
#         cur.close()
#         conn.close()

#         #print(df_new_opportunities[3])
#         print(f"le 4e element est: {df_new_opportunities[3]}")
#         return df_new_opportunities
    
#     except Exception as e:
#         logging.error(f"Erreur lors de la récupération des nouvelles opportunités : {e}")
#         return pd.DataFrame()  # Retourner un DataFrame vide en cas d'erreur


def get_new_opportunities():
    # Connexion à la base de données PostgreSQL
    try:
        conn = get_db_connection()
        logging.info("Connexion réussie à la base de données.")
    except Exception as e:
        logging.error(f"Erreur de connexion à la base de données : {e}")
        return pd.DataFrame()  # Retourner un DataFrame vide en cas d'erreur

    # Exécuter la requête pour récupérer les nouvelles opportunités
    try:
        cur = conn.cursor()
        
        # Récupérer tous les stages
        logging.info("Exécution de la requête pour récupérer les nouvelles opportunités...")
        cur.execute('SELECT * FROM opportunities_etudes WHERE send = FALSE;')
        
        # Récupérer les résultats
        df_new_opportunities = cur.fetchall()
        
        # Vérifier si des opportunités ont été trouvées
        if df_new_opportunities:
            logging.info(f"Récupération réussie de {len(df_new_opportunities)} nouvelles opportunités.")
            #print(f"le 4e élément est: {df_new_opportunities[3]}")
        else:
            logging.warning("Aucune nouvelle opportunité trouvée.")

        cur.close()
        conn.close()

        return df_new_opportunities
    
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des nouvelles opportunités : {e}")
        return pd.DataFrame()  # Retourner un DataFrame vide en cas d'erreur
    
    
# Appel de la fonction
#get_new_opportunities()

# def mark_opportunities_as_sent(opportunity_ids):
#     """Marque les opportunités comme envoyées dans la base de données."""
#     try:
#         engine = create_engine_connection()
#         logging.info("Connexion réussie à la base de données.")
#     except Exception as e:
#         logging.error(f"Erreur de connexion à la base de données : {e}")
#         return False

#     try:
#         with engine.connect() as conn:
#             update_query = "UPDATE opportunities_etudes SET send = TRUE WHERE id = ANY(%s);"
#             conn.execute(update_query, (opportunity_ids,))
#             logging.info(f"Opportunités marquées comme envoyées pour les IDs : {opportunity_ids}")
#         return True
#     except Exception as e:
#         logging.error(f"Erreur lors de la mise à jour des opportunités envoyées : {e}")
#         return False


# def mark_opportunities_as_sent(opportunity_ids):
#     try:
#         conn = get_db_connection()
#         logging.info("Connexion réussie à la base de données.")
#     except Exception as e:
#         logging.error(f"Erreur de connexion à la base de données : {e}")

#     try:
#         connexion = conn.cursor()
#         # Connexion à la base de données
#         logging.info("Connexion à la base de données pour mise à jour des opportunités.")
        
#         # Logique de mise à jour dans la base de données
#         # Exemple : Mise à jour de l'état des opportunités
#         update_query = "UPDATE opportunities SET sent = TRUE WHERE id IN %s"
#         cursor.execute(update_query, (tuple(opportunity_ids),))
#         connection.commit()
        
#         logging.info(f"{len(opportunity_ids)} opportunités marquées comme envoyées.")
#     except Exception as e:
#         logging.error(f"Erreur lors de la mise à jour des opportunités : {str(e)}")


def mark_opportunities_as_sent(opportunity_ids):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        logging.info("Connexion réussie à la base de données.")

        cursor = conn.cursor()  # Création du curseur
        logging.info("Connexion à la base de données pour mise à jour des opportunités.")
        
        # Logique de mise à jour dans la base de données
        update_query = "UPDATE opportunities_etudes SET send = TRUE WHERE id IN %s"
        cursor.execute(update_query, (tuple(opportunity_ids),))  # Utilisation du curseur ici
        conn.commit()  # Appliquer les changements
        
        logging.info(f"{len(opportunity_ids)} opportunités marquées comme envoyées.")
    except Exception as e:
        logging.error(f"Erreur lors de la mise à jour des opportunités : {str(e)}")
    finally:
        # Fermeture du curseur et de la connexion
        if cursor:
            cursor.close()
        if conn:
            conn.close()