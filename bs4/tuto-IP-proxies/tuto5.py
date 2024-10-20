"""
Advanced Introduction to WebScraping: Efficient Proxy Rotation
Author: sarrabenyahia (modified)
Description: This script demonstrates an advanced approach to using proxy servers for web scraping. 
It includes the following key features:

1. Fetching a large pool of proxies (500) from a public API.
2. Implementing concurrent proxy checking to efficiently identify working proxies.
3. Using a ThreadPoolExecutor for parallel execution, significantly speeding up the proxy verification process.
4. Implementing a robust error handling system to manage proxy-related issues.
5. Utilizing a rotating proxy system for making requests, helping to avoid IP-based blocking and distribute requests.

This script is designed to handle common issues with free proxies, such as unavailability and slow response times. 
It's particularly useful for large-scale web scraping projects where maintaining anonymity and bypassing rate limits 
are crucial. The script demonstrates advanced concepts in Python such as concurrent programming, error handling, 
and efficient resource management in the context of web scraping.
"""

import requests
from bs4 import BeautifulSoup
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_proxies():
    url = "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&filterUpTime=90"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return [f"{proxy['ip']}:{proxy['port']}" for proxy in data['data']]
    except Exception as e:
        print(f"Erreur lors de la récupération des proxies : {e}")
        return []

def check_proxy(proxy, timeout=5):
    try:
        response = requests.get('http://httpbin.org/ip', 
                                proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'}, 
                                timeout=timeout)
        if response.status_code == 200:
            print(f"Proxy {proxy} fonctionne")
            return proxy
    except:
        pass
    return None

def get_working_proxies(all_proxies, max_workers=10, timeout=5):
    working_proxies = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_proxy = {executor.submit(check_proxy, proxy, timeout): proxy for proxy in all_proxies}
        for future in as_completed(future_to_proxy):
            if future.result():
                working_proxies.append(future.result())
    return working_proxies

def scrape_with_rotating_proxies(url, proxies, max_retries=5, timeout=10):
    for _ in range(max_retries):
        if not proxies:
            print("Aucun proxy fonctionnel disponible")
            return None
        
        proxy = random.choice(proxies)
        print(f"Tentative avec le proxy : {proxy}")
        
        try:
            response = requests.get(url, 
                                    proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'}, 
                                    timeout=timeout)
            if response.status_code == 200:
                return response.text
        except requests.RequestException as e:
            print(f"Erreur avec le proxy {proxy}: {e}")
            proxies.remove(proxy)
        
        time.sleep(1)
    
    print("Toutes les tentatives de proxy ont échoué")
    return None

def main():
    all_proxies = fetch_proxies()
    print(f"Récupération de {len(all_proxies)} proxies. Vérification de leur validité...")
    
    working_proxies = get_working_proxies(all_proxies, timeout=3)
    print(f"Trouvé {len(working_proxies)} proxies fonctionnels")
    
    if not working_proxies:
        print("Aucun proxy fonctionnel trouvé. Fin du programme.")
        return
    
    target_url = "http://httpbin.org/ip"
    
    for _ in range(5):
        content = scrape_with_rotating_proxies(target_url, working_proxies)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            print(f"Requête réussie. IP utilisée : {soup.text}")
        else:
            print("Échec de la récupération du contenu")
        
        time.sleep(2)

if __name__ == "__main__":
    main()