
def find_min_distances_and_predecessor(roads, source, target, f):
    # The only critter of adding a node to queue is if its distance has changed at the current step.
    frontier = [(source, 0)]
    # init distances to be infinity
    min_distances = {junction.index: float("inf") for junction in roads.junctions()}
    min_distances[source] = 0  # cost for getting from source to source is 0.
    # init the predecessor dict
    predecessor = {}
    # while queue is not empty
    while frontier:
        print(frontier)
        pair_min =min(frontier, key=lambda p: p[1])
        # in the first iteration, the only member in the queue is the source.
        current_junc_index = pair_min[0]
        frontier.remove(pair_min)
        if current_junc_index == target:
            return min_distances, predecessor
        # loop through the links of current junction
        for link in roads[current_junc_index].links:
            # get junc info of the current link
            neighbor_link = roads[link.target]
            current_j = roads[current_junc_index]
            # get potential new_dist from start to link = the distance from s to current junction + the distance
            # from current junction to neighbor link.
            new_dist = min_distances[current_junc_index] + f(current_j.lat, current_j.lon,
                                                             neighbor_link.lat,
                                                             neighbor_link.lon)

            # if the new_dist is shorter to reach neighbor updated to newDist
            if new_dist < min_distances[neighbor_link.index]:
                min_distances[neighbor_link.index] = min(new_dist, min_distances[neighbor_link.index])
                frontier.append((neighbor_link.index, new_dist))
                predecessor[neighbor_link.index] = current_junc_index

    return min_distances, predecessor


def find_path(source, target, predecessor):
    path = []
    # start from the end to the  start to fund the path
    current_node = target
    while current_node != source:
        if current_node not in predecessor:
            print("Path not reachable")
            break
        else:
            path.insert(0, current_node)
            current_node = predecessor[current_node]
    path.insert(0, source)
    return path


