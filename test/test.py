import unittest
from src import movie
from src import actor
from src import graph
from src import JSON
import json, requests
from src import data_analysis
from src.web_API import *
from flask import Flask, jsonify, request


class TestGraph(unittest.TestCase):
    def test_movie(self):
        m = movie.Movie('https://en.wikipedia.org/wiki/Corridor_of_Mirrors_(film)')
        m.set_name('Corridor of Mirrors')
        assert isinstance(m, movie.Movie)
        m.set_year(1948)
        assert(m.year == 1948)
        m.set_gross(100000)
        assert m.gross == 100000
        a = actor.Actor('https://en.wikipedia.org/wiki/Eric_Portman')
        a.set_name('Eric Portman')
        m.add_actor(a)
        assert m.actorList == [a.actor_name]

    def test_actor(self):
        a = actor.Actor('https://en.wikipedia.org/wiki/Morgan_Freeman')
        a.set_name('Morgan Freeman')
        assert isinstance(a, actor.Actor)
        m1 = movie.Movie('https://en.wikipedia.org/wiki/Brubaker')
        m1.set_name('Brubaker')
        m1.set_year(1980)

        a.add_movie(m1)
        assert a.movieList == [m1.movie_name]
        m2 = movie.Movie('https://en.wikipedia.org/wiki/Marie_(film)')
        m2.set_name('Marie')
        m2.set_year(1985)

        a.add_movie(m2)
        assert a.movieList == [m1.movie_name, m2.movie_name]

    def test_graph(self):
        g = graph.Graph()
        assert isinstance(g.movies, dict)
        assert isinstance(g.actors, dict)

        m1 = movie.Movie('https://en.wikipedia.org/wiki/Marie_(film)')
        m1.set_name("Marie")
        g.add_movie(m1)
        assert g.movies == {m1.movie_name: m1}

        a1 = actor.Actor('https://en.wikipedia.org/wiki/Sissy_Spacek')
        a1.set_name('Sissy Spacek')
        g.add_actor(a1)
        assert g.actors == {a1.actor_name: a1}

        g.add_edge(m1, a1, 69)  # date of birth as edge weight
        assert (m1.actorList == [a1.actor_name])
        assert (a1.movieList == [m1.movie_name])

        a2 = actor.Actor('https://en.wikipedia.org/wiki/Jeff_Daniels')
        a2.set_name('eff Daniels')
        g.add_actor(a2)

        g.add_edge(a2, m1, 64)
        assert a2.movieList == [m1.movie_name]
        assert m1.actorList == [a1.actor_name, a2.actor_name]
        assert g.is_connected(a2, m1) is True
        assert g.is_connected(m1, a2) is True
        assert g.is_connected(a1, m1) is True
        assert g.is_connected(m1, a1) is True


        assert g.get_neighbors(m1) == [a1.actor_name, a2.actor_name]
        assert g.get_neighbors(a1) == [m1.movie_name]
        assert g.get_neighbors(a2) == [m1.movie_name]

        a3 = actor.Actor('https://en.wikipedia.org/wiki/Morgan_Freeman')
        g.add_actor(a3)
        assert g.get_neighbors(a3) == []

        g.add_edge(m1, a2, 60)   # already exist this edge

        assert m1.actorList == g.get_neighbors(m1)
        assert a1.movieList == g.get_neighbors(a1)
        assert a2.movieList == g.get_neighbors(a2)

    def test_graph_mutual_link(self):
        g = graph.Graph()

        m = movie.Movie('https://en.wikipedia.org/wiki/Marie_(film)')
        m.set_name('Marie')
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

        g.movies['Marie'].add_actor(a1)
        g.movies['Marie'].add_actor(a2)

        g.add_edge(m, a1, 69)
        g.add_edge(m, a2, 64)

        assert g.is_connected(m, a1) and g.is_connected(a1, m)
        assert g.is_connected(m, a2) and g.is_connected(a2, m)

        JSON.store_to_Json(g, 'test2.json')




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
        #(g.list_actor_movies(a1))
        assert g.list_actor_movies(a1) == [m.movie_name]
        assert g.list_actor_movies(a2) == [m.movie_name]
        assert g.list_movie_actors(m) == [a1.actor_name, a2.actor_name]
        assert g.list_oldest_x_actors(1) == [a1]
        assert g.list_movies_for_a_year(1970) == []
        assert g.list_movies_for_a_year(1980) == []
        assert g.list_movies_for_a_year(1985) == [m]
        assert g.list_actors_for_a_year(1800) == []
        assert g.list_actors_for_a_year(2019 - 69) == [a1]


