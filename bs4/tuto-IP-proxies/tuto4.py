"""
Introduction to WebScraping : Proxies
Author: sarrabenyahia
Description: This script demonstrates how to use proxy servers for web scraping. It fetches a list of 
proxy servers from a public API, then uses these proxies to make requests to a target website. 
The script rotates through different proxies to avoid IP-based blocking and to distribute requests 
across multiple IP addresses. It's a practical example of how to implement proxy rotation in 
web scraping projects, which can be useful for accessing geo-restricted content or bypassing 
rate limits.
"""

import requests
from bs4 import BeautifulSoup
import random
import time

def fetch_proxies():
    url = "https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc&filterUpTime=90"
    response = requests.get(url)
    data = response.json()
    return [f"{proxy['ip']}:{proxy['port']}" for proxy in data['data']]

def get_random_proxy(proxies):
    return random.choice(proxies)

def scrape_with_rotating_proxies(url, proxies, max_retries=5):
    for _ in range(max_retries):
        proxy = get_random_proxy(proxies)
        print(f"Trying proxy: {proxy}")
        
        try:
            response = requests.get(url, proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'}, timeout=10)
            if response.status_code == 200:
                return response.text
        except requests.RequestException as e:
            print(f"Error with proxy {proxy}: {e}")
        
        time.sleep(1)  # Be respectful, wait a bit before trying the next proxy
    
    print("All proxy attempts failed")
    return None

def main():
    proxies = fetch_proxies()
    target_url = "http://httpbin.org/ip"  # This will show us the IP being used
    
    for _ in range(5):  # Try 5 times to demonstrate rotation
        content = scrape_with_rotating_proxies(target_url, proxies)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            print(f"Successful request. IP used: {soup.text}")
        else:
            print("Failed to fetch content")
        
        time.sleep(2)  # Wait between requests

if __name__ == "__main__":
    main()