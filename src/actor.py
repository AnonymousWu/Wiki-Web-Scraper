class Actor:
    id = -1
    actor_name = ''
    age = 0
    url = ''
    gross = 0
    movieList = []

    def __init__(self, actor_name, url, age):
        self.id = -1
        self.actor_name = actor_name
        self.age = age
        self.url = url
        self.gross = 0
        self.movieList = []

    def set_id(self, id):
        self.id = id

    def add_movie(self, new_movie):
        if new_movie not in self.movieList:
            self.movieList.append(new_movie)

    def update_gross(self, new_movie):
        if new_movie not in self.movieList:
            self.gross += new_movie.gross

    def get_total_gross(self):
        for m in self.movieList:
            self.gross += m.gross

    def to_json(self):
        json = {}
        json['id'] = self.id
        json['actor_name'] = self.actor_name
        json['age'] = self.age
        json['url'] = self.url
        json['gross'] = self.gross
        json['movieList'] = self.movieList