class TestJson(unittest.TestCase):
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

    def test_receive_from_Json(self):

        #g = graph.Graph()
        g, actor_data, movie_data = JSON.retrieve_from_Json('data.json')

        assert g.actors['Bruce Willis'].actor_name == 'Bruce Willis'
        assert g.actors['Bruce Willis'].age == 61
        assert g.actors['Bruce Willis'].gross == 562709189
        assert g.actors['Bruce Willis'].movieList == [
        "The First Deadly Sin",
        "The Verdict",
        "Blind Date",
        "Sunset",
        "Die Hard",
        "In Country",
        "Look Who's Talking",
        "That's Adequate",
        "Die Hard 2",
        "Look Who's Talking Too",
        "The Bonfire of the Vanities",
        "Mortal Thoughts",
        "Hudson Hawk",
        "Billy Bathgate",
        "The Last Boy Scout",
        "The Player",
        "Death Becomes Her",
        "Loaded Weapon 1",
        "Striking Distance",
        "Color of Night",
        "North",
        "Pulp Fiction",
        "Nobody's Fool",
        "Die Hard with a Vengeance",
        "Four Rooms",
        "12 Monkeys",
        "Last Man Standing",
        "Beavis and Butt-Head Do America",
        "The Fifth Element",
        "The Jackal",
        "Mercury Rising",
        "Armageddon",
        "The Siege",
        "Breakfast of Champions",
        "The Sixth Sense",
        "The Story of Us",
        "The Whole Nine Yards",
        "Disney's The Kid",
        "Unbreakable",
        "Bandits",
        "Hart's War",
        "True West",
        "The Crocodile Hunter: Collision Course",
        "Grand Champion",
        "Tears of the Sun",
        "Rugrats Go Wild",
        "Charlie's Angels: Full Throttle",
        "The Whole Ten Yards",
        "Ocean's Twelve",
        "Hostage",
        "Sin City",
        "Alpha Dog",
        "16 Blocks",
        "Fast Food Nation",
        "Lucky Number Slevin",
        "Over the Hedge",
        "Hammy's Boomerang Adventure",
        "The Astronaut Farmer",
        "Perfect Stranger",
        "Grindhouse",
        "Planet Terror",
        "Nancy Drew",
        "Live Free or Die Hard",
        "What Just Happened",
        "Assassination of a High School President",
        "Surrogates",
        "Cop Out",
        "The Expendables",
        "Red",
        "Set Up",
        "Catch .44",
        "Moonrise Kingdom",
        "Lay the Favorite",
        "The Expendables 2",
        "The Cold Light of Day",
        "Looper",
        "Fire with Fire",
        "A Good Day to Die Hard",
        "G.I. Joe: Retaliation",
        "Red 2",
        "Sin City: A Dame to Kill For",
        "The Prince",
        "Vice",
        "Rock the Kasbah",
        "Extraction",
        "Precious Cargo",
        "Marauders",
        "Split",
        "The Bombing",
        "Once Upon a Time in Venice",
        "First Kill",
        "Death Wish"
      ]

        assert g.movies["The First Deadly Sin"].movie_name == 'The First Deadly Sin'
        assert g.movies["The First Deadly Sin"].gross == 0
        assert g.movies["The First Deadly Sin"].year == 1980

    def test_data_analysis(self):
        g, actor_data, movie_data = JSON.retrieve_from_Json('data.json')
        assert not data_analysis.find_hub_actors(g, -1)
        assert data_analysis.find_hub_actors(g, 1)[0][0] == 'Bruce Willis'

        assert not data_analysis.find_most_profitable_age(g, -1)
        assert data_analysis.find_most_profitable_age(g, 1)[0][0] == 61




if __name__ == '__main__':

    unittest.main()