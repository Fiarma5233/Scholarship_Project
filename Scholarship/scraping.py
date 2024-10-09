# Importer le module 'importlib' pour gérer les imports dynamiques
import importlib

import os

# Définir une fonction pour vérifier et installer un module si nécessaire
def install_if_needed(module_name, package_name=None):
    # Si 'package_name' n'est pas fourni, utiliser 'module_name'
    if package_name is None:
        package_name = module_name

    try:
        # Essayer d'importer le module
        importlib.import_module(module_name)
        # Indiquer que le module est déjà installé
        print(f"{package_name} est déjà installé.")
    except ImportError:
        # Indiquer que le module n'est pas installé et qu'on va l'installer
        print(f"{package_name} n'est pas installé. Installation en cours...")
        # Installer le package avec pip
        os.system(f'pip install {package_name}')  # Remplacer !pip par os.system pour fonctionner dans des scripts
        # Indiquer que le package a été installé avec succès
        print(f"{package_name} a été installé avec succès.")

# Vérifier et installer 'requests' si nécessaire
install_if_needed("requests")

# Vérifier et installer 'bs4' si nécessaire
install_if_needed("bs4")

# Vérifier et installer 'beautifulsoup4' si nécessaire
install_if_needed("beautifulsoup4", "beautifulsoup4")



import requests
from bs4 import BeautifulSoup
import pandas as pd

# Importer le module 'os' pour exécuter des commandes système
import os

# Vérifier si Selenium est déjà installé
try:
    # Essayer d'importer Selenium
    import selenium
    # Indiquer que Selenium est déjà installé
    print("Selenium est déjà installé.")
except ImportError:
    # Indiquer que Selenium n'est pas installé et que l'installation va commencer
    print("Installation de Selenium...")
    # Installer Selenium en utilisant pip
    os.system('pip install selenium')

# Vérifier si Google Chrome est déjà installé
# Exécuter une commande pour obtenir la version de Google Chrome et vérifier si elle réussit
chrome_installed = os.system("google-chrome --version") == 0

# Si Google Chrome n'est pas installé
if not chrome_installed:
    # Indiquer que l'installation de Google Chrome va commencer
    print("Installation de Google Chrome...")
    # Mettre à jour les index des paquets
    os.system('apt-get update')
    # Installer wget et unzip pour télécharger et décompresser le fichier d'installation
    os.system('apt-get install -y wget unzip')
    # Télécharger le fichier .deb pour Google Chrome
    os.system('wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb')
    # Installer Google Chrome en utilisant le fichier .deb
    os.system('dpkg -i google-chrome-stable_current_amd64.deb')
    # Corriger les problèmes de dépendances éventuels
    os.system('apt-get -f install -y')
else:
    # Indiquer que Google Chrome est déjà installé
    print("Google Chrome est déjà installé.")

# Vérifier si ChromeDriver est déjà installé
# Exécuter une commande pour obtenir la version de ChromeDriver et vérifier si elle réussit
chromedriver_installed = os.system("chromedriver --version") == 0

# Si ChromeDriver n'est pas installé
if not chromedriver_installed:
    # Indiquer que l'installation de ChromeDriver va commencer
    print("Installation de ChromeDriver...")
    # Télécharger le fichier zip contenant ChromeDriver
    os.system('wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/128.0.6613.119/linux64/chromedriver-linux64.zip')
    # Décompresser le fichier zip
    os.system('unzip chromedriver-linux64.zip')
    # Déplacer le fichier chromedriver dans /usr/local/bin pour le rendre exécutable depuis n'importe quel endroit
    os.system('mv chromedriver-linux64/chromedriver /usr/local/bin/')
    # Rendre le fichier chromedriver exécutable
    os.system('chmod +x /usr/local/bin/chromedriver')
else:
    # Indiquer que ChromeDriver est déjà installé
    print("ChromeDriver est déjà installé.")

# Vérification des versions installées
# Afficher la version de Google Chrome installée
print("Vérification des versions installées :")
os.system('google-chrome --version')
# Afficher la version de ChromeDriver installée
os.system('chromedriver --version')

