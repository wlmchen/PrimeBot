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
    url = "https://pypi.org/pypi/{}/json".format(query)
    page = requests.get(url)
    if page.status_code == 404:
        raise commands.CommandError("Package not found")
    json = page.json()
    author = json['info']['author']
    homepage = json['info']['home_page']
    license = json['info']['license']
    description = json['info']['description']
    url = json['info']['package_url']
    name = json['info']['name'] + json['info']['version']

    return homepage, author, license, description, url, name
