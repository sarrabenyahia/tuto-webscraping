from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import json
from datetime import datetime
import pandas as pd

class WebScraper:
    def __init__(self):
        # Configuration du navigateur avec des options
        self.options = webdriver.ChromeOptions()
        #self.options.add_argument('--headless')  # Mode sans interface graphique
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        
        # Initialisation du driver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.options
        )
        self.wait = WebDriverWait(self.driver, 10)

    def get_page_info(self, url):
        """Récupère les informations générales de la page"""
        try:
            self.driver.get(url)
            return {
                "titre": self.driver.title,
                "url": self.driver.current_url,
                "date_extraction": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "cookies": len(self.driver.get_cookies()),
                "taille_page": len(self.driver.page_source)
            }
        except Exception as e:
            return {"erreur": str(e)}

    def extract_links(self):
        """Extrait tous les liens de la page avec leur texte"""
        links = self.driver.find_elements(By.TAG_NAME, "a")
        return [{
            "texte": link.text.strip(),
            "href": link.get_attribute("href"),
            "title": link.get_attribute("title")
        } for link in links if link.text.strip()]

    def extract_images(self):
        """Extrait les informations sur les images"""
        images = self.driver.find_elements(By.TAG_NAME, "img")
        return [{
            "src": img.get_attribute("src"),
            "alt": img.get_attribute("alt"),
            "width": img.get_attribute("width"),
            "height": img.get_attribute("height")
        } for img in images]

    def extract_text_content(self):
        """Extrait le contenu textuel principal"""
        try:
            # Attendre que le contenu principal soit chargé
            main_content = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "main"))
            )
            paragraphs = main_content.find_elements(By.TAG_NAME, "p")
            return [p.text for p in paragraphs if p.text.strip()]
        except TimeoutException:
            # Si pas de balise main, on prend tous les paragraphes
            paragraphs = self.driver.find_elements(By.TAG_NAME, "p")
            return [p.text for p in paragraphs if p.text.strip()]

    def extract_metadata(self):
        """Extrait les métadonnées de la page"""
        meta_tags = self.driver.find_elements(By.TAG_NAME, "meta")
        return [{
            "name": meta.get_attribute("name"),
            "content": meta.get_attribute("content"),
            "property": meta.get_attribute("property")
        } for meta in meta_tags if meta.get_attribute("content")]

    def scrape_page(self, url):
        """Fonction principale qui orchestre le scraping"""
        try:
            # Collecter toutes les informations
            data = {
                "info_page": self.get_page_info(url),
                "liens": self.extract_links(),
                "images": self.extract_images(),
                "contenu_textuel": self.extract_text_content(),
                "metadata": self.extract_metadata()
            }

            # Sauvegarder en JSON
            with open('resultats_scraping.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            # Créer un DataFrame avec les liens
            df_links = pd.DataFrame(data['liens'])
            df_links.to_csv('liens_extraits.csv', index=False)

            return data

        except Exception as e:
            print(f"Erreur lors du scraping: {str(e)}")
            return None

        finally:
            self.driver.quit()

def main():
    # URL à scraper (exemple avec le site Python.org)
    url = "https://www.python.org"
    
    # Initialiser et exécuter le scraper
    scraper = WebScraper()
    resultats = scraper.scrape_page(url)
    
    if resultats:
        print("\n=== Résumé du Scraping ===")
        print(f"Titre de la page: {resultats['info_page']['titre']}")
        print(f"Nombre de liens trouvés: {len(resultats['liens'])}")
        print(f"Nombre d'images trouvées: {len(resultats['images'])}")
        print(f"Paragraphes extraits: {len(resultats['contenu_textuel'])}")
        print("\nLes résultats complets ont été sauvegardés dans 'resultats_scraping.json'")
        print("Les liens ont été exportés dans 'liens_extraits.csv'")

if __name__ == "__main__":
    main()