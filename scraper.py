import logging
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import numpy as np
from collections import deque
import re

wiki = 'https://en.wikipedia.org/'


def read_url(url):
    # get the content of current url
    page = urlopen(url)
    if not page:
        logging.error('urlopen Error: cannot open url')  # add logging
        return

    soup = BeautifulSoup(page, "html.parser")
    if not soup:
        logging.error('BeautifulSoup Error: cannot make the soup')
        return

    return soup


def is_filmography_page(url):
    soup = read_url(url)
    table = soup.find("a", href=re.compile("filmography"))
    if not table:
        return False
    return True


def is_film_page(url):
    soup = read_url(url)
    if soup.find("title", text=re.compile("film")):
        return True
    elif soup.find_all('th', text='Directed by'):
        return True
    elif soup.find_all('th', text='directed by'):
        return True

    return False


def is_actor_page(url):
    soup = read_url(url)
    occupation = soup.find_all("td", {'class': 'role'})
    if occupation:
        for elem in occupation:
            string = elem.get_text()
            if not string:
                return False
            # Occupation is actor/actress
            elif string.find('Actor') >= 0 or string.find('actor') >= 0 or string.find('Actress') >= 0 or string.find(
                    'actress') >= 0:
                return True
    return False


def get_film_from_filmography(url, urlQueue):
    soup = read_url(url)
    # find class ‘wikitable sortable’ in the HTML script
    table = soup.find('table', {'class': 'wikitable sortable'})
    if not table:
        logging.warning('Soup Find Warning: cannot find filmography table')
        return

    # print(table)

    # extract all the links within <a>
    links = table.find_all('a')
    if not links:
        logging.warning('Soup find_all Warning: cannot find any film link from this filmography page')
        return

    movies = []
    for link in links:
        movies.append(link.get('title'))
        # get the actor information for each film
        film_url = link.get('href')
        urlQueue.append(film_url)

    return movies


def get_actor_from_film(url, urlQueue):
    soup = read_url(url)
    cast = soup.find_all('span', {'id': ['Cast']})
    if not cast:
        logging.warning('Soup find_all Warning: cannot find any cast information')
        return

    cast_list = cast[0].find_next('ul')  # unordered list
    cast_link = cast_list.find_all('a')
    if not cast_link:
        logging.warning('Soup find_all Warning: cannot find any actor link from this film page')

    actors = []
    for link in cast_link:
        actors.append(link.get('title'))
        urlQueue.append(link.get('href'))

    return actors


def get_filmography_from_actor(url, urlQueue):
    soup = read_url(url)
    filmography = soup.find("span", id=re.compile("filmography"))
    filmography_list = filmography.find_next('ul')  # unordered list
    filmography_link = filmography_list.find_all('a')
    for link in filmography_link:
        urlQueue.append(link)


def scrap():
    actorList = []
    movieList = []
    urlQueue = deque(['/wiki/Christopher_Lee_filmography'])  # start with this wiki page

    while len(movieList) < 125 or len(actorList) < 250:

        if not urlQueue:
            urlQueue.append('/wiki/Michael_Caine_filmography')  # add a new start page

        curr_url = urlQueue.popleft()
        logging.info("Current Page: " + wiki+curr_url)

        # check if the current url is a movie page or actor page or a filmography page
        if is_filmography_page(wiki+curr_url):
            movie = get_film_from_filmography(wiki+curr_url, urlQueue)
            movieList.extend(movie)
            #print("number of movies: ", len(movieList))

        elif is_film_page(wiki+curr_url):
            actor = get_actor_from_film(wiki+curr_url, urlQueue)
            actorList.extend(actor)
            #print("number of actors: ", len(actorList))

        elif is_actor_page(wiki+curr_url):
            get_filmography_from_actor(wiki+curr_url, urlQueue)

    print("number of movies: ", len(movieList))
    print("number of actors: ", len(actorList))


def main():
    logging.basicConfig(filename='scraper.log', level=logging.DEBUG)
    t = time.time()
    scrap()
    print("web scraping costs %s seconds" % np.round_(time.time() - t, 4))


if __name__ == "__main__":
    main()
