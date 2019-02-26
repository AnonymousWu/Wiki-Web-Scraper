class Movie:
    id = -1
    movie_name = ''
    url = ''
    year = 1900
    gross = ''
    actorList = []

    def __init__(self, movie_name, url, year):
        self.id = -1
        self.movie_name = movie_name
        self.url = url
        self.year = year
        self.gross = ''
        self.actorList = []

    def set_id(self, id):
        self.id = id

    def set_gross(self, gross):
        self.gross = gross

    def add_actor(self, new_actor):
        if new_actor not in self.actorList:
            self.actorList.append(new_actor)

    def to_json(self):
        json = {}
        json['id'] = self.id
        json['movie_name'] = self.movie_name
        json['url'] = self.url
        json['year'] = self.year
        json['gross'] = self.gross
        json['actorList'] = self.actorList
