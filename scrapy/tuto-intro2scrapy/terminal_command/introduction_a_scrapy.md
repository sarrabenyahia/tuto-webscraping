# Introduction à Scrapy

## Installation de Scrapy
1. **Créer un environnement virtuel** : 
   ```
   venv
   ```
2. **Installer Scrapy** : 
   ```
   pip install scrapy
   ```
3. **Tester l'installation** : 
   ```
   scrapy
   ```
   Si tout fonctionne, tu devrais voir "No active project".

## Créer un projet Scrapy
1. Créer un projet avec la commande : 
   ```
   scrapy startproject bookscraper
   ```
2. Cela génère plusieurs dossiers :
   - **spiders** (vide pour l'instant)
   - **items**, **middlewares**, **pipelines** (optionnels)
   - **settings** (important pour la configuration)

Nous allons les utiliser pour scraper plusieurs pages à la fois.

## Créer un spider
1. Utiliser la commande :
   ```
   scrapy genspider quotespider http://quotes.toscrape.com/
   ```
   Cela génère un spider nommé `quotespider` pour scraper ce site web.

## Utiliser iPython avec Scrapy
1. Installer iPython : 
   ```
   pip install ipython
   ```
2. Ajouter dans `scrapy.cfg` :
   ```
   shell = ipython
   ```
3. Lancer le shell dans le terminal : 
   ```
   scrapy shell
   ```

## Interagir avec une page web dans Scrapy Shell
1. **Récupérer le HTML d'une page** :
   ```
   fetch('http://quotes.toscrape.com/')
   ```
2. **Extraire les citations** :
   ```
   response.css('div.quote')
   ```
3. **Obtenir la première citation** :
   ```
   response.css('div.quote').get()
   ```

## Travailler avec les sélecteurs CSS et XPath
1. Mettre toutes les citations dans une variable : 
   ```
   quotes = response.css('div.quote')
   ```
2. **Longueur des citations** :
   ```
   len(quotes)
   ```
3. **Première citation** :
   ```
   quote = quotes[0]
   ```
4. Extraire des éléments spécifiques avec XPath :
   - **Texte de la première citation** : 
     ```
     quote.xpath('/html/body/div/div[2]/div[1]/div[1]/span[1]/text()').get()
     ```
   - **Auteur de la première citation** : 
     ```
     quote.xpath('/html/body/div/div[2]/div[1]/div[1]/span[2]/small/text()').get()
     ```
   - **Premier tag** : 
     ```
     quote.xpath('/html/body/div/div[2]/div[1]/div[1]/div/a[1]/text()').get()
     ```
   - **Lien vers l'auteur** : 
     ```
     quote.xpath('/html/body/div/div[2]/div[1]/div[1]/span[2]/a').attrib["href"]
     ```

## Pagination
1. Pour obtenir le lien vers la page suivante :
   ```
   response.css('li.next a ::attr(href)').get()
   ```