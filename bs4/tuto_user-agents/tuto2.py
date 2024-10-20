"""
Introduction to WebScraping : User-Agents
Author: sarrabenyahia
Description: This script demonstrates how to send requests to websites using custom User-Agent headers. 
In this example, the script attempts to access the IMDB website, which disallows crawlers, and shows how 
to handle requests by using a modified User-Agent to simulate a real browser.
"""

import requests
from bs4 import BeautifulSoup

# IMDB doesn't allow crawlers, see in robots.txt file : https://www.imdb.com/robots.txt
url = "https://www.imdb.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=HEADERS)
print(
    response.request.headers
)  # Response of the request, don't confuse with response.headers that are the headers of the response.

if response.status_code == 200:
    html = response.text
    f = open("response.html", "w")
    f.write(html)
    f.close()
else:
    print("Error:", response.status_code)
