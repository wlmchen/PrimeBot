import requests
from discord.ext import commands
from bs4 import BeautifulSoup
import os
import re


def scrape_song_lyrics(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', class_='lyrics').get_text()
    # remove identifiers like chorus, verse, etc
    lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
    # remove empty lines
    lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])
    return lyrics


def scrape_arch_wiki(query):
    url = "https://wiki.archlinux.org/index.php?search={}".format(query)

    html_string = requests.get(url).content
    html_string = html_string.decode('utf-8')
    try:
        test1 = html_string[html_string.index("</ul></div>"):html_string.index("Contents")]
    except ValueError:
        raise commands.CommandError("Page not found!")
        return
    soup = BeautifulSoup(test1, "html.parser")
    description = "".join(soup.strings)
    return description


def scrape_pypi(query):  # i know this is messy but who cares
    url = "https://pypi.org/project/" + query
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    html_text = soup.get_text()
    try:
        description = soup.find(class_="project-description").get_text().strip().partition('\n')[0]
    except AttributeError:
        raise commands.CommandError('Package Not Found')
    name = soup.find(class_="package-header__name").get_text().strip()

    for item in html_text.split('\n'):
        if "License:" in item:
            license = item.strip()[9:]
        if "Author:" in item:
            author = item.strip()[8:]

    homepage = soup.find('a', class_="vertical-tabs__tab vertical-tabs__tab--with-icon vertical-tabs__tab--condensed").get('href')

    return homepage, author, license, description, url, name
