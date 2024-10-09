import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def test_email():
    subject = "Test Email"
    body = "Ceci est un e-mail de test pour vérifier la configuration SMTP."
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USERNAME
    msg["To"] = SMTP_USERNAME  # Envoyer à soi-même pour le test

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Sécuriser la connexion
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, SMTP_USERNAME, msg.as_string())
        server.quit()
        print("E-mail de test envoyé avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail de test : {e}")

# Exécuter la fonction pour tester l'envoi d'e-mail
test_email()
