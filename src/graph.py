import logging
from src import scraper
from src import movie, actor


class Graph:
    movies = {}
    actors = {}
    # vertices = {}
    numVertices = 0

    def __init__(self):
        self.movies = {}
        self.actors = {}
        self.numVertices = 0

    def add_actor(self, new_actor):
        self.numVertices += 1
        self.actors[new_actor.url] = new_actor

    def add_movie(self, new_movie):
        self.numVertices += 1
        self.movies[new_movie.url] = new_movie

    def get_neighbors(self, v):
        nbr = []
        if v in self.movies.values():
            for a in self.actors.values():
                if self.is_connected(a, v) or self.is_connected(v, a):
                    nbr.append(a)
            return nbr
        elif v in self.actors.values():
            for m in self.movies.values():
                if self.is_connected(m, v) or self.is_connected(v, m):
                    nbr.append(m)
            return nbr

        return []


    def is_connected(self, v1, v2):
        if isinstance(v1, movie.Movie) and isinstance(v2, actor.Actor):
            if v2 in v1.actorList and v1 in v2.movieList:
                return True
        if isinstance(v1, actor.Actor) and isinstance(v2, movie.Movie):
            if v1 in v2.actorList and v2 in v1.movieList:
                return True
        return False

    def add_edge(self, v1, v2, cost=0):

        if self.is_connected(v1,v2) or self.is_connected(v2, v1):
            return

        # add an actor to a movie
        if isinstance(v1, movie.Movie) and isinstance(v2, actor.Actor):
            v1.add_actor(v2)
            v2.add_movie(v1)
            # self.movies[v1].add_neighbor(self.actors[v2], cost)
            self.movies[v1.url] = v1
            self.actors[v2.url] = v2
        # add a movie to an actor
        if isinstance(v1, actor.Actor) and isinstance(v2, movie.Movie):
            # if v1 not in self.actors:
            #     self.add_actor(v1)
            # if v2 not in self.movies:
            #     self.add_movie(v2)
            v1.add_movie(v2)
            v2.add_actor(v1)
            # self.actors[v1].add_neighbor(self.movies[v2], cost)
            self.actors[v1.url] = v1
            self.movies[v2.url] = v2


#  ---------------------------GRAPH QUERIES ------------------------------------- #

    # Find how much a movie has grossed
    def find_movie_gross(self, m):
        if not m or m not in self.movies.values():
            logging.warning("cannot find movie")
            return 0
        return self.movies[m.url].gross

    # List which movies an actor has worked in
    def list_actor_movies(self, a):
        if not a or a not in self.actors.values():
            logging.warning("cannot find actor")
            return 0
        return self.actors[a.url].movieList

    # List which actors worked in a movie
    def list_movie_actors(self, m):
        if not m or m not in self.movies.values():
            logging.warning("cannot find movie")
            return 0
        return self.movies[m.url].actorList

    # List the top X actors with the most total grossing value
    # NOTE: not able to do this, no information about the grossing of an actor

    # List the oldest X actors
    def list_oldest_x_actors(self, x):
        if x <= 0 or x > len(self.actors):
            logging.warning("x is too large.")
            return []
        actor_list = self.actors.values()
        sorted(actor_list, key=lambda y: y.age)
        return list(actor_list)[:x]

    # List all the movies for a given year
    def list_movies_for_a_year(self, year):
        if year < 1900:
            logging.warning("invalid year")
            return []
        movie_list = []
        for m in self.movies.values():
            if m.year == year:
                movie_list.append(m)
        return movie_list

    # List all the actors for a given year
    def list_actors_for_a_year(self, year):
        if year < 1900:
            logging.warning("invalid year")
            return []
        actor_list = []
        for a in self.actors.values():
            if a.age == 2019 - year:
                actor_list.append(a)
        return actor_list
