import json
from src import movie, actor, graph, scraper


# def store_to_Json(movies, actors, file_name):
#
#     #assert len(movies) > 125
#     #assert len(actors) > 250
#
#     data = {}
#
#     movieList = []
#     for m in movies:
#         m.to_json()
#         movieList.append(m.to_json())
#     # print(movieList)
#
#     actorList = []
#     for a in actors:
#         actorList.append(a.to_json())
#
#     data['Movie'] = movieList
#     data['Actor'] = actorList
#     with open(file_name, 'w') as outfile:
#         json.dump(data, outfile, indent=4)

def store_to_Json(g, file_name):

    #assert len(movies) > 125
    #assert len(actors) > 250

    data = {}

    movieList = []
    for m in g.movies.values():
        movieList.append(m.to_json())
    # print(movieList)

    actorList = []
    for a in g.actors.values():
        actorList.append(a.to_json())

    data['Movie'] = movieList
    data['Actor'] = actorList
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile, indent=4)


def retrive_from_Json(Json):

    # data = json.loads(open(file).read())

    actor_dict = {}
    movie_dict = {}
    g = graph.Graph()


    for item in Json:

        # get data related to movie
        movie_name = item['Movie']['movie_name']
        movie_url = item['Movie']['url']
        movie_year = item['Movie']['year']
        movie_gross = item['Movie']['gross']
        movie_actorList = item['Movie']['actorList']

        # construct new movie class and set info
        new_movie = movie.Movie(movie_url)
        new_movie.set_name(movie_name)
        new_movie.set_year(movie_year)
        new_movie.set_gross(movie_gross)
        g.add_movie(new_movie)      # add a new movie vertex to the graph
        # add new edges to the graph
        for a in movie_actorList:
            new_movie.actorList.append(a)
            if not g.is_connected(a, new_movie) or not g.is_connected(new_movie, a):
                g.add_edge(a, new_movie, movie_gross)
        if new_movie not in movie_dict:
            movie_dict[new_movie] = new_movie

        # get data related to actor
        actor_name = item['Actor']['actor_name']
        actor_url = item['Actor']['url']
        actor_age = item['Actor']['age']
        actor_movieList = item['Actor']['movieList']

        # construct new actor class and set info
        new_actor = actor.Actor(actor_url)
        new_actor.set_name(actor_name)
        new_actor.set_age(actor_age)
        g.add_actor(new_actor)     # # add a new actor vertex to the graph
        # add new edges to the graph
        for m in actor_movieList:
            new_actor.movieList.append(m)
            if not g.is_connected(m, new_actor) or not g.is_connected(new_actor, m):
                g.add_edge(m, new_actor, m.gross)
        if new_actor not in actor_dict:
            actor_dict[new_actor] = new_actor

    return graph





