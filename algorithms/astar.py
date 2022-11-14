import csv
import os

from algorithms.bestPath import find_min_distances_and_predecessor, find_path
import ways.tools as tools
from algorithms.ucs import g
from ways.graph import load_map_from_csv


def huristic_function(lat1, lon1, lat2, lon2):
    # estimated distance to the target / maximum speed (110)
    return tools.compute_distance(lat1, lon1, lat2, lon2) / 110


def astar_path(source, target, roads):
    min_distances, predecessor = find_min_distances_and_predecessor(roads, source, target, f=
    lambda j_1, j_2: g(j_1, j_2) + huristic_function(j_1.lat, j_2.lon, roads[target].lat, roads[target].lon))
    path = find_path(source, target, predecessor)
    if target in min_distances and min_distances[target] != float("inf"):
        return path, min_distances[target]
    else:
        return None


def asar_run():
    roads = load_map_from_csv()
    results_path ='results/AStarRuns.txt'
    # check if the file already exists, if so delete the file.
    if os.path.exists(results_path):
        os.remove(results_path)

    with open('ways/problems.csv', 'r') as problems_file:
        csv_reader = csv.reader(problems_file)
        for problem in csv_reader:
            print(problem)
            path, min_distance = astar_path(int(problem[0]), int(problem[1]), roads)
            print(path, min_distance)
            with open(results_path, 'a') as results_file:
                line = ''
                for j in path:
                    line += str(j) + ' '
                line += '- ' + str(min_distance) + '\n'
                results_file.write(line)
