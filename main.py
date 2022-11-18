import os
import random
import os
import csv

import algorithms.astar as astar
import algorithms.ucs as ucs
import ways.graph as graph
import algorithms.IDA as ida
from utils import get_project_root
from ways import draw as draw


def create_csv_problems():
    roads = graph.load_map_from_csv()
    problems = []
    while len(problems) < 100:
        s, g = generate_search_problem(roads)
        problem = [s, g]
        # check if the problem already exists-if true, generate another problem
        if problem in problems or s == g:
            continue
        problems.append(problem)
    path = 'problems.csv'
    if os.path.exists(path):
        os.remove(path)
    # write problems to csv file
    with open(path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(problems)


def generate_search_problem(roads):
    # find a path 100 times :
    # 1. generate random start junction.
    random_s = random.randint(0, len(roads))
    j_start = roads[random_s]
    # TODO: 2. change num of steps to be more complex
    steps = random.randint(7, 15)
    # 3. walk from neigbor to neighbor steps time.
    current_junction = j_start
    for i in range(steps):
        # get random neighbor-if exists, in not, set current neighbor to be the goal.
        if len(current_junction.links) == 0:
            break
        random_n = random.randint(0, len(current_junction.links) - 1)
        current_junction = roads[current_junction.links[random_n].target]
    # take the last neighbor as goal.
    j_goal = current_junction
    return j_start.index, j_goal.index


def huristic_function(lat1, lon1, lat2, lon2):
    return astar.huristic_function(lat1, lon1, lat2, lon2)


'''' Find USC path with find_min_distances_and_predecessor algorithm'''


def ida_plot():
    roads = graph.load_map_from_csv()
    problem_path = os.path.join(get_project_root(), 'problems.csv')
    with open(problem_path, 'r') as problems_file:
        csv_reader = csv.reader(problems_file)
        problems = []
        for problem in csv_reader:
            problems += [problem]
        array_of_index_to_problem = set()
        print(problems)
        while len(array_of_index_to_problem) < 10:
            array_of_index_to_problem.add(random.randint(0, 99))
        for i in array_of_index_to_problem:
            p = problems[i]
            print(p)
            path = ida.IDA_star(roads, int(p[0]), int(p[1]), f=lambda j_1, j_2:
            huristic_function(roads[j_1].lat, roads[j_1].lon, roads[j_2].lat, roads[j_2].lon) + ucs.g(roads[j_1],
                                                                                                      roads[j_2]),
                                h=huristic_function)

            draw.plot_path(roads, path)
            ida.pre_nodes.clear()


def find_ucs_rout(source, target):
    roads = graph.load_map_from_csv()
    path, min_distance = ucs.ucs_path(source, target, roads)
    return path


def find_astar_route(source, target):
    roads = graph.load_map_from_csv()
    path, min_distance = astar.astar_path(source, target, roads)
    return path


def find_idastar_route(source, target):
    roads = graph.load_map_from_csv()
    path = ida.IDA_star(roads, source, target, f=lambda j_1, j_2:
    astar.huristic_function(roads[j_1].lat, roads[j_1].lon, roads[j_2].lat, roads[j_2].lon) + ucs.g(
        roads[j_1],
        roads[j_2]),
                        h=astar.huristic_function)
    return path


def dispatch(argv):
    from sys import argv
    source, target = int(argv[2]), int(argv[3])
    if argv[1] == 'ucs':
        path = find_ucs_rout(source, target)
    elif argv[1] == 'astar':
        path = find_astar_route(source, target)
    elif argv[1] == 'idastar':
        path = find_idastar_route(source, target)
    print(' '.join(str(j) for j in path))


if __name__ == '__main__':
    from sys import argv

    # astar.asar_run()
    dispatch(argv)
    # create_csv_problems()
    # ida_plot()
