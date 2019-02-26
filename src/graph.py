import logging
from scraper import *
import movie, actor


class Graph:

    movies = {}
    actors = {}
    #vertices = {}

    def __init__(self):
        movies = {}
        actors = {}

    def add_actor(self, new_actor):
        self.actors[new_actor] = new_actor

    def add_movie(self, new_movie):
        self.movies[new_movie] = new_movie

    # def add_vertices(self, vertices):
    #     for v in vertices:
    #         # a vertex is either a movie or an actor
    #         if isinstance(v, actor.Actor):
    #             self.vertices[v] =
    #         elif isinstance(v, movie.Movie):

    def add_edge(self, v1, v2):
        # add an actor to a movie
        if isinstance(v1, movie.Movie) and isinstance(v2, actor.Actor):
            v1.add_actor(v2)
            self.movies[v1] = v2.movieList
            self.actors[v2] = v1.actorList
        # add a movie to an actor
        if isinstance(v1, actor.Actor) and isinstance(v2, movie.Movie):
            v1.add_movie(v2)
            self.actors[v1] = v1.movieList
            self.movies[v2] = v2.actorList


