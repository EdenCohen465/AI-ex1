import csv
import os
from collections import namedtuple

from utils import get_project_root
from ways import load_map_from_csv
from algorithms import astar as astar
from algorithms import ucs as ucs

new_limit = 0
# define class Node
Node = namedtuple('Node',
                  ['cost',  # double
                   'index',  # int junction identifier
                   'path',  # list of junctions
                   ])
pre_nodes = {}


def DFS_countour(roads1, current_j, cost, path1, f_limit, target, h, f):
    global new_limit
    j = roads1[current_j]
    t = roads1[target]
    # calc the heuristic distance to the target. if we are not in the limit, return.
    new_f = cost + h(j.lat, j.lon, t.lat, t.lon)
    if new_f > f_limit:
        new_limit = min(new_f, new_limit)
        # pre_nodes.pop(current_j)
        return None
    # if we get to the goal-return the node and the limit
    if current_j == target:
        return path1

    # print("Visiting Node " + str(current_j))
    #
    # else, we are in the limit, so continue to expand the children.
    for neighbor in j.links:
        # print(neighbor.target)
        n = roads1[neighbor.target]
        # delete old child of current_j

        keys_to_remove = []

        pre_nodes[current_j] = neighbor.target
        if path1 is not None:
            path1.append(n.index)
            new_path = path1
        else:
            new_path = [n.index]
        path1 = DFS_countour(roads1, n.index, cost + h(j.lat, j.lon, n.lat, n.lon), new_path, f_limit, target, h, f)
        if path1 is not None:
            return path1
    return None

def find_path(source, target, predecessor):
    path = []
    # start from the end to the  start to fund the path
    current_node = source
    while current_node != target:
        if current_node not in predecessor:
            print("Path not reachable")
            break
        else:
            path.append(current_node)
            current_node = predecessor[current_node]
    path.append(target)
    return path


def IDA_star(roads2, source, target, f, h):
    global new_limit
    new_limit = h(roads2[source].lat, roads2[source].lon, roads2[target].lat, roads2[target].lon)
    i = 0
    while True:
        print("Iteration with threshold: " + str(new_limit))
        f_limit = new_limit
        new_limit = float("inf")
        path2 = DFS_countour(roads2, source, 0, None, f_limit, target, h, f)
        if path2:
            print(pre_nodes)
            print("num of iteration:          ", i)
            path = find_path(source, target, pre_nodes)
            return path
        pre_nodes.clear()
        i += 1


def find_g_time(path3, roads3):
    # print(path)
    time = 0
    for i in range(len(path3)):
        if i < len(path3) - 1:
            time += astar.g(roads3[path3[i]], roads3[path3[i + 1]])
    return time


def ida_run(roads):
    results_path = os.path.join(get_project_root(), 'results', 'IDARuns.txt')
    problem_path = os.path.join(get_project_root(), 'problems.csv')
    # check if the file already exists, if so delete the file.
    if os.path.exists(results_path):
        os.remove(results_path)

    with open(problem_path, 'r') as problems_file:
        csv_reader = csv.reader(problems_file)
        for problem in csv_reader:
            path = IDA_star(roads, int(problem[0]), int(problem[1]), f=lambda j_1, j_2:
            astar.huristic_function(roads[j_1].lat, roads[j_1].lon, roads[j_2].lat, roads[j_2].lon) + ucs.g(
                roads[j_1],
                roads[j_2]),
                            h=astar.huristic_function)
            # path.insert(0, int(problem[0]))
            with open(results_path, 'a') as results_file:
                line = ''
                for j in path:
                    line += str(j) + ' '
                line += '- ' + str(find_g_time(path, roads) + astar.huristic_function(roads[int(problem[0])].lat,
                                                                                       roads[int(problem[0])].lon,
                                                                                       roads[int(problem[1])].lat,
                                                                                       roads[
                                                                                           int(problem[1])].lon)) + '\n'
                results_file.write(line)
                print("problem =====: ", problem)
                print("pre_nodes =====: ", pre_nodes)
                print("path ======: ", path)
                print("**********************************************************************************")
                pre_nodes.clear()


if __name__ == '__main__':
    # roads = astar.load_map_from_csv()
    # path = IDA_star(roads, 742505, 742506, f=lambda j_1, j_2:
    #                 astar.huristic_function(roads[j_1].lat, roads[j_1].lon, roads[j_2].lat, roads[j_2].lon)
    #                 + ucs.g(roads[j_1], roads[j_2]), h=astar.huristic_function)
    # path.insert(0, 742505)
    # print(path)
    # print(pre_nodes)
    ida_run()

