import json
from src import movie, scraper


class Actor:
    # id = -1
    actor_name = ''
    url = ''
    age = 0
    # gross = 0
    movieList = []

    def __init__(self, url):
        # self.id = -1
        self.actor_name = ''
        self.url = url
        self.age = 0
        # self.gross = 0
        self.movieList = []

    def set_name(self, name):
        self.actor_name = name

    def set_age(self, age):
        self.age = age

    def add_movie(self, new_movie):
        if new_movie not in self.movieList:
            self.movieList.append(new_movie)

    # def update_gross(self, new_movie):
    #     if new_movie not in self.movieList:
    #         self.gross += new_movie.gross

    def add_to_each_other(self):
        for m in self.movieList:
            if self not in m.actorList:
                m.add_actor(self)

    def to_json(self):
        item = {}
        # json['id'] = self.id
        item['actor_name'] = self.actor_name
        item['url'] = self.url
        item['age'] = self.age
        # json['gross'] = self.gross
        item['movieList'] = []
        for m in self.movieList:
            item['movieList'].append(m.movie_name)

        return json.loads(json.dumps(item))
