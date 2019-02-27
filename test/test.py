import unittest
from src import movie
from src import actor
from src import graph
from src import JSON
import json


class TestGraph(unittest.TestCase):
    def test_movie(self):
        m = movie.Movie('https://en.wikipedia.org/wiki/Corridor_of_Mirrors_(film)')
        assert isinstance(m, movie.Movie)
        m.set_year(1948)
        assert(m.year == 1948)
        m.set_gross(100000)
        assert m.gross == 100000
        a = actor.Actor('https://en.wikipedia.org/wiki/Eric Portman')
        m.add_actor(a)
        assert m.actorList == [a]

    def test_actor(self):
        a = actor.Actor('https://en.wikipedia.org/wiki/Morgan_Freeman')
        assert isinstance(a, actor.Actor)
        m1 = movie.Movie('https://en.wikipedia.org/wiki/Brubaker')
        m1.set_year(1980)

        a.add_movie(m1)
        assert a.movieList == [m1]
        m2 = movie.Movie('https://en.wikipedia.org/wiki/Marie_(film)')
        m2.set_year(1985)

        a.add_movie(m2)
        assert a.movieList == [m1, m2]

    def test_graph(self):
        g = graph.Graph()
        assert isinstance(g.movies, dict)
        assert isinstance(g.actors, dict)

        m1 = movie.Movie('https://en.wikipedia.org/wiki/Marie_(film)')
        g.add_movie(m1)
        assert g.movies == {m1.url: m1}

        a1 = actor.Actor('https://en.wikipedia.org/wiki/Sissy_Spacek')
        g.add_actor(a1)
        assert g.actors == {a1.url: a1}

        g.add_edge(m1, a1, 69)  # date of birth as edge weight
        assert (m1.actorList == [a1])
        assert (a1.movieList == [m1])

        a2 = actor.Actor('https://en.wikipedia.org/wiki/Jeff_Daniels')
        g.add_actor(a2)

        g.add_edge(a2, m1, 64)
        assert a2.movieList == [m1]
        assert m1.actorList == [a1, a2]
        assert g.is_connected(a2, m1) is True
        assert g.is_connected(m1, a2) is True

        assert g.get_neighbors(m1) == [a1, a2]
        assert g.get_neighbors(a1) == [m1]
        assert g.get_neighbors(a2) == [m1]

        a3 = actor.Actor('https://en.wikipedia.org/wiki/Morgan_Freeman')
        g.add_actor(a3)
        assert g.get_neighbors(a3) == []

        g.add_edge(m1, a2, 60)   # already exist this edge

        m1.add_to_each_other()
        a1.add_to_each_other()
        a2.add_to_each_other()
        assert m1.actorList == g.get_neighbors(m1)
        assert a1.movieList == g.get_neighbors(a1)
        assert a2.movieList == g.get_neighbors(a2)

    def test_graph_mutual_link(self):
        g = graph.Graph()

        m = movie.Movie('https://en.wikipedia.org/wiki/Marie_(film)')
        m.set_name('Marie (film)')
        m.set_year(1985)
        m.set_gross(3712170)

        a1 = actor.Actor('https://en.wikipedia.org/wiki/Sissy_Spacek')
        a1.set_name('Sissy Spacek')
        a1.set_age(69)
        a2 = actor.Actor('https://en.wikipedia.org/wiki/Jeff_Daniels')
        a2.set_name('Jeff Daniels')
        a2.set_age(64)

        g.add_movie(m)
        g.add_actor(a1)
        g.add_actor(a2)

        g.movies['https://en.wikipedia.org/wiki/Marie_(film)'].add_actor(a1)
        g.movies['https://en.wikipedia.org/wiki/Marie_(film)'].add_actor(a2)

        # for a in g.actors.values():
        #     g.actors[a.url].add_to_each_other()
        # for m in g.movies.values():
        #     g.movies[m.url].add_to_each_other()
        m.add_to_each_other()
        a1.add_to_each_other()
        a2.add_to_each_other()
        assert g.is_connected(m, a1) and g.is_connected(a1, m)
        assert g.is_connected(m, a2) and g.is_connected(a2, m)

        JSON.store_to_Json(g, 'test2.json')

    def test_store_to_Json(self):
        g = graph.Graph()

        m = movie.Movie('https://en.wikipedia.org/wiki/Marie_(film)')
        m.set_name('Marie (film)')
        m.set_year(1985)
        m.set_gross(3712170)

        a1 = actor.Actor('https://en.wikipedia.org/wiki/Sissy_Spacek')
        a1.set_name('Sissy Spacek')
        a1.set_age(69)
        a2 = actor.Actor('https://en.wikipedia.org/wiki/Jeff_Daniels')
        a2.set_name('Jeff Daniels')
        a2.set_age(64)

        g.add_movie(m)
        g.add_actor(a1)
        g.add_actor(a2)

        # m.add_actor(a1)
        # m.add_actor(a2)
        # a1.add_movie(m)
        # a2.add_movie(m)

        # movieList = [m]
        # actorList = [a1, a2]

        g.add_edge(m, a1)
        g.add_edge(m, a2)

        JSON.store_to_Json(g, 'test.json')


class TestQuery(unittest.TestCase):
    def test_query(self):

        g = graph.Graph()
        m = movie.Movie('https://en.wikipedia.org/wiki/Marie_(film)')
        m.set_name('Marie (film)')
        m.set_year(1985)
        m.set_gross(3712170)

        a1 = actor.Actor('https://en.wikipedia.org/wiki/Sissy_Spacek')
        a1.set_name('Sissy Spacek')
        a1.set_age(69)
        a2 = actor.Actor('https://en.wikipedia.org/wiki/Jeff_Daniels')
        a2.set_name('Jeff Daniels')
        a2.set_age(64)

        g.add_movie(m)
        g.add_actor(a1)
        g.add_actor(a2)
        g.add_edge(m, a1)
        g.add_edge(m, a2)

        assert g.find_movie_gross(m) == m.gross
        assert g.list_actor_movies(a1) == [m]
        assert g.list_actor_movies(a2) == [m]
        assert g.list_movie_actors(m) == [a1, a2]
        assert g.list_oldest_x_actors(1) == [a1]
        assert g.list_movies_for_a_year(1970) == []
        assert g.list_movies_for_a_year(1980) == []
        assert g.list_movies_for_a_year(1985) == [m]
        assert g.list_actors_for_a_year(1800) == []
        assert g.list_actors_for_a_year(2019 - 69) == [a1]



if __name__ == '__main__':

    unittest.main()