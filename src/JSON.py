import json
from src import movie, actor, graph, scraper


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

    actor_dict = {}
    movie_dict = {}
    g = graph.Graph()

    #print(data)

    actor_data = data[0]
    movie_data = data[1]

    actor_list = [*actor_data]
    movie_list = [*movie_data]

    for key, value in actor_data.items():

        if value['json_class'] == 'Actor':
            if key in actor_dict:     # exist before
                new_actor = actor_dict[key]
            else:
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
                actor_dict[actor_name] = new_actor

                # add new movie
                for m in actor_movies:
                    if m not in movie_data:    # not exist in the movie database
                        continue

                    movie_item = movie_data[m]
                    if m in movie_dict:     # exist before
                        new_movie = movie_dict[m]
                    else:
                        movie_name = movie_item['name']
                        movie_url = movie_item['wiki_page']
                        movie_gross = movie_item['box_office']
                        movie_year = movie_item['year']
                        movie_actors = movie_item['actors']

                        # construct new movie class and set info
                        new_movie = movie.Movie(movie_url)
                        new_movie.set_name(movie_name)
                        new_movie.set_year(movie_year)
                        new_movie.set_gross(movie_gross)
                        g.add_movie(new_movie)  # add a new movie vertex to the graph
                        # add new edges to the graph
                        for a in movie_actors:
                            new_movie.actorList.append(a)
                        movie_dict[m] = new_movie

                    g.add_edge(new_actor, new_movie, movie_gross)



    # for key, value in movie_data.items():
    #
    #     if value['json_class'] == 'Movie':
    #         # get data related to movie
    #         movie_name = value['name']
    #         movie_url = value['wiki_page']
    #         movie_gross = value['box_office']
    #         movie_year = value['year']
    #         movie_actors = value['actors']
    #
    #         # construct new movie class and set info
    #         new_movie = movie.Movie(movie_url)
    #         new_movie.set_name(movie_name)
    #         new_movie.set_year(movie_year)
    #         new_movie.set_gross(movie_gross)
    #         g.add_movie(new_movie)  # add a new movie vertex to the graph
    #         # add new edges to the graph
    #         for a in movie_actors:
    #             new_movie.actorList.append(a)

    return g





