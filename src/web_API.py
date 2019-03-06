import flask, json
from flask import Flask, request, jsonify
from src import actor, movie, graph, JSON, scraper

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return flask.make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def index():
    return "CS242 Assignment2.1 part 3: API Creation"

# ----------------------------- GET --------------------------------------

# /actors/all
# Get all actors name
@app.route('/actors/all', methods=['GET'])
def get_all_actors():
    return jsonify(list(g.actors.keys()))


# /actors/Bruce_Willis
@app.route('/actors/<string:actor_name>', methods=['GET'])
def get_actor_info(actor_name):
    name = actor_name.replace("_", " ")
    try:
        a = actor_data[name]
    except:
        return flask.make_response(jsonify({'error': 'Not found: ' + name}), 404)
    return jsonify(a)


# actors?name=Bruce_Willis&age=61
# /actors?name=Bob
@app.route('/actors', methods=['GET'])
def get_actor_by_filter():

    actor_name = request.args.get('name')
    name_list = []
    if actor_name:
        if '|' in actor_name:
            actor_names = actor_name.split("|")
            for n in actor_names:
                n = n.replace('_', ' ')
                name_list.append(n)
        else:
            name_list.append(actor_name.replace('_', ' '))
    print(name_list)

    actor_age = request.args.get('age')
    age_list = []
    if actor_age:
        if '|' in actor_age:
            actor_ages = actor_age.split('|')
            for n in actor_ages:
                age_list.append(int(n))
        else:
            age_list.append(int(actor_age))
    print(age_list)

    result = {}
    for a in list(g.actors.keys()):
        if not name_list:
            if actor_data[a]["age"] in age_list:
                result[a] = actor_data[a]

        else:
            if actor_data[a]["age"] in age_list or not age_list:
                for an in name_list:
                    if an == a or an in a:
                        result[a] = actor_data[a]

    if result == {}:
        return flask.make_response(jsonify({'Error': 'Not found'}), 404)

    return flask.make_response(jsonify(result), 200)


# /movies/all
# Get all movies name
@app.route('/movies/all', methods=['GET'])
def get_all_movies():
    return jsonify(list(g.movies.keys()))


# /movies/Toys
@app.route('/movies/<string:movie_name>', methods=['GET'])
def get_movie_info(movie_name):
    name = movie_name.replace("_", " ")
    try:
        m = movie_data[name]
    except:
        return flask.make_response(jsonify({'error': 'Not found: ' + name}), 404)
    return jsonify(m)


# /movies?name=Sunset&year=1988
# /movies?name=Toys
#http://127.0.0.1:5000/movies?name=Sunset|Toys&year=1988

@app.route('/movies', methods=['GET'])
def get_movie_by_filter():

    movie_name = request.args.get('name')
    name_list = []
    if movie_name:
        if '|' in movie_name:
            movie_names = movie_name.split("|")
            for n in movie_names:
                n = n.replace('_', ' ')
                name_list.append(n)
        else:
            name_list.append(movie_name.replace('_', ' '))
    print(name_list)

    movie_year = request.args.get('year')
    year_list = []
    if movie_year:
        if '|' in movie_year:
            movie_years = movie_year.split('|')
            for n in movie_years:
                year_list.append(int(n))
        else:
            year_list.append(int(movie_year))
    print(year_list)

    result = {}
    for a in list(g.movies.keys()):
        if not name_list:
            if movie_data[a]["year"] in year_list:
                result[a] = movie_data[a]
        else:
            if movie_data[a]["year"] in year_list or not year_list:
                for an in name_list:
                    if an == a or an in a:
                        result[a] = movie_data[a]

    if result == {}:
        return flask.make_response(jsonify({'Error': 'Not found: '}), 404)

    return flask.make_response(jsonify(result), 200)


# ----------------------------- PUT --------------------------------------

# Leverage PUT requests to update standing content in backend
# curl -i -X PUT -H "Content-Type: application/json" -d '
# {"total_gross":500}'http://localhost:4567/api/a/actors/Bruce_Willis
@app.route('/actors/update/<string:name>', methods=['PUT'])
def put_actor(name):

    name = name.replace('_', ' ')
    if name not in [*data[0]]:
        return flask.make_response(jsonify({'Error':  name + ' not exists in backend'}), 404)

    ndata = request.get_json()
    for item in ndata:
        try:
            data[0][name][item] = ndata[item]
        except:
            return flask.make_response(jsonify({'Error': item + ' not found'}), 404)

    with open("data copy.json", 'w') as f:
        json.dump(data, f, indent=2)

    return flask.make_response(jsonify({'Success': name + ' updated'}), 200)


@app.route('/movies/update/<string:name>', methods=['PUT'])
def put_movie(name):

    name = name.replace('_', ' ')
    if name not in [*data[1]]:
        return flask.make_response(jsonify({'Error':  name + ' not exists in backend'}), 404)

    ndata = request.get_json()
    for item in ndata:
        try:
            data[1][name][item] = ndata[item]
        except:
            return flask.make_response(jsonify({'Error': item + ' not found'}), 404)

    with open("data copy.json", 'w') as f:
        json.dump(data, f, indent=2)

    return flask.make_response(jsonify({'Success': name + ' updated'}), 200)

# ----------------------------- POST --------------------------------------

@app.route('/actors/add/<string:name>', methods=['POST'])
def add_actor(name):

    name = name.replace('_', ' ')
    if name in [*data[0]]:
        return flask.make_response(jsonify({'Error': name + ' already exists in backend'}), 404)

    ndata = request.get_json()
    data[0][name] = ndata

    with open("data copy.json", 'w') as f:
        json.dump(data, f, indent=2)

    return flask.make_response(jsonify({'Success': name + ' updated'}), 200)


@app.route('/movies/add/<string:name>', methods=['POST'])
def add_movie(name):

    name = name.replace('_', ' ')
    if name in [*data[1]]:
        return flask.make_response(jsonify({'Error': name + ' already exists in backend'}), 404)

    ndata = request.get_json()
    data[1][name] = ndata

    with open("data copy.json", 'w') as f:
        json.dump(data, f, indent=2)

    return flask.make_response(jsonify({'Success': name + ' updated'}), 200)


# ----------------------------- DELETE --------------------------------------

# http://localhost:5000/actor/delete/name_new_1
@app.route('/actors/delete/<string:name>', methods=['DELETE'])
def delete_actor(name):

    name = name.replace('_', ' ')
    if name not in [*data[0]]:
        return flask.make_response(jsonify({'Error': name + ' not exists in backend'}), 404)

    try:
        del data[0][name]
    except:
        return flask.make_response(jsonify({'Error: Cannot Delete'}), 404)

    with open("data copy.json", 'w') as f:
        json.dump(data, f, indent=2)

    return flask.make_response(jsonify({'Success': name + ' deleted'}), 200)


@app.route('/movies/delete/<string:name>', methods=['DELETE'])
def delete_movie(name):

    name = name.replace('_', ' ')
    if name not in [*data[1]]:
        return flask.make_response(jsonify({'Error': name + ' not exists in backend'}), 404)

    try:
        del data[1][name]
    except:
        return flask.make_response(jsonify({'Error: Cannot Delete'}), 404)

    with open("data copy.json", 'w') as f:
        json.dump(data, f, indent=2)

    return flask.make_response(jsonify({'Success': name + ' deleted'}), 200)


if __name__ == '__main__':

    data = json.loads(open('data copy.json').read())

    g, actor_data, movie_data = JSON.retrieve_from_Json('data.json')

    app.run(debug=True)