# Importer les modules nécessaires pour utiliser Selenium et manipuler les données
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time






# Configuration des options pour utiliser Chrome dans Colab
chrome_options = Options()
# Exécuter Chrome en mode headless (sans interface graphique)
chrome_options.add_argument("--headless")
# Désactiver le sandboxing pour éviter les problèmes de sécurité
chrome_options.add_argument("--no-sandbox")
# Désactiver l'utilisation du /dev/shm, ce qui peut améliorer la stabilité dans certains environnements
chrome_options.add_argument("--disable-dev-shm-usage")
# Désactiver l'accélération GPU pour éviter les problèmes graphiques
chrome_options.add_argument('--disable-gpu')

# Lancer Chrome avec les options configurées
service = Service('/usr/local/bin/chromedriver')  # Spécifier le chemin vers le ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)  # Démarrer le navigateur

# URL des pages à ouvrir
url_bourses = 'https://www.campusfaso.bf/formations/bourses'  # URL de la page des bourses
url_connexion = "https://www.campusfaso.bf/candidat/acceder-compte"  # URL de la page de connexion

# Ouvrir la page de connexion
driver.get(url_connexion)

# Trouver les champs de connexion
username_input = driver.find_element(By.ID, "login")  # Champ pour l'identifiant
password_input = driver.find_element(By.ID, "mdp")  # Champ pour le mot de passe

# Saisir les identifiants pour se connecter
username_input.send_keys("N00330120211")  # Remplacer par ton identifiant
password_input.send_keys("Nup6X4psB")  # Remplacer par ton mot de passe

# Soumettre le formulaire de connexion
login_button = driver.find_element(By.ID, "connecter")  # Bouton de connexion
login_button.click()  # Cliquer sur le bouton de connexion

# Pause pour laisser le temps de connexion
time.sleep(5)  # Attendre 5 secondes pour que la connexion soit traitée

# Accéder à la page des bourses
driver.get(url_bourses)

# Attendre le chargement complet de la page des bourses
time.sleep(5)  # Attendre 5 secondes pour s'assurer que la page est complètement chargée

# Trouver toutes les sections contenant les informations des bourses
bourses = driver.find_elements(By.CLASS_NAME, "col-md-4.col-sm-6")  # Sélectionner toutes les sections avec la classe spécifiée

# Utiliser des sets pour éviter les doublons dans les titres des bourses
titres_set = set()

# Listes pour stocker les informations des bourses
titres = []  # Liste pour les titres des bourses
descriptionss = []  # Liste pour les descriptions des bourses
dates_limite = []  # Liste pour les dates limites de candidature
pays = []  # Liste pour les pays associés aux bourses
liens_combines = []  # Liste pour les liens associés aux bourses
no_bourses = []  # Liste pour le nombre de bourses
premier_liens = []  # Liste pour le premier lien trouvé

