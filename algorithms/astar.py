import csv
import os
import re

from utils import get_project_root
from algorithms.bestPath import find_min_distances_and_predecessor, find_path
import ways.tools as tools
from algorithms.ucs import g
from ways.graph import load_map_from_csv
from ways import info as info


def huristic_function(lat1, lon1, lat2, lon2):
    # estimated distance to the target / maximum speed (110)
    max_speed = info.SPEED_RANGES[0][1]
    return tools.compute_distance(lat1, lon1, lat2, lon2) / max_speed


def astar_path(source, target, roads):
    min_distances, predecessor = find_min_distances_and_predecessor(roads, source, target, f=
    lambda j_1, j_2: g(j_1, j_2) + huristic_function(j_2.lat, j_2.lon, roads[target].lat, roads[target].lon))
    path = find_path(source, target, predecessor)
    if target in min_distances and min_distances[target] != float("inf"):
        return path, min_distances[target]
    else:
        return None


def find_g_time(path, roads):
    time = 0
    for i in range(len(path)):
        if i < len(path) - 1:
            time += g(roads[path[i]], roads[path[i + 1]])
    return time


def asar_run():
    roads = load_map_from_csv()
    results_path = os.path.join(get_project_root(), 'results', 'AStarRuns.txt')
    problem_path = os.path.join(get_project_root(), 'problems.csv')
    # check if the file already exists, if so delete the file.
    if os.path.exists(results_path):
        os.remove(results_path)

    with open(problem_path, 'r') as problems_file:
        csv_reader = csv.reader(problems_file)
        for problem in csv_reader:
            print(problem)
            path, min_distance = astar_path(int(problem[0]), int(problem[1]), roads)
            with open(results_path, 'a') as results_file:
                line = ''
                for j in path:
                    line += str(j) + ' '
                line += '- ' + str(find_g_time(path, roads)) + ' '
                line += '- ' + str(huristic_function(roads[int(problem[0])].lat, roads[int(problem[0])].lon,
                                                     roads[int(problem[1])].lat, roads[int(problem[1])].lon)) + '\n'
                results_file.write(line)


def generate_graph():
    with open(os.path.join(get_project_root(), 'results', 'AstarRuns.txt')) as f:
        # csv_reader = csv.reader(f)
        for r in f.readlines():
            s = re.split(r'\n| - ', r)
            print(s)
            hg = [s[-2], s[-3]]

            with open(os.path.join(get_project_root(), 'results', 'graph_res.csv'), 'a') as f1:
                writer = csv.writer(f1)
                writer.writerow(hg)

if __name__ == '__main__':
    asar_run()
    #generate_graph()