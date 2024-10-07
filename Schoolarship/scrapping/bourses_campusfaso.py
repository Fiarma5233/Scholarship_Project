# # bourses_campusfaso.py

# from scrapping.utils import setup_scraping_environment, configure_chrome, load_env_variables

# # Charger les variables d'environnement
# username, password = load_env_variables()

# # Configurer l'environnement de scraping
# pd, time, webdriver, By, Service, Options, BeautifulSoup = setup_scraping_environment()

# def scraper_bourses_campusfaso():
#     # Configurer et lancer le navigateur
#     driver = configure_chrome()
    
#     # URL des pages à ouvrir
#     url_bourses = 'https://www.campusfaso.bf/formations/bourses'  # URL de la page des bourses
#     url_connexion = "https://www.campusfaso.bf/candidat/acceder-compte"  # URL de la page de connexion
    
#     # Ouvrir la page de connexion
#     driver.get(url_connexion)
    
#     # Trouver les champs de connexion
#     username_input = driver.find_element(By.ID, "login")  # Champ pour l'identifiant
#     password_input = driver.find_element(By.ID, "mdp")  # Champ pour le mot de passe
    
#     # Saisir les identifiants pour se connecter
#     username_input.send_keys(username)  # Utiliser le nom d'utilisateur chargé depuis .env
#     password_input.send_keys(password)  # Utiliser le mot de passe chargé depuis .env
    
#     # Soumettre le formulaire de connexion
#     login_button = driver.find_element(By.ID, "connecter")  # Bouton de connexion
#     login_button.click()  # Cliquer sur le bouton de connexion
    
#     # Pause pour laisser le temps de connexion
#     time.sleep(5)  # Attendre 5 secondes pour que la connexion soit traitée
    
#     # Accéder à la page des bourses
#     driver.get(url_bourses)
    
#     # Attendre le chargement complet de la page des bourses
#     time.sleep(5)  # Attendre 5 secondes pour s'assurer que la page est complètement chargée
    
#     # Trouver toutes les sections contenant les informations des bourses
#     bourses = driver.find_elements(By.CLASS_NAME, "col-md-4.col-sm-6")  # Sélectionner toutes les sections avec la classe spécifiée
    
#     # Utiliser des sets pour éviter les doublons dans les titres des bourses
#     titres_set = set()
    
#     # Listes pour stocker les informations des bourses
#     titres = []  # Liste pour les titres des bourses
#     descriptionss = []  # Liste pour les descriptions des bourses
#     dates_limite = []  # Liste pour les dates limites de candidature
#     pays = []  # Liste pour les pays associés aux bourses
#     liens_combines = []  # Liste pour les liens associés aux bourses
#     no_bourses = []  # Liste pour le nombre de bourses
#     premier_liens = []  # Liste pour le premier lien trouvé
    
#     # Boucle pour extraire les informations de chaque bourse
#     for bourse in bourses:
#         try:
#             # Extraire le titre de la bourse
#             titre = bourse.find_element(By.TAG_NAME, "h4").text
    
#             if titre not in titres_set:  # Vérifier si le titre est déjà extrait
#                 titres_set.add(titre)
    
#                 # Trouver toutes les balises <p> dans chaque section de bourse
#                 p_tags = bourse.find_elements(By.TAG_NAME, "p")
    
#                 if len(p_tags) > 0:
#                     # Trouver toutes les balises <strong> dans la première balise <p>
#                     strong_tags = p_tags[0].find_elements(By.TAG_NAME, "strong")
    
#                     # Vérifier si strong_tags contient suffisamment d'éléments
#                     if len(strong_tags) > 0:
#                         # Récupérer le nombre de bourses
#                         nombre_bourse = strong_tags[0].text.strip()  # Extraire et nettoyer le texte de la balise <strong>
    
#                         # Vérifier si le texte est vide
#                         if nombre_bourse == "":
#                             no_bourses.append("Non spécifié")
#                         else:
#                             no_bourses.append(nombre_bourse)
    
#                     # Date limite (3ème <strong>)
#                     if len(strong_tags) >= 3:
#                         date_limite = strong_tags[2].text
#                     else:
#                         date_limite = "Date limite non trouvée"
    
