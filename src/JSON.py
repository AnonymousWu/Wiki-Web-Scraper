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


def retrive_from_Json(file):

    wiki = 'https://en.wikipedia.org'

    data = json.loads(open(file).read())

    # actor_dict = {}
    # movie_dict = {}
    g = graph.Graph()

    #print(data)

    actor_data = data[0]
    movie_data = data[1]

    actor_list = [*actor_data]
    movie_list = [*movie_data]

    for key, value in actor_data.items():
        if value['json_class'] == 'Actor':
            # get data related to actor
            actor_name = value['name']
            actor_age = value['age']
            actor_gross = value['total_gross']
            actor_movies = value['movies']

            # construct new actor class and set info
            actor_url = wiki + '/wiki/' + actor_name.replace(" ", "_")
            new_actor = actor.Actor(actor_url)
            new_actor.set_name(actor_name)
            new_actor.set_age(actor_age)
            new_actor.set_gross(actor_gross)
            g.add_actor(new_actor)  # # add a new actor vertex to the graph
            for m in actor_movies:
                new_actor.movieList.append(m)

                # if not g.is_connected(m, new_actor) or not g.is_connected(new_actor, m):
                #     g.add_edge(m, new_actor, m.gross)
            # if new_actor not in actor_dict:
            #     actor_dict[new_actor] = new_actor

    for key, value in movie_data.items():

        if value['json_class'] == 'Movie':
            # get data related to movie
            movie_name = value['name']
            movie_url = value['wiki_page']
            movie_gross = value['box_office']
            movie_year = value['year']
            movie_actors = value['actors']

            # construct new movie class and set info
            new_movie = movie.Movie(movie_url)
            new_movie.set_name(movie_name)
            new_movie.set_year(movie_year)
            new_movie.set_gross(movie_gross)
            g.add_movie(new_movie)  # add a new movie vertex to the graph
            # add new edges to the graph
            for a in movie_actors:
                new_movie.actorList.append(a)
            #     if not g.is_connected(a, new_movie) or not g.is_connected(new_movie, a):
            #         g.add_edge(a, new_movie, movie_gross)
            # if new_movie not in movie_dict:
            #     movie_dict[new_movie] = new_movie

    return g





