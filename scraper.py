import logging
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import numpy as np


def getMovies(url):

    page = urlopen(url)
    if not page:
        logging.error('urlopen Error: cannot open url')  # add logging
        return

    soup = BeautifulSoup(page, "html.parser")
    if not soup:
        logging.error('BeautifulSoup Error: cannot make the soup')
        return

    # find class ‘wikitable sortable’ in the HTML script
    table = soup.find('table',{'class':'wikitable sortable'})
    if not table:
        logging.error('Soup Find Error: cannot find table')

    #print(table)

    # extract all the links within <a>
    links = table.find_all('a')
    if not links:
        logging.error('Soup find_all Error: cannot find any link')

    movies = []
    movieLinks = []
    for link in links:
        movies.append(link.get('title'))
        movieLinks.append(link.get('href'))

    #print(movies)
    #print(movieLinks)

    return movies, movieLinks




def scrap():
    actors = []

    #start_wiki = 'https://en.wikipedia.org/wiki/Christopher_Lee_filmography'
    start_wiki = 'https://en.wikipedia.org/wiki/Michael_Caine_filmography'
    movies, movieLinks = getMovies(start_wiki)


if __name__ == "__main__":
    t = time.time()
    scrap()
    print("web scraping costs %s seconds" % np.round_(time.time() - t, 4))