# Boucle pour extraire les informations de chaque bourse
for bourse in bourses:
    try:
        # Extraire le titre de la bourse
        titre = bourse.find_element(By.TAG_NAME, "h4").text

        if titre not in titres_set:  # Vérifier si le titre est déjà extrait
            titres_set.add(titre)

            # Trouver toutes les balises <p> dans chaque section de bourse
            p_tags = bourse.find_elements(By.TAG_NAME, "p")

            if len(p_tags) > 0:
                # Trouver toutes les balises <strong> dans la première balise <p>
                strong_tags = p_tags[0].find_elements(By.TAG_NAME, "strong")

                # Vérifier si strong_tags contient suffisamment d'éléments
                if len(strong_tags) > 0:
                    # Récupérer le nombre de bourses
                    nombre_bourse = strong_tags[0].text.strip()  # Extraire et nettoyer le texte de la balise <strong>

                    # Vérifier si le texte est vide
                    if nombre_bourse == "":
                        no_bourses.append("Non spécifié")
                    else:
                        no_bourses.append(nombre_bourse)

                # Date limite (3ème <strong>)
                if len(strong_tags) >= 3:
                    date_limite = strong_tags[2].text
                else:
                    date_limite = "Date limite non trouvée"

                # Pays (4ème et dernière <strong>)
                if len(strong_tags) >= 4:
                    pays_val = strong_tags[3].text
                else:
                    pays_val = "Pays non trouvé"
            else:
                date_limite = "Date limite non trouvée"
                pays_val = "Pays non trouvé"

            # Description à partir de la deuxième balise <p>
            if len(p_tags) > 1:
                description = p_tags[1].text
            else:
                description = "Description non trouvée"

            # Trouver toutes les balises <a> après la dernière balise <p>
            a_tags = bourse.find_elements(By.TAG_NAME, "a")

            # Prendre seulement le premier lien
            if a_tags:
                premier_lien = a_tags[0].get_attribute('href')
                premier_liens.append(premier_lien)
            else:
                premier_lien = "Lien non trouvé"

            # Extraire tous les liens
            liens = [a_tag.get_attribute('href') for a_tag in a_tags]

            # Ajouter la liste de liens sans concaténation
            if liens:
                liens_combines_ = liens  # On garde simplement la liste des liens
            else:
                liens_combines_ = ["Lien non trouvé"]

            # Vérifier si les informations sont valides avant de les ajouter
            if titre != "BURKINA FASO" and date_limite != "Date limite non trouvée" and pays_val != "Pays non trouvé" and description != "Description non trouvée":
                titres.append(titre)
                dates_limite.append(date_limite)
                pays.append(pays_val)
                descriptionss.append(description)
                liens_combines.append(liens_combines_)

    except Exception as e:
        # Gérer les exceptions en cas d'erreur lors de l'extraction des informations
        print(f"Erreur lors de l'extraction d'une bourse: {str(e)}")

# Fermer le navigateur une fois le scraping terminé
driver.quit()




# Créer un DataFrame avec les informations extraites
df_bourses_campusfaso = pd.DataFrame({
    'Pays': pays,
    'Titre': titres,
    "Type" : "Bourse",
    'Description': descriptionss,
    'Niveau':titres,
    'Financement':premier_liens,
    'Date Limite': dates_limite,
    'Conditions': liens_combines,
    "Nombre de bourses": no_bourses,
    "Domaine Conserné": premier_liens,
    "Durée d'étude": premier_liens,
    "Pays éligibles": premier_liens


})


df_bourses_campusfaso.to_csv("bourses_campusfaso.csv", index=False)

# Définir une fonction pour obtenir le nombre total de pages d'une pagination sur un site web
def get_total_pages(url, chromedriver_path='/usr/local/bin/chromedriver'):
    """
    Fonction pour obtenir le nombre total de pages d'une pagination sur un site web.

    Args:
        url (str): URL de la page contenant la pagination.
        chromedriver_path (str): Chemin vers le fichier ChromeDriver. Par défaut, '/usr/local/bin/chromedriver'.

    Returns:
        int: Nombre total de pages.
    """
    # Configurer les options pour Chrome
    chrome_options = Options()
    # Exécuter en mode headless (sans interface graphique)
    chrome_options.add_argument("--headless")
    # Éviter les problèmes de sandboxing
    chrome_options.add_argument("--no-sandbox")
    # Éviter les problèmes de gestion de la mémoire
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Définir le chemin vers ChromeDriver
    webdriver_service = Service(chromedriver_path)

    # Initialiser le navigateur Chrome avec les options et le service définis
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    try:
        # Accéder à la page spécifiée
        driver.get(url)

        # Trouver le nombre total de pages
        try:
            # Trouver tous les éléments avec la classe 'page-numbers'
            page_number_elements = driver.find_elements(By.CSS_SELECTOR, '.page-numbers')

            # Extraire les numéros de page en convertissant le texte des éléments en entiers
            page_numbers = [int(el.text) for el in page_number_elements if el.text.isdigit()]

            # Trouver le plus grand numéro de page parmi ceux extraits
            if page_numbers:
                last_page_number = max(page_numbers)
                # Afficher le nombre total de pages
                print(f"Nombre total de pages : {last_page_number}")
                # Retourner le nombre total de pages
                return last_page_number
            else:
                # Afficher un message si aucun numéro de page n'est trouvé
                print("Aucun numéro de page trouvé.")
                # Retourner 0 si aucun numéro de page n'est trouvé
                return 0

        except Exception as e:
            # Afficher un message d'erreur en cas d'exception lors de l'extraction des numéros de page
            print(f"Erreur lors de l'extraction des numéros de page: {str(e)}")
            # Retourner 0 en cas d'erreur
            return 0

    finally:
        # Fermer le navigateur pour libérer les ressources
        driver.quit()


