from src import actor, graph, movie, JSON, scraper
import pandas as pd
import  numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Who are the "hub" actors in your dataset?
# That is, which actors have the most connections with other actors?
# Two actors have a connection if they have acted in the same movie together.


# List the top x hub actors, i.e., top x actors have the most connections with other actors
def find_hub_actors(g, x):
    if x <= 0:
        return

    # a dictionary that maps an actor name to his/her number of connections with other actors
    dic = {}
    for movie_name, curr_movie in g.movies.items():
        actors = curr_movie.actorList
        for curr_actor in actors:
            # add connection with all other actors in this movie except himself
            if curr_actor not in dic:
                dic[curr_actor] = len(actors) - 1
            else:
                dic[curr_actor] += len(actors) - 1
    sorted_dic = sorted(dic.items(), key=lambda kv: kv[1], reverse=True)
    sorted_dic_x = sorted_dic[:x]
    print("--------------------------------------------------------------")
    print('Top %d "hub" actors in the dataset: ' % x)
    for a in sorted_dic_x:
        print(a[0])
        #print(a[0] + ': ' + str(a[1]) + ' connections')

    return sorted_dic


# Is there an age group that generates the most amount of money?
def find_most_profitable_age(g, x):
    if x <= 0:
        return

    # a dictionary that maps an age group to total amount of grossing
    dic = {}
    for actor_name, curr_actor in g.actors.items():
        curr_age = curr_actor.age
        if curr_age not in dic:
            dic[curr_age] = curr_actor.gross
        else:
            dic[curr_age] += curr_actor.gross

    sorted_dic = sorted(dic.items(), key=lambda kv: kv[1], reverse=True)
    sorted_dic_x = sorted_dic[:x]
    print("--------------------------------------------------------------")
    print('The top %d age groups that generate the most amount of money: ' % x)
    for a in sorted_dic_x:
        print(a[0])

    return dic

# What does the correlation between age and grossing value look like?
def plot_age_gross_corr_heatMap(age_gross):

    # lists = []
    # age_list = []
    # gross_list = []
    # for actor_name, curr_actor in g.actors.items():
    #     age_list.append(curr_actor.age)
    #     gross_list.append(curr_actor.gross)
    #     lists.append((curr_actor.age, curr_actor.gross))
    #
    # A = np.stack((age_list, gross_list), axis=1)
    plt.scatter(list(age_gross.keys()), age_gross.values())
    plt.xlabel("age")
    plt.ylabel("gross")
    plt.title("Age-Gross Relation")
    plt.show()

    #plt.scatter(*zip(*lists))
    #plt.show()



def main():

    # ------ part 0: JSON External Support ----------- #
    g = JSON.retrive_from_Json('data.json')

    # ------ part 1: Data Analysis -------------
    hub = find_hub_actors(g, 10)
    profit_age = find_most_profitable_age(g, 10)
    plot_age_gross_corr_heatMap(profit_age)


if __name__ == "__main__":
    main()
