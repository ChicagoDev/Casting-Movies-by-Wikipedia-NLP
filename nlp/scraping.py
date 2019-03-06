"""
    Functions that assist scraping wikipedia biography pages
"""
import re
from bs4 import BeautifulSoup


def clean(text):
    """
        Cleans Wikipedia Text with Regexes
    :param text:
    :return: text:
    """
    doc = ''.join(text).lower()
    doc = re.sub(r'[<>\{}/;|\[\]-]', ' ', doc)
    doc = re.sub(r'[0-9]', ' ', doc)
    doc = re.sub(r'\'', ' ', doc)
    doc = re.sub(r'=', ' ', doc)
    doc = re.sub(r':', ' ', doc)
    doc = re.sub(r'"', ' ', doc)
    doc = re.sub(r'\s+', ' ', doc)
    doc = re.sub(r'\(', ' ', doc)
    doc = re.sub(r'\)', ' ', doc)
    doc = re.sub(r'\s{2,}', ' ', doc)

    return doc


def extract_wikipedia_body(response):
    """
    From a Wikipedia Page, Retrieve the body-text. (All text until references)
    :param response: Wikipedia Page
    :return: text: body text
    """
    page_txts = []

    soup = BeautifulSoup(response.text, 'html.parser')

    body = soup.find('div', id='mw-content-text').find('div')

    found_reference_tag = False

    for child in body.children:
        if not is_reference_heading(child):
            if type(child) is bs4.element.Tag:
                page_txts.append(child.get_text())
        else:
            # print(f'BROKE')
            break

    return ' '.join(page_txts)


def is_reference_heading(tag):
    """
    Function for Beautiful Soup specifically.
    Used to determine if the DOM element is the reference area
    :param tag:
    :return: boolean:
    """
    span = None

    if tag.name == 'h2':

        try:
            span = tag.contents[0]

        except:
            # Nothing found in tag, just return False
            return False

        if span.name == 'span':

            if span['id'] == 'References':
                return True

    return False
