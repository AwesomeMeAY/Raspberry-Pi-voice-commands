#!/bin/python
import requests as Requests
from sys import argv
from bs4 import BeautifulSoup as Soup

def wikipeadia_search(article):
    article = article.replace(" ", "_")
    request = Requests.get(f'https://en.wikipedia.org/wiki/{article}')
    print(request.status_code)
    parser = Soup(request.text, 'html.parser')
    print(parser.find_all('p')[1].get_text())

wikipeadia_search(argv[1])
print("What you said", argv[1])
print("succsess")
