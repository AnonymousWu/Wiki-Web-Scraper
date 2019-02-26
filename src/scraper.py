import logging
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import numpy as np
from collections import deque
import re
from src import movie, actor

wiki = 'https://en.wikipedia.org/'


def read_url(url):
    # get the content of current url
    try:
        page = urlopen(wiki+url)
    except:
        logging.error('urlopen Error: cannot open url')  # add logging
        return

    soup = BeautifulSoup(page, "html.parser")
    if not soup:
        logging.error('BeautifulSoup Error: cannot make the soup')
        return

    #print(soup.prettify())
    return soup


def is_filmography_page(url):
    soup = read_url(url)
    if not soup:
        logging.warning("cannot open current url: " + wiki + url)
        return False
    table = soup.find("a", href=re.compile("filmography"))
    if not table:
        return False
    return True


def is_film_page(url):
    soup = read_url(url)
    if not soup:
        logging.warning("cannot open current url: " + wiki + url)
        return False
    if soup.find("title", text=re.compile("film")):
        return True
    elif soup.find_all('th', text='Directed by'):
        return True
    elif soup.find_all('th', text='directed by'):
        return True

    return False


def is_actor_page(url):
    soup = read_url(url)
    if not soup:
        logging.warning("cannot open current url: " + wiki + url)
        return False
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
        film_url = link.get('href')
        film_year = get_movie_year(film_url)
        print(link.get('title'), film_url, film_year)
        new_movie = movie.Movie(link.get('title'), film_url, film_year)
        movies.append(new_movie)
        # get the actor information for each film
        urlQueue.append(film_url)

    return movies


def get_movie_year(url):
    soup = read_url(url)
    if not soup:
        logging.warning("cannot open current url: " + wiki+ url)
        return 1900
    year = soup.find('span', {'class': 'bday dtstart published updated'})
    if year:
        return year.get_text()[:4]
    else:
        title = soup.title.get_text()
        for string in title.split():
            if string[1:].isdigit() and int(string[1:]) > 1800 < 2020:
                return int(string[1:])

    logging.warning("Cannot find movie year, set to default year 1900")
    return 1900


def get_actor_from_film(url, urlQueue):
    soup = read_url(url)
    # if not soup:
    #     logging.error('cannot open the url ', wiki+url)
    #     return
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
        actor_url = link.get('href')
        print(actor_url)
        actor_age = get_actor_age(actor_url)
        print(actor_age)
        new_actor = actor.Actor(link.get('title'), actor_url, actor_age)
        actors.append(new_actor)
        urlQueue.append(actor_url)

    return actors


def get_actor_age(url):
    soup = read_url(url)
    if not soup:
        logging.warning('cannot open the url')
        return 0
    showAge = soup.find('span',{"class": "noprint ForceAgeToShow"})
    if not showAge:
        # find an info table
        table = soup.find("table", {"class": "infobox biography vcard"})
        if not table:
            logging.warning("cannot find age data")
            return 0
        age = 0
        for row in table.findAll("tr"):
            if row.findAll(string=re.compile('Died')):
                try:
                    died = row.find(string=re.compile('aged')).replace("\xa0", " ")
                except:
                    logging.warning("cannot find age data")
                    return 0
                age = int(re.findall(r'\b\d+\b', died)[0])
        if not age:
            logging.warning("Soup find Warning: cannot find any age info")
            return 0
        else:
            return age
    return int(re.findall(r'\b\d+\b', showAge.text)[0])



def update_movie_gross(soup, movie):
    table = soup.find("table", {"class": "infobox vevent"})
    if not table:
        logging.info("Soup find Error: cannot find info box.")
        return
    box_office = ''
    for item in table.find_all('tr'):
        if item.findAll(string=re.compile("Box office")):
            box_office = item.find("td").text
            if "[" in box_office:
                box_office = box_office[0: box_office.index("[")]
                if (movie):
                    movie.set_gross(box_office)
            print(box_office)


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

    while len(movieList) < 10 or len(actorList) < 250:
    #while len(movieList) < 125:

        if not urlQueue:
            urlQueue.append('/wiki/Michael_Caine_filmography')  # add a new start page

        curr_url = urlQueue.popleft()
        logging.info("Current Page: " + wiki+curr_url)

        # check if the current url is a movie page or actor page or a filmography page
        if is_filmography_page(curr_url):
            m = get_film_from_filmography(curr_url, urlQueue)
            movieList.extend(m)
            print("number of movies: ", len(movieList))

        elif is_film_page(curr_url):
            a = get_actor_from_film(curr_url, urlQueue)
            actorList.extend(a)
            #print("number of actors: ", len(actorList))

        elif is_actor_page(curr_url):
            get_filmography_from_actor(curr_url, urlQueue)


    print("number of movies: ", len(movieList))
    print("number of actors: ", len(actorList))


def main():
    logging.basicConfig(filename='scraper.log', level=logging.DEBUG)
    t = time.time()
    scrap()
    print("web scraping costs %s seconds" % np.round_(time.time() - t, 4))


if __name__ == "__main__":
    main()
