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

    return sorted_dic[:x]


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

    return sorted_dic[:x]

# What does the correlation between age and grossing value look like?
def plot_age_gross_corr_heatMap(g):

    # lists = []
    # age_list = []
    # gross_list = []
    # for actor_name, curr_actor in g.actors.items():
    #     age_list.append(curr_actor.age)
    #     gross_list.append(curr_actor.gross)
    #     lists.append((curr_actor.age, curr_actor.gross))
    #
    # A = np.stack((age_list, gross_list), axis=1)

    dic = {}
    for actor_name, curr_actor in g.actors.items():
        curr_age = curr_actor.age
        if curr_age not in dic:
            dic[curr_age] = curr_actor.gross
        else:
            dic[curr_age] += curr_actor.gross
    plt.scatter(list(dic.keys()), dic.values())
    plt.xlabel("age")
    plt.ylabel("gross")
    plt.title("Age-Gross Relation")
    plt.show()

    #plt.scatter(*zip(*lists))
    #plt.show()



def main():

    # ------ part 0: JSON External Support ----------- #
    g,actor_data, movie_data = JSON.retrieve_from_Json('data.json')

    # ------ part 1: Data Analysis -------------

    choice = -1
    while (choice != 0):
        choice = int(input("Data Analysis: choose from the following question:\n"
                      "1 = Display top 10 hub actors:\n"
                      "2 = Display top 10 age group that generates the most amount of money\n"
                      "3 = Display the plot of correlation between age and grossing value\n"
                      "0 = QUIT\n\n"
                      ))
        if (choice < 0 or choice > 3):
            print("Select from Question 1-3; Type 0 to quit")

        if choice == 1:
            hub = find_hub_actors(g, 10)
            print("--------------------------------------------------------------")
            print('Top %d "hub" actors in the dataset: ' % 10)
            for a in hub:
                print(a[0])
                # print(a[0] + ': ' + str(a[1]) + ' connections')
            print("--------------------------------------------------------------")

        if choice == 2:
            profit_age = find_most_profitable_age(g, 10)
            print("--------------------------------------------------------------")
            print('The top %d age groups that generate the most amount of money: ' % 10)
            for a in profit_age:
                print(a[0])
            print("--------------------------------------------------------------")

        if choice == 3:
            plot_age_gross_corr_heatMap(g)


if __name__ == "__main__":
    main()
