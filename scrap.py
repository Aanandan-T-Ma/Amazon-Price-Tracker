import requests
from bs4 import BeautifulSoup

def getDetails(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
    }
    results = requests.get(url, headers = headers)
    soup = BeautifulSoup(results.content, 'lxml')
    name = soup.find('span', { 'id': 'productTitle' }).get_text().strip()
    price = float((soup.find('span', { 'id': 'priceblock_dealprice' }) or soup.find('span', { 'id': 'priceblock_ourprice' })).get_text()[2:].replace(',', ''))
    return [name, price]

""" url = 'https://www.amazon.in/LG-Convertible-Anti-Virus-protection-MS-Q18YNZA/dp/B08R918D6Y/ref=lp_22940538031_1_1'
#url = 'https://www.amazon.in/Boult-Audio-BassBuds-Earphones-Cancellation/dp/B08JVGLP2D/ref=sr_1_2_sspa?dchild=1&keywords=earphones&qid=1617527280&sr=8-2-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzREg4VjdYWVMyWUpJJmVuY3J5cHRlZElkPUEwNzE1MTIwM0JNMkpZVUxDMVpBRSZlbmNyeXB0ZWRBZElkPUEwOTc2MTY1QzQ1N1VHU1VTRllFJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=='

details = getDetails(url)
print(details) """