url_bourses = 'https://greatyop.com/category/bourses/'
# Appeler la fonction et stocker le nombre total de pages dans la variable 'total_pages_bourses'
total_pages_bourses = get_total_pages(url_bourses)




url_stages = 'https://greatyop.com/category/stages-emplois/'

# Appeler la fonction et stocker le nombre total de pages dans la variable 'total_pages_stages'
total_pages_stages = get_total_pages(url_stages)


url_formations = 'https://greatyop.com/category/formations/'
# Appeler la fonction et stocker le nombre total de pages dans la variable 'total_pages_formations'
total_pages_formations = get_total_pages(url_formations)

def generate_page_urls(base_url, total_pages):
    """
    Fonction pour générer une liste d'URLs pour chaque page d'une pagination.

    Args:
        base_url (str): L'URL de base pour la pagination.
        last_page_number (int): Le numéro de la dernière page.

    Returns:
        list: Liste des URLs pour chaque page de la pagination.
    """
    # Liste pour stocker les URLs des pages
    urls_pages = []

    # Boucle pour générer les URLs pour chaque page
    for page_number in range(1, total_pages + 1):
        # Créer l'URL pour la page actuelle
        page_url = f'{base_url}page/{page_number}/'
        # Ajouter l'URL à la liste
        urls_pages.append(page_url)

    return urls_pages

urls_pages_bourses = generate_page_urls(url_bourses, total_pages_bourses)

urls_pages_bourses

urls_pages_stages = generate_page_urls(url_stages, total_pages_stages)

urls_pages_stages

urls_pages_formations = generate_page_urls(url_formations, total_pages_formations)

urls_pages_formations



def extract_links_from_pages(urls_pages, chromedriver_path='/usr/local/bin/chromedriver'):
    """
    Fonction pour extraire les liens de bourses à partir de plusieurs pages web.

    Args:
        urls_pages (list): Liste des URLs des pages à parcourir.
        chromedriver_path (str): Chemin vers le fichier ChromeDriver. Par défaut, '/usr/local/bin/chromedriver'.

    Returns:
        list: Liste des liens extraits des pages.
    """
    # Configurer les options pour Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Exécuter en mode headless (sans interface graphique)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Définir le chemin vers ChromeDriver
    webdriver_service = Service(chromedriver_path)

    # Initialiser le navigateur Chrome
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    # Liste pour stocker les liens extraits
    liens = []

    try:
        for url in urls_pages:
            # Accéder à la page web
            driver.get(url)

            # Attendre que la page se charge complètement
            time.sleep(3)

            # Utiliser BeautifulSoup pour parser le contenu de la page
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Trouver tous les div de classe "entry-header"
            bourses = soup.find_all('div', class_='entry-header')

            # Parcourir chaque div.entry-header pour vérifier les conditions
            for bourse in bourses:
                # Trouver la balise h2 qui contient le lien
                h2_tag = bourse.find('h2')

                if h2_tag:
                    # Récupérer le lien href de la balise a dans h2
                    lien = h2_tag.find('a')['href']

                    # Trouver le div.gy-pcard-bottom associé (balise suivante à entry-header)
                    next_div = bourse.find_next('div', class_='gy-pcard-bottom')

                    if next_div:
                        # Vérifier si le contenu de la balise p est différent de "Clôturé(e)"
                        status_p = next_div.find('p')
                        if status_p and status_p.text.strip() != "Clôturé(e)":
                            # Ajouter le lien à la liste si la condition est remplie
                            liens.append(lien)

    finally:
        # Fermer le driver après l'extraction des pages
        driver.quit()

    return liens


