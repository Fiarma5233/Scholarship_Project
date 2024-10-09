# Importer les fonctions nécessaires depuis utils/utils.py
from installations.dependancies import     install_python_dependencies, install_chrome_and_chromedriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
from dotenv import load_dotenv

# utils.py
# fonction d'importations des bibliotheques
def setup_scraping_environment():
    import pandas as pd
    import time
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from bs4 import BeautifulSoup

    return pd, time, webdriver, By, Service, Options, BeautifulSoup


# def configure_chrome():
#     # Appeler la fonction pour installer Chrome et ChromeDriver si nécessaire
#     install_chrome_and_chromedriver()

#     # Configuration des options pour utiliser Chrome
#     pd, time, webdriver, By, Service, options, BeautifulSoup = setup_scraping_environment()  # Déballage du tuple
#     chrome_options = options()  # Affecter seulement l'objet Options

#     chrome_options.add_argument("--headless")  # Exécuter Chrome en mode headless (sans interface graphique)
#     chrome_options.add_argument("--no-sandbox")  # Désactiver le sandboxing
#     chrome_options.add_argument("--disable-dev-shm-usage")  # Améliorer la stabilité
#     chrome_options.add_argument('--disable-gpu')  # Désactiver l'accélération GPU

#     # Lancer Chrome avec les options configurées
#     service = Service('/usr/local/bin/chromedriver')  # Spécifier le chemin vers le ChromeDriver
#     driver = webdriver.Chrome(service=service, options=chrome_options)
    
#     return driver


def configure_chrome():
    """
    Configure les options de Chrome pour le scraping.

    Returns:
        webdriver.Chrome: Le pilote Chrome configuré.
    """
    from selenium import webdriver  # Import webdriver
    from selenium.webdriver.chrome.service import Service  # Import Service class
    from webdriver_manager.chrome import ChromeDriverManager  # Import ChromeDriverManager

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")  

    chrome_options.add_argument('--disable-gpu')  


    # Utiliser webdriver-manager pour gérer ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    return driver


def load_env_variables():
    load_dotenv()  # Charge les variables d'environnement depuis le fichier .env
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    return username, password
