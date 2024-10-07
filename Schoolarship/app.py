


import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from users.users_authentification import auth_blueprint, create_users_table
from databases.db import get_all_bourses, get_bourse_by_id  # Importer la fonction qui récupère les données de la base
from utils.utils import install_python_dependencies, install_chrome_and_chromedriver
import datetime
load_dotenv()  # Charge les variables d'environnement à partir du fichier .env
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # Charge la clé secrète depuis .env

create_users_table()
# Enregistrer le blueprint pour l'authentification
app.register_blueprint(auth_blueprint)

def get_paginated_opportunities(opportunities, page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    return opportunities[start:end]

@app.route('/', methods=['GET'])
def opportunites():
    message = request.args.get('message', None)
    is_error = request.args.get('is_error', False)
    search_term = request.args.get('search', '')
    opportunities = get_all_bourses(search_term)
    # Obtenez le numéro de page à partir des paramètres de la requête, avec 1 comme valeur par défaut
    page = request.args.get('page', 1, type=int)
    per_page = 6

    # Obtenez les bourses paginées
    paginated_bourses = get_paginated_opportunities(opportunities['toutes_les_bourses'], page, per_page)

    # Vérifiez si les résultats de recherche sont vides
    messages = None
    if not paginated_bourses:  # Si la liste est vide
        messages = "Aucun résultat trouvé"

    return render_template(
        'index.html',
        opportunities=paginated_bourses,
        page=page, 
        per_page=per_page,  # Assurez-vous que cette ligne est ajoutée
        total=len(opportunities['toutes_les_bourses']),
        message=message,
        messages=messages, 
        is_error=is_error)
#######

@app.route('/bourses', methods=['GET'])
def bourses():
    
    search_term = request.args.get('search', '')
    opportunities = get_all_bourses(search_term)
    # Obtenez le numéro de page à partir des paramètres de la requête, avec 1 comme valeur par défaut
    page = request.args.get('page', 1, type=int)
    per_page = 6

    # Obtenez les bourses paginées
    paginated_bourses = get_paginated_opportunities(opportunities['bourses'], page, per_page)

# Vérifiez si les résultats de recherche sont vides
    messages = None
    if not paginated_bourses:  # Si la liste est vide
        messages = "Aucun résultat trouvé"

    return render_template(
        'bourses.html',
        opportunities=paginated_bourses,
        page=page, 
        per_page=per_page,  # Assurez-vous que cette ligne est ajoutée
        total=len(opportunities['bourses']),
        messages=messages
        )

@app.route('/stages', methods=['GET'])
def stages():
    
    search_term = request.args.get('search', '')
    opportunities = get_all_bourses(search_term)
    # Obtenez le numéro de page à partir des paramètres de la requête, avec 1 comme valeur par défaut
    page = request.args.get('page', 1, type=int)
    per_page = 6

    # Obtenez les bourses paginées
    paginated_bourses = get_paginated_opportunities(opportunities['stages'], page, per_page)

    # Vérifiez si les résultats de recherche sont vides
    messages = None
    if not paginated_bourses:  # Si la liste est vide
        messages = "Aucun résultat trouvé"

    return render_template(
        'stages.html',
        opportunities=paginated_bourses,
        page=page, 
        per_page=per_page,  # Assurez-vous que cette ligne est ajoutée
        total=len(opportunities['stages']),
        messages=messages
        )

@app.route('/formations', methods=['GET'])
def formations():
    
    search_term = request.args.get('search', '')
    opportunities = get_all_bourses(search_term)
    # Obtenez le numéro de page à partir des paramètres de la requête, avec 1 comme valeur par défaut
    page = request.args.get('page', 1, type=int)
    per_page = 6

    # Obtenez les bourses paginées
    paginated_bourses = get_paginated_opportunities(opportunities['formations'], page, per_page)

    # Vérifiez si les résultats de recherche sont vides
    messages = None
    if not paginated_bourses:  # Si la liste est vide
        messages = "Aucun résultat trouvé"

    return render_template(
        'formations.html',
        opportunities=paginated_bourses,
        page=page, 
        per_page=per_page,  # Assurez-vous que cette ligne est ajoutée
        total=len(opportunities['formations']),
        messages=messages
        )

###################

# @app.route('/', methods=['GET'])
# def opportunites():
#     message = request.args.get('message', None)
#     is_error = request.args.get('is_error', False)
#     search_term = request.args.get('search', '')
#     opportunities = get_all_bourses(search_term, rubrique='opportunites')
#     # Obtenez le numéro de page à partir des paramètres de la requête, avec 1 comme valeur par défaut
#     page = request.args.get('page', 1, type=int)
#     per_page = 6

#     # Obtenez les bourses paginées
#     paginated_bourses = get_paginated_opportunities(opportunities['toutes_les_bourses'], page, per_page)

#     return render_template(
#         'index.html',
#         opportunities=paginated_bourses,
#         page=page, 
#         per_page=per_page, 
#         total=len(opportunities['toutes_les_bourses']),
#         message=message, 
#         is_error=is_error
#     )



# @app.route('/bourses', methods=['GET'])
# def bourses():
#     search_term = request.args.get('search', '')
#     opportunities = get_all_bourses(search_term, rubrique='bourses')
#     page = request.args.get('page', 1, type=int)
#     per_page = 6

#     paginated_bourses = get_paginated_opportunities(opportunities['bourses'], page, per_page)

#     return render_template(
#         'bourses.html',
#         opportunities=paginated_bourses,
#         page=page, 
#         per_page=per_page,  
#         total=len(opportunities['bourses']),
#     )

# @app.route('/stages', methods=['GET'])
# def stages():
#     search_term = request.args.get('search', '')
#     opportunities = get_all_bourses(search_term, rubrique='stages')
#     page = request.args.get('page', 1, type=int)
#     per_page = 6

#     paginated_bourses = get_paginated_opportunities(opportunities['stages'], page, per_page)

#     return render_template(
#         'stages.html',
#         opportunities=paginated_bourses,
#         page=page, 
#         per_page=per_page,  
#         total=len(opportunities['stages']),
#     )


#############################

# @app.route('/', methods=['GET'])
# def opportunites():
#     message = request.args.get('message', None)
#     is_error = request.args.get('is_error', False)
#     search_term = request.args.get('search', '')
#     opportunities = get_all_bourses(search_term)  # Ne pas passer de type

#     # Obtenez le numéro de page à partir des paramètres de la requête, avec 1 comme valeur par défaut
#     page = request.args.get('page', 1, type=int)
#     per_page = 6

#     # Obtenez les bourses paginées
#     paginated_bourses = get_paginated_opportunities(opportunities['toutes_les_bourses'], page, per_page)

#     return render_template(
#         'index.html',
#         opportunities=paginated_bourses,
#         page=page, 
#         per_page=per_page,
#         total=len(opportunities['toutes_les_bourses']),
#         message=message, 
#         is_error=is_error)


# @app.route('/bourses', methods=['GET'])
# def bourses():
#     search_term = request.args.get('search', '')
#     opportunities = get_all_bourses(search_term, type='Bourse')  # Passer 'Bourse' comme type

#     # Obtenez le numéro de page
#     page = request.args.get('page', 1, type=int)
#     per_page = 6

#     # Obtenez les bourses paginées
#     paginated_bourses = get_paginated_opportunities(opportunities['bourses'], page, per_page)

#     return render_template(
#         'bourses.html',
#         opportunities=paginated_bourses,
#         page=page, 
#         per_page=per_page,
#         total=len(opportunities['bourses']),
#     )


# @app.route('/stages', methods=['GET'])
# def stages():
#     search_term = request.args.get('search', '')
#     opportunities = get_all_bourses(search_term, type='Stage')  # Passer 'Stage' comme type

#     # Obtenez le numéro de page
#     page = request.args.get('page', 1, type=int)
#     per_page = 6

#     # Obtenez les bourses paginées
#     paginated_bourses = get_paginated_opportunities(opportunities['stages'], page, per_page)

#     return render_template(
#         'stages.html',
#         opportunities=paginated_bourses,
#         page=page, 
#         per_page=per_page,
#         total=len(opportunities['stages']),
#     )


@app.route('/details/<int:bourse_id>', methods=['GET'])
def details(bourse_id):
    bourse = get_bourse_by_id(bourse_id)  # Récupère la bourse avec l'ID donné
    section = request.args.get('section', 'opportunites')  # Récupère la section ou par défaut 'opportunites'

    if bourse:
        return render_template('detail.html', bourse=bourse, section=section)  # Remplace 'detail.html' par ton template
    else:
        return "Bourse non trouvée", 404
    
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.datetime.now().year}
    


@app.route('/about/')
def about():
    return render_template("about.html")

if __name__ == '__main__':
    install_chrome_and_chromedriver()
    app.run(debug=True, ssl_context=None)

