
import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy import create_engine
import psycopg2


from scrapping.bourses_campusfaso import scraper_bourses_campusfaso

from scrapping.bourses_greatyop import get_total_pages, generate_page_urls,extract_links_from_pages, extract_bourse_info_from_urls


def scrape_and_store_data():
    try:
       

        # Scraping des données
        df_bourses_campusfaso = scraper_bourses_campusfaso()
        
        url_bourses = 'https://greatyop.com/category/bourses/'
        total_pages_bourses = get_total_pages(url_bourses)
        
        url_stages = 'https://greatyop.com/category/stages-emplois/'
        total_pages_stages = get_total_pages(url_stages)
        
        url_formations = 'https://greatyop.com/category/formations/'
        total_pages_formations = get_total_pages(url_formations)
        
        urls_pages_bourses = generate_page_urls(url_bourses, total_pages_bourses)
        urls_pages_stages = generate_page_urls(url_stages, total_pages_stages)
        urls_pages_formations = generate_page_urls(url_formations, total_pages_formations)
        
        liens_bourses = extract_links_from_pages(urls_pages_bourses)
        liens_stages = extract_links_from_pages(urls_pages_stages)
        liens_formations = extract_links_from_pages(urls_pages_formations)
        
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
        
        # Concaténer tous les DataFrames
        df = pd.concat([df_bourses_campusfaso, df_bourses, df_stages, df_formations], ignore_index=True)
        
        return df.to_csv("opportunities_etudes.csv")
        
        print("Scraping terminé, données nettoyées et stockées dans PostgreSQL.")
    
    except Exception as e:
        print(f"Erreur lors du processus: {str(e)}")

# Appeler la fonction pour exécuter le processus complet
#scrape_and_store_data()
