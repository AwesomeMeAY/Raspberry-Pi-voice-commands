#!/bin/python
import requests as Requests
from bs4 import BeautifulSoup as Soup
from time import sleep

# In wikipedia some of the html paragraphs are empty
# So I need to find the first none empty one
def find_first_paragraph(lst):
    for paragraph in lst:
        if str(paragraph) == '<p class="mw-empty-elt">\n</p>':
            continue
        return paragraph.get_text()

def wikipedia_search(article):
    article = article.replace(" ", "_")
    request = Requests.get(f'https://en.wikipedia.org/wiki/{article}')
    print(request.status_code)
    parser = Soup(request.text, 'html.parser')
    return find_first_paragraph(parser.find_all('p'))

if __name__ == '__main__':
    from sys import argv

    print(find_first_paragraph(wikipeadia_search(argv[1])))
    print("What you said", argv[1])
    print("succsess")
