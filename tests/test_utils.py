import unittest

from sudoku_solver.utils import MyList


def main():
    node_name, node = 'base_node', 1
    a = MyList(node_name, node)
    a.append('node1', 'base_node', (0, 1), (0, 0), 'red')
    a.append('node2', 'base_node', (1, 1), (0, 0), 'red')
    a.append('node3', 'node1', (2, 1), (0, 0), 'red')

    print(a)

    for k, v in a:
        print(k)
        print(v)
    print('-' * 20)
    for item in a.section('node1'):
        print(item)
    print('-' * 20)
    for item in a.section('node2'):
        print(item)

    return a


class TestMyList(unittest.TestCase): pass
