from users.send_email import get_opportunities_and_users  
from flask import Flask, request, redirect, url_for, flash
import os
import smtplib
import pandas as pd
from sqlalchemy import create_engine
from email.mime.text import MIMEText
from dotenv import load_dotenv
# Charger les variables d'environnement
load_dotenv()



from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader

# Configuration pour l'envoi d'e-mails
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = os.getenv("SMTP_USERNAME")  # Ton adresse Gmail
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # Ton mot de passe ou App Password


def send_weekly_opportunities_email_to_users(opportunites, users):
    """
    Envoie des emails aux utilisateurs avec les informations des stages.
    
    :param stages: Liste des stages à inclure dans l'email
    :param users: Liste des utilisateurs (chaque utilisateur étant une liste contenant l'email et le nom)
    """
    # Configuration de l'environnement Jinja2 pour charger les templates
    env = Environment(loader=FileSystemLoader('templates'))
    env.globals['url_for'] = url_for  # Ajoute url_for aux globals de Jinja2

    template = env.get_template('email.html')  # Template HTML créé auparavant
    
    # Connexion au serveur SMTP
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
    except smtplib.SMTPException as e:
        print(f"Erreur lors de la connexion au serveur SMTP : {e}")
        return
    
    for user in users:
        email = user[1]  # Assumant que l'email est dans la deuxième colonne (index 1)
        name = user[2]   # Assumant que le nom est dans la troisième colonne (index 2)
        
        # Préparation du sujet et du contenu de l'email
        subject = "Opportunites d'etudes toujours disponibles"
        
        # Rendu du template avec les données utilisateur et stages
        html_content = template.render(nom=name, opportunites=opportunites)
        
        # Création du message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SMTP_USERNAME
        msg["To"] = email
        
        # Attacher le contenu HTML à l'email
        msg.attach(MIMEText(html_content, 'html'))
        
        # Envoi de l'email
        try:
            server.sendmail(SMTP_USERNAME, email, msg.as_string())
            print(f"E-mail envoyé avec succès à {email}")
        except smtplib.SMTPException as e:
            print(f"Erreur lors de l'envoi de l'e-mail à {email}: {e}")
    
    # Fermer la connexion SMTP
    server.quit()

opportunities, users = get_opportunities_and_users()

if __name__ == '__main__':
    send_weekly_opportunities_email_to_users(opportunites=opportunities, users=users)