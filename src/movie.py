import json
from src import actor, scraper


class Movie:

    # id = -1
    movie_name = ''
    url = ''
    year = 1900
    gross = 0
    actorList = []    # neighbors

    def __init__(self, url):
        # self.id = -1
        self.movie_name = ''
        self.url = url
        self.year = 1900
        self.gross = 0
        self.actorList = []

    def set_name(self, name):
        self.movie_name = name

    def set_year(self, year):
        self.year = year

    def set_gross(self, gross):
        self.gross = gross

    def add_actor(self, new_actor):
        if new_actor not in self.actorList:
            self.actorList.append(new_actor)

    def add_to_each_other(self):
        for a in self.actorList:
            if self not in a.movieList:
                a.add_movie(self)

    def to_json(self):
        item = {}
        # json['id'] = self.id
        item['movie_name'] = self.movie_name
        item['url'] = self.url
        item['year'] = self.year
        item['gross'] = self.gross
        item['actorList'] = []
        for a in self.actorList:
            item['actorList'].append(a.actor_name)

        return json.loads(json.dumps(item))
