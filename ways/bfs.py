import collections
from collections import deque
import graph


class RoutingProblem:

    def __init__(self, s_start, goal, G):
        self.s_start = s_start
        self.goal = goal
        self.G = G

    def actions(self, s):
        return self.G[s].keys() if s in self.G else ()

    def succ(self, s, a):
        if a in self.G[s]:
            return a
        raise ValueError(f'No route from {s} to {a}')

    def is_goal(self, s):
        return s == self.goal

    def step_cost(self, s, a):
        return self.G[s][a]

    def state_str(self, s):
        return s

    def __repr__(self):
        return {'s_start': self.s_start, 'goal': self.goal, graph: 'self.G'}


def ordered_set(coll):
    return dict.fromkeys(coll).keys()


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def expand(self, problem):
        return ordered_set([self.child_node(problem, action)
                            for action in problem.actions(self.state)])

    def child_node(self, problem, action):
        next_state = problem.succ(self.state, action)
        next_node = Node(next_state, self, action,
                         self.path_cost + problem.step_cost(self.state, action))
        return next_node

    def solution(self):
        return [node.action for node in self.path()[1:]]

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __repr__(self):
        return f"<{self.state}>"

    def __lt__(self, node):
        return self.state < node.state

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.state)


def breadth_first_graph_search(problem):
    frontier = deque([Node(problem.s_start)])  # FIFO queue
    closed_list = set()
    log = []
    while frontier:
        junction = frontier.popleft()
        log.append((problem.state_str(junction.state), junction.solution(), len(frontier),
                    problem.actions(junction.state), problem.is_goal(
            junction.state)))
        if problem.is_goal(junction.state):
            return junction.solution(), log
        closed_list.add(junction.state)
        for child in junction.expand(problem):
            if child.state not in closed_list and child not in frontier:
                frontier.append(child)
    return None, log
