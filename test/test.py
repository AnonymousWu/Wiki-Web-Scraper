import unittest
from src import movie
from src import actor


class TestGraph(unittest.TestCase):
    def test_movie(self):
        movie_name = 'Corridor_of_Mirrors_(film)'
        url = 'https://en.wikipedia.org/wiki/Corridor_of_Mirrors_(film)'
        year = '1948'
        m = movie.Movie(movie_name, url, year)
        assert isinstance(m, movie.Movie)
        m.set_id(10)
        assert m.id == 10
        gross = 100000
        m.set_gross(gross)
        assert m.gross == gross
        m.add_actor('Eric Portman')
        assert m.actorList == ['Eric Portman']

    def test_actor(self):
        actor_name = 'Morgan Freeman'
        url = 'https://en.wikipedia.org/wiki/Morgan_Freeman'
        age = 40
        a = actor.Actor(actor_name, url, age)
        assert isinstance(a, actor.Actor)
        a.set_id(1)
        assert a.id == 1
        a.add_movie('Brubaker')
        assert a.movieList == ['Brubaker']
        a.add_movie('Marie')
        assert a.movieList == ['Brubaker', 'Marie']