#                     # Pays (4ème et dernière <strong>)
#                     if len(strong_tags) >= 4:
#                         pays_val = strong_tags[3].text
#                     else:
#                         pays_val = "Pays non trouvé"
#                 else:
#                     date_limite = "Date limite non trouvée"
#                     pays_val = "Pays non trouvé"
    
#                 # Description à partir de la deuxième balise <p>
#                 if len(p_tags) > 1:
#                     description = p_tags[1].text
#                 else:
#                     description = "Description non trouvée"
    
#                 # Trouver toutes les balises <a> après la dernière balise <p>
#                 a_tags = bourse.find_elements(By.TAG_NAME, "a")
    
#                 # Prendre seulement le premier lien
#                 if a_tags:
#                     premier_lien = a_tags[0].get_attribute('href')
#                     premier_liens.append(premier_lien)
#                 else:
#                     premier_lien = "Lien non trouvé"
    
#                 # Extraire tous les liens
#                 liens = [a_tag.get_attribute('href') for a_tag in a_tags]
    
#                 # Ajouter la liste de liens sans concaténation
#                 if liens:
#                     liens_combines_ = liens  # On garde simplement la liste des liens
#                 else:
#                     liens_combines_ = ["Lien non trouvé"]
    
#                 # Vérifier si les informations sont valides avant de les ajouter
#                 if titre != "BURKINA FASO" and date_limite != "Date limite non trouvée" and pays_val != "Pays non trouvé" and description != "Description non trouvée":
#                     titres.append(titre)
#                     dates_limite.append(date_limite)
#                     pays.append(pays_val)
#                     descriptionss.append(description)
#                     liens_combines.append(liens_combines_)
    
#         except Exception as e:
#             # Gérer les exceptions en cas d'erreur lors de l'extraction des informations
#             print(f"Erreur lors de l'extraction d'une bourse: {str(e)}")
    
#     # Fermer le navigateur une fois le scraping terminé
#     driver.quit()
    
#     # Créer un DataFrame avec les informations extraites
#     df_bourses_campusfaso = pd.DataFrame({
#         'Pays': pays,
#         'Titre': titres,
#         "Type" : "Bourse",
#         'Description': descriptionss,
#         'Niveau':titres,
#         'Financement':premier_liens,
#         'Date Limite': dates_limite,
#         'Conditions': liens_combines,
#         "Nombre de bourses": no_bourses,
#         "Domaine Conserné": premier_liens,
#         "Durée d'étude": premier_liens,
#         "Pays éligibles": premier_liens
#     })
    

#     # Créer un DataFrame avec les informations extraites
#     return df_bourses_campusfaso
    
#     # Sauvegarder le DataFrame dans un fichier CSV
#     #df_bourses_campusfaso.to_csv(output_file, index=False)


# #scraper_bourses_campusfaso()


# bourses_campusfaso.py

from scrapping.utils import setup_scraping_environment, configure_chrome, load_env_variables

# Charger les variables d'environnement
username, password = load_env_variables()

# Configurer l'environnement de scraping
pd, time, webdriver, By, Service, Options, BeautifulSoup = setup_scraping_environment()

def scraper_bourses_campusfaso():
    # Configurer et lancer le navigateur
    driver = configure_chrome()
    
    # URL des pages à ouvrir
    url_bourses = 'https://www.campusfaso.bf/formations/bourses'  # URL de la page des bourses
    url_connexion = "https://www.campusfaso.bf/candidat/acceder-compte"  # URL de la page de connexion
    
    # Ouvrir la page de connexion
    driver.get(url_connexion)
    
    # Trouver les champs de connexion
    username_input = driver.find_element(By.ID, "login")  # Champ pour l'identifiant
    password_input = driver.find_element(By.ID, "mdp")  # Champ pour le mot de passe
    
    # Saisir les identifiants pour se connecter
    username_input.send_keys(username)  # Utiliser le nom d'utilisateur chargé depuis .env
    password_input.send_keys(password)  # Utiliser le mot de passe chargé depuis .env
    
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
    
    # Assurez-vous que toutes les colonnes ont la même longueur
    df_bourses_campusfaso = df_bourses_campusfaso.reset_index(drop=True)
    
    return df_bourses_campusfaso
