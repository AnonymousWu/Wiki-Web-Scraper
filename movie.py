class Movie:
    i = -1
    name = ""
    url = ""
    year = 1900
    gross = 0

    def __init__(self, name, url, year):
        self.i = -1
        self.name = name
        self.url = url
        self.year = year
        self.gross = 0

    def set_year(self, year):
        self.year = year

    def set_gross(self, gross):
        self.gross = gross

    def to_json(self):
        json = {}
        json['i'] = self.i
        json['name'] = self.name
        json['url'] = self.url
        json['year'] = self.year
        json['gross'] = self.gross
