# import importlib
# import subprocess
# import sys
# import os
# import pip


# #import subprocess
# import shutil

# '''def install_if_needed(module_name, package_name=None):
#     """Vérifie et installe un module Python si nécessaire."""
#     if package_name is None:
#         package_name = module_name
#     try:
#         importlib.import_module(module_name)
#         print(f"{package_name} est déjà installé.")
#     except ImportError:
#         print(f"{package_name} n'est pas installé. Installation en cours...")
#         subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
#         print(f"{package_name} a été installé avec succès.")
# '''


# def install_python_dependencies():
#     """Installe les dépendances Python listées dans requirements.txt, en évitant les réinstallations."""

#     # Récupérer la liste des paquets déjà installés
#     installed_packages = [package.project_name for package in pip.get_installed_distributions()]

#     # Lire le fichier requirements.txt
#     with open("requirements.txt", "r") as f:
#         requirements = f.read().splitlines()

#     # Filtrer les packages à installer
#     packages_to_install = [package for package in requirements if package not in installed_packages]

#     if packages_to_install:
#         subprocess.check_call([sys.executable, "-m", "pip", "install", *packages_to_install])
#         print("Les packages suivants ont été installés :", ", ".join(packages_to_install))
#     else:
#         print("Tous les packages requis sont déjà installés.")



# def install_chrome_and_chromedriver():
#     versions = {}
    
#     # Vérifier si Google Chrome est déjà installé
#     if shutil.which("google-chrome") is None:
#         print("Installation de Google Chrome...")
#         subprocess.run(['apt-get', 'update'], check=True)
#         subprocess.run(['apt-get', 'install', '-y', 'wget', 'unzip'], check=True)
#         subprocess.run(['wget', 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'], check=True)
#         subprocess.run(['dpkg', '-i', 'google-chrome-stable_current_amd64.deb'], check=True)
#         subprocess.run(['apt-get', '-f', 'install', '-y'], check=True)
#     else:
#         print("Google Chrome est déjà installé.")
    
#     # Vérifier si ChromeDriver est déjà installé
#     if shutil.which("chromedriver") is None:
#         print("Installation de ChromeDriver...")
#         subprocess.run(['wget', 'https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/128.0.6613.119/linux64/chromedriver-linux64.zip'], check=True)
#         subprocess.run(['unzip', 'chromedriver-linux64.zip'], check=True)
#         subprocess.run(['mv', 'chromedriver-linux64/chromedriver', '/usr/local/bin/'], check=True)
#         subprocess.run(['chmod', '+x', '/usr/local/bin/chromedriver'], check=True)
#     else:
#         print("ChromeDriver est déjà installé.")
    
#     # Vérification des versions installées
#     versions['chrome_version'] = subprocess.getoutput('google-chrome --version')
#     versions['chromedriver_version'] = subprocess.getoutput('chromedriver --version')
    
#     return versions



# '''def install_chrome_and_chromedriver():
#     """Installe Google Chrome et ChromeDriver si nécessaire."""
#     # Vérifier et installer Google Chrome
#     try:
#         subprocess.check_call(['google-chrome', '--version'])
#         print("Google Chrome est déjà installé.")
#     except FileNotFoundError:
#         print("Installation de Google Chrome...")
#         subprocess.check_call(['apt-get', 'update'])
#         subprocess.check_call(['apt-get', 'install', '-y', 'wget', 'unzip'])
#         subprocess.check_call(['wget', 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'])
#         subprocess.check_call(['dpkg', '-i', 'google-chrome-stable_current_amd64.deb'])
#         subprocess.check_call(['apt-get', '-f', 'install', '-y'])
#         print("Google Chrome a été installé avec succès.")

#     # Vérifier et installer ChromeDriver
#     try:
#         subprocess.check_call(['chromedriver', '--version'])
#         print("ChromeDriver est déjà installé.")
#     except FileNotFoundError:
#         print("Installation de ChromeDriver...")
#         subprocess.check_call(['wget', 'https://chromedriver.storage.googleapis.com/128.0.6613.119/chromedriver_linux64.zip'])
#         subprocess.check_call(['unzip', 'chromedriver_linux64.zip'])
#         subprocess.check_call(['mv', 'chromedriver', '/usr/local/bin/'])
#         subprocess.check_call(['chmod', '+x', '/usr/local/bin/chromedriver'])
#         print("ChromeDriver a été installé avec succès.")'''

# ################


import json
import os
import shutil
import subprocess
from webdriver_manager.chrome import ChromeDriverManager  # Import the class

###########

def install_python_dependencies():
    """Installe les dépendances Python listées dans requirements.txt, en évitant les réinstallations."""
    
    installed_packages = [package.project_name for package in pip.get_installed_distributions()]

    with open("requirements.txt", "r") as f:
        requirements = f.read().splitlines()

    packages_to_install = [package for package in requirements if package not in installed_packages]

    if packages_to_install:
        subprocess.check_call([sys.executable, "-m", "pip", "install", *packages_to_install])
        print("Les packages suivants ont été installés :", ", ".join(packages_to_install))
    else:
        print("Tous les packages requis sont déjà installés.")


###############

def load_config():
    """Charge le fichier de configuration JSON."""
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            return json.load(f)
    return {"chrome_installed": False, "chromedriver_installed": False}

def save_config(config):
    """Sauvegarde l'état d'installation dans le fichier de configuration JSON."""
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

def install_chrome_and_chromedriver():
    config = load_config()
    versions = {}

    # Vérifier si Google Chrome est déjà installé ou noté comme installé dans le fichier config.json
    if not config.get("chrome_installed", False):
        if shutil.which("google-chrome") is None:
            print("Installation de Google Chrome...")
            subprocess.run(['apt-get', 'update'], check=True)
            subprocess.run(['apt-get', 'install', '-y', 'wget', 'unzip'], check=True)
            subprocess.run(['wget', 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'], check=True)
            subprocess.run(['dpkg', '-i', 'google-chrome-stable_current_amd64.deb'], check=True)
            subprocess.run(['apt-get', '-f', 'install', '-y'], check=True)
        config["chrome_installed"] = True
        save_config(config)
    else:
        print("Google Chrome est déjà installé.")

    # Vérifier si ChromeDriver est déjà installé ou noté comme installé dans le fichier config.json
    if not config.get("chromedriver_installed", False):
        if shutil.which("chromedriver") is None:
            print("Installation de ChromeDriver...")
            subprocess.run(['wget', 'https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/128.0.6613.119/linux64/chromedriver-linux64.zip'], check=True)
            subprocess.run(['unzip', 'chromedriver-linux64.zip'], check=True)
            subprocess.run(['mv', 'chromedriver-linux64/chromedriver', '/usr/local/bin/'], check=True)
            subprocess.run(['chmod', '+x', '/usr/local/bin/chromedriver'], check=True)
        config["chromedriver_installed"] = True
        save_config(config)
    else:
        print("ChromeDriver est déjà installé.")

    # Vérification des versions installées
    versions['chrome_version'] = subprocess.getoutput('google-chrome --version')
    versions['chromedriver_version'] = subprocess.getoutput('chromedriver --version')

    return versions
