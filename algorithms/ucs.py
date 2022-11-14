''''Ex4- USC'''
import csv
import os

from algorithms.bestPath import find_min_distances_and_predecessor, find_path
from ways import tools, graph


def ucs_run():
    roads = graph.load_map_from_csv()
    # check if the file already exists, if so delete the file.
    if os.path.exists('results/UCSRuns.txt'):
        os.remove('results/UCSRuns.txt')

    with open('ways/problems.csv', 'r') as problems_file:
        csv_reader = csv.reader(problems_file)
        for problem in csv_reader:
            print(problem)
            path, min_distance = ucs_path(int(problem[0]), int(problem[1]), roads)
            print(path, min_distance)
            with open('results/UCSRuns.txt', 'a') as results_file:
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
    return required_link.distance


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