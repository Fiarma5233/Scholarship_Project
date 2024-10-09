from scrapping.utils import setup_scraping_environment, configure_chrome, load_env_variables


# Configurer l'environnement de scraping
pd, time, webdriver, By, Service, Options, BeautifulSoup = setup_scraping_environment()


# Définir une fonction pour obtenir le nombre total de pages d'une pagination sur un site web
def get_total_pages(url):
    """
    Fonction pour obtenir le nombre total de pages d'une pagination sur un site web.

    Args:
        url (str): URL de la page contenant la pagination.
        chromedriver_path (str): Chemin vers le fichier ChromeDriver. Par défaut, '/usr/local/bin/chromedriver'.

    Returns:
        int: Nombre total de pages.
    """
    

    driver = configure_chrome()  # Utilisation de la fonction configurée dans utils.py


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
####################################################Fonction d'extraction des urls de toutes les pages ###############

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

############################## Fonction d'extraction  des liens ####################

def extract_links_from_pages(urls_pages):
    """
    Fonction pour extraire les liens de bourses à partir de plusieurs pages web.

    Args:
        urls_pages (list): Liste des URLs des pages à parcourir.
        chromedriver_path (str): Chemin vers le fichier ChromeDriver. Par défaut, '/usr/local/bin/chromedriver'.

    Returns:
        list: Liste des liens extraits des pages.
    """
   

    # Initialiser le navigateur Chrome
    driver = configure_chrome()  # Utilisation de la fonction configurée dans utils.py

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

##################    Fonction pour extraire des informations sur les bourses à partir de plusieurs URLs.#########################


def extract_bourse_info_from_urls(urls):
    """
    Fonction pour extraire des informations sur les bourses à partir de plusieurs URLs.

    Args:
        urls (list): Liste des URLs des bourses à analyser.
        chromedriver_path (str): Chemin vers le fichier ChromeDriver. Par défaut, '/usr/local/bin/chromedriver'.

    Returns:
        dict: Dictionnaire contenant des listes avec les informations extraites (titres, dates limites, etc.).
    """
   

    # Initialiser le navigateur Chrome
    driver = configure_chrome()  # Utilisation de la fonction configurée dans utils.py


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



####################################################
# url_bourses = 'https://greatyop.com/category/bourses/'
# # Appeler la fonction et stocker le nombre total de pages dans la variable 'total_pages_bourses'
# total_pages_bourses = get_total_pages(url_bourses)




# url_stages = 'https://greatyop.com/category/stages-emplois/'

# # Appeler la fonction et stocker le nombre total de pages dans la variable 'total_pages_stages'
# total_pages_stages = get_total_pages(url_stages)


# url_formations = 'https://greatyop.com/category/formations/'
# # Appeler la fonction et stocker le nombre total de pages dans la variable 'total_pages_formations'
# total_pages_formations = get_total_pages(url_formations)

# ####################### Appel de fonctions 

# urls_pages_bourses = generate_page_urls(url_bourses, total_pages_bourses)


# urls_pages_stages = generate_page_urls(url_stages, total_pages_stages)

# urls_pages_formations = generate_page_urls(url_formations, total_pages_formations)

# #################################

# liens_bourses = extract_links_from_pages(urls_pages_bourses)

# liens_stages = extract_links_from_pages(urls_pages_stages)

# liens_formations = extract_links_from_pages(urls_pages_formations)

# #######################

# bourses = extract_bourse_info_from_urls(liens_bourses)

# df_bourses = pd.DataFrame(bourses)

# df_bourses.to_csv('bourses.csv')

# stages = extract_bourse_info_from_urls(liens_stages)

# df_stages = pd.DataFrame(stages)

# df_stages['Type'] = 'Stage'

# df_stages.to_csv('stages.csv')


# formations = extract_bourse_info_from_urls(liens_formations)

# df_formations = pd.DataFrame(formations)

# df_formations['Type'] = 'Formation'

# df_formations.to_csv('formations.csv')