liens_bourses = extract_links_from_pages(urls_pages_bourses)

liens_bourses

liens_stages = extract_links_from_pages(urls_pages_stages)

liens_stages

liens_formations = extract_links_from_pages(urls_pages_formations)

liens_formations



def extract_bourse_info_from_urls(urls, chromedriver_path='/usr/local/bin/chromedriver'):
    """
    Fonction pour extraire des informations sur les bourses à partir de plusieurs URLs.

    Args:
        urls (list): Liste des URLs des bourses à analyser.
        chromedriver_path (str): Chemin vers le fichier ChromeDriver. Par défaut, '/usr/local/bin/chromedriver'.

    Returns:
        dict: Dictionnaire contenant des listes avec les informations extraites (titres, dates limites, etc.).
    """
    # Configurer les options pour Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Exécuter en mode headless (sans interface graphique)
    chrome_options.add_argument("--no-sandbox")  # Désactiver le sandboxing
    chrome_options.add_argument("--disable-dev-shm-usage")  # Désactiver l'utilisation du shared memory

    # Définir le chemin vers ChromeDriver
    webdriver_service = Service(chromedriver_path)

    # Initialiser le navigateur Chrome
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    # Initialiser les listes pour stocker les informations de chaque bourse
    liens = []  # Liste pour stocker les URLs
    titres_bourses = []  # Liste pour stocker les titres des bourses
    dates_limites = []  # Liste pour stocker les dates limites des bourses
    niveaux = []  # Liste pour stocker les niveaux des bourses
    financements = []  # Liste pour stocker les types de financement des bourses
    pays_etudes = []  # Liste pour stocker les pays d'étude des bourses
    statuts = []  # Liste pour stocker les statuts des bourses
    descriptions = []  # Liste pour stocker les descriptions des bourses
    domaines_etudes = []  # Liste pour stocker les domaines d'études des bourses
    nombres_bourses = []  # Liste pour stocker le nombre de bourses disponibles
    pays_eligibles_list = []  # Liste pour stocker les pays éligibles pour chaque bourse
    durees_etudes = []  # Liste pour stocker les durées d'étude

    try:
        # Parcourir chaque URL pour extraire les informations
        for url in urls:
            # Ajouter l'URL à la liste des liens
            liens.append(url)
            # Charger la page web à partir de l'URL
            driver.get(url)
            # Attendre 3 secondes pour que la page se charge complètement
            time.sleep(3)

            # Utiliser BeautifulSoup pour parser le contenu de la page
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extraire le titre de la bourse
            titre_bourse = soup.find('h1')
            if titre_bourse:
                titres_bourses.append(titre_bourse.text.strip())  # Ajouter le titre à la liste
            else:
                titres_bourses.append("Titre non spécifié")  # Ajouter un message par défaut si le titre n'est pas trouvé

            # Initialiser les valeurs par défaut pour les informations de la bourse
            date_limite = "Date limite non spécifiée"
            niveau = "Niveau non spécifié"
            financement = "Type de financement non spécifié"
            pays_etude = "Pays d'étude non spécifié"
            statut = "Statut non spécifié"
            description = ""  # Par défaut, vide
            duree_etude = "Durée d'étude non spécifiée"

            # Extraire les informations depuis la div.app_summary
            summary_div = soup.find('div', class_='app_summary gy-ncp')

            if summary_div:
                sum_infos = summary_div.find_all('div', class_='sum_info')

                # Parcourir les informations extraites depuis sum_info
                for info in sum_infos:
                    texte = info.get_text(strip=True)
                    if "DATE LIMITE" in texte:
                        date_limite = texte.split(':', 1)[1].strip()  # Extraire la date limite
                    elif "NIVEAU" in texte:
                        niveau = texte.split(':', 1)[1].strip()  # Extraire le niveau
                    elif "FINANCE" in texte:
                        financement = texte.split(':', 1)[1].strip()  # Extraire le type de financement

                # Extraire le pays d'étude depuis la div.studyin
                studyin_div = summary_div.find('div', class_='sum_info studyin')
                if studyin_div:
                    texte = studyin_div.get_text(strip=True)
                    if ':' in texte:
                        pays_etude = texte.split(':', 1)[1].strip()  # Extraire le pays d'étude

                # Extraire le statut depuis la dernière div.sum_info
                last_sum_info = sum_infos[-1] if sum_infos else None
                if last_sum_info:
                    spans = last_sum_info.find('span', class_='status')
                    if spans:
                        statut = spans.text.strip()  # Extraire le statut

            # Extraire la description de la bourse
            entry_content = soup.find('div', class_='entry-content')
            if entry_content:
                paragraphs = entry_content.find_all('p', class_='gy-ncp')
                if paragraphs:
                    description = " ".join(p.text.strip() for p in paragraphs)  # Extraire et combiner les paragraphes

            # Si aucune description n'a été trouvée, utiliser l'URL comme description
            if not description:
                description = url

            # Extraire les informations depuis la balise ul
            domaine_etude = "Non spécifié"
            nombre_bourses = "Non spécifié"
            pays_eligibles = "Non spécifié"

            if entry_content:
                ul_tags = entry_content.find_all('ul', class_=['gy-details', 'gy-details gy-ncp'])
                if ul_tags:
                    for ul in ul_tags:
                        li_tags = ul.find_all('li')
                        for li in li_tags:
                            strong_tag = li.find('strong')
                            if strong_tag:
                                label = strong_tag.text.strip()
                                content = li.get_text(strip=True).split(':', 1)[1] if ':' in li.get_text(strip=True) else ""
                                if "Domaine d'études" in label or "Domaine" in label or "Domaines" in label or "Domaines d'études" in label or "Programme éligible" in label:
                                    domaine_etude = content.strip()  # Extraire le domaine d'études
                                elif "Nombre de bourses" in label or "Nombre de Bourses" in label or "Nombre de récompenses" in label:
                                    nombre_bourses = content.strip()  # Extraire le nombre de bourses
                                elif "Groupe cible" in label or "Pays éligibles" in label:
                                    pays_eligibles = content.strip()  # Extraire les pays éligibles
                                elif "Durée d'étude" in label or "Durée" in label:
                                    duree_etude = content.strip()  # Extraire la durée d'étude

            # Ajouter les informations extraites à leurs listes respectives
            dates_limites.append(date_limite)
            niveaux.append(niveau)
            financements.append(financement)
            pays_etudes.append(pays_etude)
            statuts.append(statut)
            descriptions.append(description)
            domaines_etudes.append(domaine_etude)
            nombres_bourses.append(nombre_bourses)
            pays_eligibles_list.append(pays_eligibles)
            durees_etudes.append(duree_etude)  # Ajouter la durée d'étude

    finally:
        # Fermer le driver après l'extraction de toutes les pages
        driver.quit()

    # Retourner un dictionnaire avec les informations extraites
    return {
        'Pays': pays_etudes,
        'Titre': titres_bourses,
        "Type" : "Bourse",
        'Description': descriptions,
        'Niveau': niveaux,
        'Financement': financements,
        'Date Limite': dates_limites,
        'Conditions': liens,
        "Nombre de bourses": nombres_bourses,
        "Domaine Conserné": domaines_etudes,
        'Durée d\'étude': durees_etudes,
        "Pays éligibles": pays_eligibles_list,

    }


bourses = extract_bourse_info_from_urls(liens_bourses)

df_bourses = pd.DataFrame(bourses)

df_bourses.to_csv('bourses.csv')

stages = extract_bourse_info_from_urls(liens_stages)

df_stages = pd.DataFrame(stages)

df_stages['Type'] = 'Stage'

df_stages.to_csv('stages.csv')


formations = extract_bourse_info_from_urls(liens_formations)

df_formations = pd.DataFrame(formations)

df_formations['Type'] = 'Formation'

df_formations.to_csv('formations.csv')


df = pd.concat([df_bourses_campusfaso ,df_bourses, df_stages, df_formations], ignore_index=True)

df.to_csv('bourses_etudes.csv')