"""
Introduction to Web Scraping: IMDB User-Agent Randomization
Author: sarrabenyahia
Description: This script demonstrates how to scrape data from the IMDB website by using 
randomly selected User-Agent headers to avoid being blocked. It retrieves the page content 
and checks the response status.
"""

import requests
import random
from bs4 import BeautifulSoup

# IMDB doesn't allow crawlers, see in robots.txt file: https://www.imdb.com/robots.txt
url = "https://www.imdb.com"

# List of user-agents, retrieved from https://www.useragentlist.net/.
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
]


def get_random_user_agent():
    return random.choice(USER_AGENTS)


# Prepare headers with a randomly selected user-agent
HEADERS = {"User-Agent": get_random_user_agent()}

response = requests.get(url, headers=HEADERS)

# Print the request headers to confirm the selected user-agent
print(f"Used User-Agent: {response.request.headers['User-Agent']}")

if response.status_code == 200:
    print("Success!")
else:
    print("Error:", response.status_code)
