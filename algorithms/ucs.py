''''Ex4- USC'''
import csv
import os

from ways import info as info
from utils import get_project_root
from algorithms.bestPath import find_min_distances_and_predecessor, find_path
from ways import tools, graph


def ucs_run():
    roads = graph.load_map_from_csv()
    path_result = os.path.join(get_project_root(), 'results/UCSRuns.txt')
    path_problems = os.path.join(get_project_root(), 'problems.csv')
    # check if the file already exists, if so delete the file.
    if os.path.exists(path_result):
        os.remove(path_result)

    with open(path_problems, 'r') as problems_file:
        csv_reader = csv.reader(problems_file)
        for problem in csv_reader:
            print(problem)
            path, min_distance = ucs_path(int(problem[0]), int(problem[1]), roads)
            print(path, min_distance)
            with open(path_result, 'a') as results_file:
                line = ''
                for j in path:
                    line += str(j) + ' '
                line += '- ' + str(min_distance) + '\n'
                results_file.write(line)


def g(j1, j2):
    required_link = None
    for link in j1.links:
        # find the link that the target is j1:
        if link.target == j2.index:
            required_link = link
    # find maximum speed in link-
    max_speed = info.SPEED_RANGES[required_link.highway_type][1]
    return (required_link.distance * 0.001) / max_speed


def ucs_path(source, target, roads):
    min_distances, predecessor = find_min_distances_and_predecessor(roads, source, target, f=g)
    path = find_path(source, target, predecessor)
    if target in min_distances and min_distances[target] != float("inf"):
        return path, min_distances[target]
    else:
        return None


if __name__ == '__main__':
    from sys import argv

    ucs_run()
