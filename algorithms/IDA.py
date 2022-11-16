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

    # if we get to the goal-return the node and the limit
    if current_j == target:
        return path

    j = roads[current_j]
    t = roads[target]
    # calc the heuristic distance to the target. if we are not in the limit, return.
    new_f = cost + h(j.lat, j.lon, t.lat, t.lon)
    if new_f > f_limit:
        new_limit = min(new_f, new_limit)
        return []

    print("Visiting Node " + str(current_j))

    # else, we are in the limit, so continue to expand the children.
    for neighbor in j.links:
        print(path)
        n = roads[neighbor.target]
        print(n)
        path = DFS_countour(roads, n.index, cost + f(current_j, neighbor.target), path.append(n.index), f_limit, target, h, f)
        if len(path) > 0:
            return path
    return []


def IDA_star(roads, source, target, f, h):
    global new_limit
    new_limit = h(roads[source].lat, roads[source].lon, roads[target].lat, roads[target].lon)
    while True:
        print("Iteration with threshold: " + str(new_limit))
        f_limit = new_limit
        new_limit = float("inf")
        path = list()
        print('path:=========================', path)
        path = DFS_countour(roads, source, 0, path, f_limit, target, h, f)
        if len(path) > 0:
            return path


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
        array_of_index_to_problem = set()
        while len(array_of_index_to_problem) < 10:
            array_of_index_to_problem.add(random.randint(1, 100))
        for i in array_of_index_to_problem:
            p = problems[i]
            path = IDA_star(roads, p[0], p[1], f=lambda j_1, j_2:
            astar.huristic_function(roads[j_1].lat, roads[j_1].lon, roads[j_2].lat, roads[j_2].lon) + ucs.g(j_1, j_2),
                            h=astar.huristic_function)


if __name__ == '__main__':
    # asar_run()
    ida_run()
