import io
import logging
import math
import sys


from settings import LOG_FILE_NAME, WORD_LENGTH

logger = logging.getLogger()


class GameException(Exception):
    pass


class Node:
    def __init__(self, name):
        self.name = name
        self.neighbor_distance = {}

    def set_neighbor_distance(self, neighbor, distance):
        self.neighbor_distance[neighbor] = distance


class Graph:
    def __init__(self):
        self.nodes = {}

    def get_node(self, name) -> Node:
        return self.nodes.setdefault(name, Node(name))

    def add_edge(self, name1, name2, distance):
        node1 = self.get_node(name1)
        node2 = self.get_node(name2)
        node1.set_neighbor_distance(node2, distance)
        node2.set_neighbor_distance(node1, distance)


def configure_logging():
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s]: %(message)s')
    stdout_logger_handler = logging.StreamHandler(sys.stdout)
    stdout_logger_handler.setLevel(logging.INFO)
    stdout_logger_handler.setFormatter(formatter)
    logger.addHandler(stdout_logger_handler)

    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s]: %(message)s')
    file_logger_handler = logging.FileHandler(LOG_FILE_NAME)
    file_logger_handler.setLevel(logging.NOTSET)
    file_logger_handler.setFormatter(formatter)
    logger.addHandler(file_logger_handler)


def dijkstra(graph, start_node, end_node=None):
    ways = {}
    seen_nodes = []
    current_node = start_node
    ways[current_node] = ([current_node], 0)
    while True:
        if end_node == current_node:
            return ways[current_node]

        current_way, current_distance = ways[current_node]
        for node in current_node.neighbor_distance.keys():
            if node in seen_nodes:
                continue

            node_distance = current_node.neighbor_distance[node]
            new_distance = current_distance + node_distance

            if node in ways:
                way, distance = ways[node]
                if new_distance < distance:
                    ways[node] = current_way + [node], new_distance
            else:
                ways[node] = current_way + [node], new_distance

        seen_nodes.append(current_node)

        next_node, next_node_distance = None, math.inf
        for node, (_, distance) in ways.items():
            if node in seen_nodes:
                continue

            if next_node_distance > distance:
                next_node, next_node_distance = node, distance

        if len(graph.nodes) <= len(seen_nodes) or next_node is None:
            if end_node is not None:
                raise GameException('the way from \'{}\' to \'{}\' does not exist'.format(
                    str(start_node.name), str(end_node.name)
                ))

            return ways

        current_node = next_node


def distance_between_words(word_a, word_b):
    return sum([int(word_a[i] != word_b[i]) for i in range(0, WORD_LENGTH)])


def init_graph(dictionary):
    graph = Graph()
    for i in range(0, len(dictionary)):
        for j in range(i + 1, len(dictionary)):
            word_a, word_b = dictionary[i], dictionary[j]
            distance = distance_between_words(word_a, word_b)
            if distance == 1:
                graph.add_edge(word_a, word_b, 1)

    return graph


def print_result(way, _):
    logger.info('The resulted chain is:')
    logger.info('-'.join([str(x.name) for x in way]))


def read_dictionary():
    dictionary = []
    with io.open("dictionary.txt", encoding='utf-8') as f:
        for line in f.readlines():
            word = line.strip().lower()
            if len(word) != WORD_LENGTH:
                continue

            dictionary.append(word)

    return dictionary
