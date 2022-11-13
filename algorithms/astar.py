from algorithms.bestPath import find_min_distances_and_predecessor, find_path
from ways import tools


def huristic_function(lat1, lon1, lat2, lon2):
    return tools.compute_distance(lat1, lon1, lat2, lon2)


def astar_path(source, target, roads):
    min_distances, predecessor = find_min_distances_and_predecessor(roads, source, target, f=
    lambda lat1, lon1, lat2, lon2: tools.compute_distance(lat1, lon1, lat2, lon2) +
                                   huristic_function(lat1, lon1, roads[target].lat, roads[target].lon))
    path = find_path(source, target, predecessor)
    if target in min_distances and min_distances[target] != float("inf"):
        return path, min_distances[target]
    else:
        return None
