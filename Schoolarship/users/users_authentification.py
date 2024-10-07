# from flask import Flask, request, redirect, url_for, flash
# import os
# import psycopg2
# import smtplib
# from flask import Blueprint
# from oauthlib.oauth2 import WebApplicationClient
# import requests
# from email.mime.text import MIMEText
# from dotenv import load_dotenv
# from databases.db import get_db_connection

# # Charger les variables d'environnement
# load_dotenv()

# # Configuration du client OAuth 2.0
# GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
# GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
# GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
# client = WebApplicationClient(GOOGLE_CLIENT_ID)

# # Créer un blueprint pour les routes liées à l'authentification
# auth_blueprint = Blueprint('auth', __name__)

# # Configuration pour l'envoi d'e-mails
# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587
# SMTP_USERNAME = os.getenv("SMTP_USERNAME")  # Ton adresse Gmail
# SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # Ton mot de passe ou App Password

# def create_users_table():
#     sql_file_path = './users/users_table.sql'
    
#     with open(sql_file_path, 'r') as sql_file:
#         sql_commands = sql_file.read()

#     conn = get_db_connection()
#     cur = conn.cursor()

#     try:
#         cur.execute(sql_commands)
#         conn.commit()
#         print("Table users créée avec succès.")
#     except Exception as e:
#         print(f"Erreur lors de la création de la table: {e}")
#         conn.rollback()
#     finally:
#         cur.close()
#         conn.close()

# def send_welcome_email(email, name):
#     subject = "Bienvenue aux informations sur les opportunités d'études"
#     body = f"Bonjour {name},\n\nVous recevrez désormais des informations sur les nouvelles opportunités d'études disponibles.\n\nCordialement,\nL'équipe."
    
#     msg = MIMEText(body)
#     msg["Subject"] = subject
#     msg["From"] = SMTP_USERNAME
#     msg["To"] = email
    
#     try:
#         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
#         server.starttls()
#         server.login(SMTP_USERNAME, SMTP_PASSWORD)
#         server.sendmail(SMTP_USERNAME, email, msg.as_string())
#         server.quit()
#         print(f"E-mail envoyé avec succès à {email}")
#     except smtplib.SMTPException as e:
#         print(f"Erreur lors de l'envoi de l'e-mail à {email}: {e}")

# @auth_blueprint.route("/login")
# def login():
#     google_provider_cfg = get_google_provider_cfg()
#     authorization_endpoint = google_provider_cfg["authorization_endpoint"]

#     request_uri = client.prepare_request_uri(
#         authorization_endpoint,
#         redirect_uri="http://127.0.0.1:5000/login/callback",
#         scope=["openid", "email", "profile"],
#     )
#     return redirect(request_uri)

# @auth_blueprint.route("/login/callback")
# def callback():
#     code = request.args.get("code")

#     google_provider_cfg = get_google_provider_cfg()
#     token_endpoint = google_provider_cfg["token_endpoint"]
#     token_url, headers, body = client.prepare_token_request(
#         token_endpoint,
#         authorization_response=request.url,
#         redirect_url=request.base_url,
#         code=code
#     )
#     token_response = requests.post(
#         token_url,
#         headers=headers,
#         data=body,
#         auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
#     )

#     if token_response.status_code != 200:
#         return redirect(url_for('/', message="Erreur lors de l'échange du code d'autorisation.", is_error=True))

#     client.parse_request_body_response(token_response.text)
#     userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
#     uri, headers, body = client.add_token(userinfo_endpoint)
#     userinfo_response = requests.get(uri, headers=headers, data=body)

#     if userinfo_response.status_code != 200:
#         return redirect(url_for('/', message="Erreur lors de la récupération des informations de l'utilisateur.", is_error=True))

#     userinfo = userinfo_response.json()
#     if userinfo.get("email_verified"):
#         email = userinfo["email"]
#         name = userinfo.get("name", "Nom inconnu")

#         conn = get_db_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute(
#                 "INSERT INTO users (email, name) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING",
#                 (email, name)
#             )
#             conn.commit()
#             if cur.rowcount > 0:
#                 send_welcome_email(email, name)
#                 message = f"Email {email} et nom {name} enregistrés avec succès ! Un e-mail de bienvenue a été envoyé."
#                 return redirect(url_for('/', message=message, is_error=False))
#             else:
#                 message = f"L'utilisateur avec l'email {email} existe déjà."
#                 return redirect(url_for('/', message=message, is_error=True))
#         except Exception as e:
#             conn.rollback()
#             return redirect(url_for('/', message=f"Erreur lors de l'enregistrement : {e}", is_error=True))
#         finally:
#             cur.close()
#             conn.close()
#     return redirect(url_for('/', message="Erreur : l'utilisateur n'a pas de compte Google vérifié.", is_error=True))

