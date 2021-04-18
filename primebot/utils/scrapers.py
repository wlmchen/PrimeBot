from primebot.utils.math import convert_size
import primebot
from discord.ext import commands
from bs4 import BeautifulSoup
import os
import re


def scrape_song_lyrics(url):
    page = primebot.session.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', class_='lyrics').get_text()
    # remove identifiers like chorus, verse, etc
    lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
    # remove empty lines
    lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])
    return lyrics


def scrape_pypi(query):  # i know this is messy but who cares
    url = "https://pypi.org/pypi/{}/json".format(query)
    page = primebot.session.get(url)
    if page.status == 404:
        raise commands.CommandError("Package not found")
    json = page.json()
    author = json['info']['author']
    homepage = json['info']['home_page']
    license = json['info']['license']
    description = json['info']['summary']
    url = json['info']['package_url']
    name = json['info']['name'] + ' ' + json['info']['version']

    return homepage, author, license, description, url, name


def scrape_crates(crate):
    url = "https://crates.io/api/v1/crates/{}".format(crate)
    raw = primebot.cached_session.get(url)
    if raw.status == 404:
        raise commands.CommandError("Crate not found")
    json = raw.json()
    crate = json['crate']
    name = crate['name']
    description = crate['description']
    version = crate['max_version']
    repo = crate['repository']
    docs = crate['documentation']
    downloads = crate['downloads']
    created_at = crate['created_at']
    owners = []
    owner_json = primebot.cached_session.get("https://crates.io{}".format(crate['links']['owners'])).json()['users']
    for owner in owner_json:
        owners.append('[{}]({})'.format(owner['name'], owner['url']))
    return name, description, version, repo, docs, downloads, created_at, owners


def scrape_arch(package):
    url = "https://archlinux.org/packages/search/json/?name={}".format(package)
    raw = primebot.cached_session.get(url)
    json = raw.json()
    pkg = json['results'][0]

    name = pkg['pkgname']
    description = pkg['pkgdesc']
    url = pkg['url']
    repo = pkg['repo']
    version = pkg['pkgver']
    pkgrel = pkg['pkgrel']
    arch = pkg['arch']
    pkg_size = convert_size(pkg['compressed_size'])
    installed_size = convert_size(pkg['installed_size'])
    licenses = pkg['licenses']
    build_date = pkg['build_date']
    maintainer = pkg['maintainers'][0]
    packager = pkg['packager']

    provides = pkg['provides']
    conflicts = pkg['conflicts']
    replaces = pkg['replaces']
    depends = pkg['depends']
    optdepends = pkg['optdepends']
    return name, description, url, repo, version, pkgrel, arch, pkg_size, installed_size, licenses, build_date, maintainer, packager, provides, conflicts, replaces, depends, optdepends
