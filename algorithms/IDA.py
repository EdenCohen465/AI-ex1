from bestPath import find_path


def DFS_countour(roads, f, current_node, target, distance, limit, predecessor):
    # if we get to the goal-return the node and the limit
    if current_node == target:
        return predecessor, distance, True
    print("Visiting Node " + str(current_node))
    estimated_distance = distance + f(current_node, target)
    # if we didn't find with the current limit, return the predecessor and new limit.
    if estimated_distance > limit:
        return predecessor, estimated_distance, False
    # else, we are in the limit, so continue to expand the children,
    node = roads[current_node]
    next_limit = float("inf")
    for neighbor in node.links:
        predecessor[neighbor.target] = current_node
        predecessor, distance, is_succ = DFS_countour(roads, f, neighbor, target, estimated_distance, limit,
                                                      predecessor)
        if is_succ:
            return predecessor, distance, True
        elif distance < next_limit:
            next_limit = distance
    return predecessor, next_limit, False


def IDA_star(roads, source, target, f):
    limit = f(source, target)
    while True:
        print("Iteration with threshold: " + str(limit))
        predecessor, distance, is_succ = DFS_countour(roads, f, source, target, 0, limit)
        if is_succ:
            return distance, find_path(source, target, predecessor)
        if distance == float("inf"):
            return -1

