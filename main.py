
import os
import algorithms.astar as astar
import algorithms.ucs as ucs
import ways.graph as graph

print(os.getcwd())



# do NOT import ways. This should be done from other files
# simply import your modules and call the appropriate functions
# class PriorityQueue:
#
#     def __init__(self, f=lambda x: x):
#         self.heap = []
#         self.f = f
#
#     def append(self, item):
#         heapq.heappush(self.heap, (self.f(item), item))
#
#     # def extend(self, items):
#     #     for item in items:
#     #         self.append(item)
#
#     def pop(self):
#         if self.heap:
#             return heapq.heappop(self.heap)[1]
#         else:
#             raise Exception('Trying to pop from empty PriorityQueue.')
#
#     def __len__(self):
#         return len(self.heap)
#
#     def __contains__(self, key):
#         return any([item == key for _, item in self.heap])
#
#     def __getitem__(self, key):
#         for value, item in self.heap:
#             if item == key:
#                 return value
#         raise KeyError(str(key) + " is not in the priority queue")
#
#     def __delitem__(self, key):
#         try:
#             del self.heap[[item == key for _, item in self.heap].index(True)]
#         except ValueError:
#             raise KeyError(str(key) + " is not in the priority queue")
#         heapq.heapify(self.heap)
#
#     def __repr__(self):
#         return str(self.heap)


def huristic_function(lat1, lon1, lat2, lon2):
    return astar.huristic_function(lat1, lon1, lat2, lon2)


# def best_first_graph_search(roads, source, target, f):
#     frontier = PriorityQueue()
#     frontier.put((0, source))
#     min_distances = {junction.index: float("inf") for junction in roads.junctions()}
#     min_distances[source] = 0  # cost for getting from source to source is 0.
#     path = []
#     predecessor = {}
#     closed_list = set()
#     while frontier:
#         current_j_i = frontier.get()[1]
#         if current_j_i == target:
#             return min_distances[current_j_i], path
#         closed_list.add(current_j_i)
#         # get current junction data
#         current_j_d = roads[current_j_i]
#         for link in current_j_d.links:
#             link_data = roads[link.target]
#             new_dist = min_distances[current_j_i] + f(current_j_d, link_data)
#             # new node
#             if link_data.index not in closed_list and link_data.index not in min_distances:
#                 frontier.put((new_dist, link_data.index))
#                 predecessor[link_data.index] = current_j_i
#                 min_distances[link_data] = new_dist
#             elif link_data.index in min_distances and new_dist < min_distances[link_data.index]:
#                 # if he already in frontier, find his preprocessor
#                 frontier.get(link_data.index)
#                 frontier.put((new_dist, link_data.index))
#                 predecessor[link_data.index] = current_j_i
#                 min_distances[link_data] = new_dist
#
#     return min_distances, predecessor


'''' Find USC path with find_min_distances_and_predecessor algorithm'''


def find_ucs_rout(source, target):
    roads = graph.load_map_from_csv()
    path, min_distance = ucs.ucs_path(source, target, roads)
    for j in path:
        print(str(j), end=" ")
    return path


def find_astar_route(source, target):
    roads = graph.load_map_from_csv()
    path, min_distance = astar.astar_path(source, target, roads)
    for j in path:
        print(str(j), end=" ")
    return path


def find_idastar_route(source, target):
    'call function to find path, and return list of indices'
    raise NotImplementedError


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
    #astar.asar_run()
    # dispatch(argv)
