import csv
import os
import random

from utils import get_project_root
from ways import load_map_from_csv
from algorithms import astar as astar
from algorithms import ucs as ucs

new_limit = None


def DFS_countour(roads, current_j, cost, path, f_limit, target, h, f):
    global new_limit
    j = roads[current_j]
    t = roads[target]
    # calc the heuristic distance to the target. if we are not in the limit, return.
    new_f = cost + h(j.lat, j.lon, t.lat, t.lon)
    if new_f > f_limit:
        new_limit = min(new_f, new_limit)
        return None
    # if we get to the goal-return the node and the limit
    if current_j == target:
        return path

    print("Visiting Node " + str(current_j))

    # else, we are in the limit, so continue to expand the children.
    for neighbor in j.links:
        print(neighbor.target)
        n = roads[neighbor.target]
        new_path = []
        if path:
            path.append(neighbor.target)
            new_path = path
        else:
            new_path = [neighbor.target]
        path = DFS_countour(roads, n.index, cost + h(j.lat, j.lon, n.lat, n.lon), new_path, f_limit, target, h, f)
        if path:
            return path
    return None


def IDA_star(roads, source, target, f, h):
    global new_limit
    new_limit = h(roads[source].lat, roads[source].lon, roads[target].lat, roads[target].lon)
    while True:
        print("Iteration with threshold: " + str(new_limit))
        f_limit = new_limit
        new_limit = float("inf")
        path = DFS_countour(roads, source, 0, None, f_limit, target, h, f)
        if path:
            return path


def find_g_time(path, roads):
    # print(path)
    time = 0
    for i in range(len(path)):
        if i < len(path) - 1:
            time += astar.g(roads[path[i]], roads[path[i + 1]])
    return time


def ida_run():
    roads = load_map_from_csv()
    results_path = os.path.join(get_project_root(), 'results', 'IDARuns.txt')
    problem_path = os.path.join(get_project_root(), 'problems.csv')
    # check if the file already exists, if so delete the file.
    if os.path.exists(results_path):
        os.remove(results_path)

    with open(problem_path, 'r') as problems_file:
        csv_reader = csv.reader(problems_file)
        problems = []
        for problem in csv_reader:
            problems += problem
            path = IDA_star(roads, int(problem[0]), int(problem[1]), f=lambda j_1, j_2:
            astar.huristic_function(roads[j_1].lat, roads[j_1].lon, roads[j_2].lat, roads[j_2].lon) + ucs.g(roads[j_1],
                                                                                                            roads[j_2]),
                            h=astar.huristic_function)
            with open(results_path, 'a') as results_file:
                line = ''
                for j in path:
                    line += str(j) + ' '
                line += '- ' + str(find_g_time(roads, path) + astar.huristic_function(roads[int(problem[0])].lat,
                                                                                      roads[int(problem[0])].lon,
                                                                                      roads[int(problem[1])].lat,
                                                                                      roads[int(problem[1])].lon)) + '\n'
                results_file.write(line)



if __name__ == '__main__':

    ida_run()
