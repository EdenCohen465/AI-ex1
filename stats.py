"""
This file should be runnable to print map_statistics using
$ python stats.py
"""
import collections
from collections import namedtuple
from ways import load_map_from_csv


def num_of_links(roads):
    num = 0
    for link in roads.iterlinks():
        num += 1
    return num


def calc_distance(roads):
    link_list = []
    for links in roads.iterlinks():
        link_list.append(links)
    distance_list = list(li.distance for li in link_list)
    min_d = min(distance_list)
    max_d = max(distance_list)
    avg_d = sum(distance_list) / len(distance_list)
    return min_d, max_d, avg_d


def calc_branching_factor(roads):
    min_b = len(min(roads.junctions(), key=lambda j: len(j.links)).links)
    max_b = len(max(roads.junctions(), key=lambda j: len(j.links)).links)
    avg_b = num_of_links(roads) / len(roads.junctions())
    return min_b, max_b, avg_b



def create_link_type_histogram(roads):
    link_list = list(li for li in roads.iterlinks())
    highway_type_list = list(li.highway_type for li in link_list)
    return collections.Counter(highway_type_list)

# Get roads - dict of junctions.
def map_statistics(roads):
    """return a dictionary containing the desired information
    You can edit this function as you wish"""
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])
    min_b, max_b, avg_b = calc_branching_factor(roads)
    min_d, max_d, avg_d = calc_distance(roads)
    return {
        'Number of junctions': len(roads),
        'Number of links': num_of_links(roads),
        'Outgoing branching factor': Stat(max=max_b, min=min_b, avg=avg_b),  # maximum number of links in junction
        'Link distance': Stat(max=max_d, min=min_d, avg=avg_d),
        # value should be a dictionary
        # mapping each road_info.TYPE to the no' of links of this type
        'Link type histogram': create_link_type_histogram(roads),
    }


def print_stats():
    for k, v in map_statistics(load_map_from_csv()).items():
        print('{}: {}'.format(k, v))


if __name__ == '__main__':
    from sys import argv

    assert len(argv) == 1
    print_stats()
