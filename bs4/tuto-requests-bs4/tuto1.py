"""
Introduction to WebScraping : Request & BeautifulSoup
Author: sarrabenyahia
Description: This script demonstrates how to scrape data from a book website 
using the Requests library and BeautifulSoup for HTML parsing. It extracts 
the title, price, and other relevant data about the books listed on the website.
"""

import requests
import pdb
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"


def get_text_if_exist(e):
    if e:
        return e.text.strip()
    return None


# -------------------- Python Debbuging
# pdb.set_trace()
# -------------------------------------

response = requests.get(url)
response.encoding = response.apparent_encoding

# -------------------- GET HEADER AND USER_AGENT OF THE REQUEST
# print(response.header)
# print(response.user_agent)
# user_agent = response.request.headers['User-Agent']
# print(f"User-Agent: {user_agent}")
# -------------------------------------------------------------

if response.status_code == 200:
    html = response.text
    # print(html)
    f = open("response.html", "w")
    f.write(html)
    f.close()

    soup = BeautifulSoup(html, "lxml")

    # Find all the titles of the books
    titre = soup.find("a").text
    print(titre)

    # Find all the prices of the books
    price = get_text_if_exist(soup.find("p", class_="price_color"))
    print(price)

    # --------- NON-ROBUST WAY TO CHECK EXISTENCE OF ELEMENT, SEE FUNCTION
    # e_price = soup.find("p", class_="price_color")
    # if e_price:
    #     price = e_price.text
    #     print(price)
    # -------------------------------------------------------------

    # First way to find the prices, searching in all the HTML file:
    prices = soup.find_all("p", class_="price_color")
    for price in prices:
        pass
        # print(price.text)

    # Second way to find the prices, searching in each book "cards":
    cards = soup.find_all("div", class_="product_price")
    for card in cards:
        prices = card.find("p").text
        print(prices)

    
    # Find all the article elements with class 'product_pod'
    titles = soup.find_all("h3")
    for title in titles:
        title.find("a").get("title")

    # ------------------------- EXERCICE CORRECTION : FIND ALL TITLES OF BOOKS
    # Using find_all() to get all book articles
    book_articles = soup.find_all("article", class_="product_pod")

    for article in book_articles:
        # Using find() to get the title element within each article
        title_element = article.find("h3").find("a")
        title = title_element.get("title")
        print(title)
# -------------------------------------------------------------

else:
    print("Error:", response.status_code)

print("FIN")