# def get_google_provider_cfg():
#     return requests.get(GOOGLE_DISCOVERY_URL).json()


from flask import Flask, request, redirect, url_for, flash
import os
import psycopg2
import smtplib
from flask import Blueprint
from oauthlib.oauth2 import WebApplicationClient
import requests
from email.mime.text import MIMEText
from dotenv import load_dotenv
from databases.db import get_db_connection

from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader

# Charger les variables d'environnement
load_dotenv()

# Configuration du client OAuth 2.0
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Créer un blueprint pour les routes liées à l'authentification
auth_blueprint = Blueprint('auth', __name__)

# Configuration pour l'envoi d'e-mails
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = os.getenv("SMTP_USERNAME")  # Ton adresse Gmail
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # Ton mot de passe ou App Password

def create_users_table():
    sql_file_path = './users/users_table.sql'
    
    with open(sql_file_path, 'r') as sql_file:
        sql_commands = sql_file.read()

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(sql_commands)
        conn.commit()
        print("Table users créée avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création de la table: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

# def send_welcome_email(email, name):
#     subject = "Bienvenue aux informations sur les opportunités d'études"
#     body = f"Bonjour {name},\n\nVous recevrez désormais des informations sur les nouvelles opportunités d'études disponibles.\n\nCordialement,\nL'équipe."
    
#     msg = MIMEText(body)
#     msg["Subject"] = subject
#     msg["From"] = SMTP_USERNAME
#     msg["To"] = email
    
#     try:
#         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
#         server.starttls()
#         server.login(SMTP_USERNAME, SMTP_PASSWORD)
#         server.sendmail(SMTP_USERNAME, email, msg.as_string())
#         server.quit()
#         print(f"E-mail envoyé avec succès à {email}")
#     except smtplib.SMTPException as e:
#         print(f"Erreur lors de l'envoi de l'e-mail à {email}: {e}")

##################

def send_welcome_email(email, name):

    # Configuration de l'environnement Jinja2 pour charger les templates
    env = Environment(loader=FileSystemLoader('templates'))
    env.globals['url_for'] = url_for  # Ajoute url_for aux globals de Jinja2

    template = env.get_template('welcome_email.html')  # Template HTML créé auparavant
# Rendu du template avec les données utilisateur et stages
    html_content = template.render(email=email, name=name)
    subject = "Bienvenue aux informations sur les opportunités d'études"
    body = f"Bonjour {name},\n\nVous recevrez désormais des informations sur les nouvelles opportunités d'études disponibles.\n\nCordialement,\nL'équipe."
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SMTP_USERNAME
    msg["To"] = email
    # Attacher le contenu HTML à l'email
    msg.attach(MIMEText(html_content, 'html'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, email, msg.as_string())
        server.quit()
        print(f"E-mail envoyé avec succès à {email}")
    except smtplib.SMTPException as e:
        print(f"Erreur lors de l'envoi de l'e-mail à {email}: {e}")



@auth_blueprint.route("/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri="http://127.0.0.1:5000/login/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@auth_blueprint.route("/login/callback")
def callback():
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    if token_response.status_code != 200:
        return redirect(url_for('opportunites', message="Erreur lors de l'échange du code d'autorisation.", is_error=True))

    client.parse_request_body_response(token_response.text)
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.status_code != 200:
        return redirect(url_for('opportunites', message="Erreur lors de la récupération des informations de l'utilisateur.", is_error=True))

    userinfo = userinfo_response.json()
    if userinfo.get("email_verified"):
        email = userinfo["email"]
        name = userinfo.get("name", "Nom inconnu")

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (email, name) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING",
                (email, name)
            )
            conn.commit()
            if cur.rowcount > 0:
                send_welcome_email(email, name)
                message = f"Email {email} et nom {name} enregistrés avec succès ! Un e-mail de bienvenue a été envoyé."
                return redirect(url_for('opportunites', message=message, is_error=False))
            else:
                message = f"L'utilisateur avec l'email {email} existe déjà."
                return redirect(url_for('opportunites', message=message, is_error=True))
        except Exception as e:
            conn.rollback()
            return redirect(url_for('opportunites', message=f"Erreur lors de l'enregistrement : {e}", is_error=True))
        finally:
            cur.close()
            conn.close()
    return redirect(url_for('opportunites', message="Erreur : l'utilisateur n'a pas de compte Google vérifié.", is_error=True))

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()
