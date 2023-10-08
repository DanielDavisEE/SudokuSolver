class MyList(dict):
    """
    A dictionary with some list-like properties for storing BlockObjects
    Can:
    - keep track of parents
    - iterate by dfs
    
    """

    def __init__(self, node_name, node):
        super().__init__()
        self[node_name] = BlockObject(None, None, None, None)
        self[node_name].surface = node
        self.node_name = node_name
        self.queue = []

    def append(self, name, parent, dimensions, coordinates, colour):
        """name -> name of block
           parent -> name of parent block
           position -> euclidean coordinates of block
        """
        self[parent].children.append(name)
        self[name] = BlockObject(parent, dimensions, coordinates, colour)
        return None

    def branch(self, node):
        """Returns the branch of the tree beginning at node.
        """
        self.queue = [node]
        return (x for x in self)

    def section(self, node):
        """Deprecated for readability
        """
        return self.branch(node)

    def __delitem__(self, item):
        parent = self[item].parent
        self[parent].children.remove(item)
        super().__delitem__(item)

        # def __iter__(self):
        # if self.queue == []:
        # self.queue.extend(self[self.node][2])
        # return self

    # def __next__(self):
    # """Iterates through as a depth first search.
    # """
    # if not self.queue:
    # raise StopIteration
    # else:
    # current_object = self.queue.pop(0)
    # try:
    # self.queue.extend(self[current_object][2])
    # except KeyError as err:
    # print(err)
    # [print(x) for x in self.items()]
    # print(self.queue)
    # raise KeyError
    # return current_object, self[current_object][0], self[current_object][1]

    def __iter__(self):
        """Iterates through as a depth first search.
        """
        if not self.queue:
            self.queue.extend(self[self.node_name].children)

        while self.queue:
            current_object = self.queue.pop(0)
            self.queue.extend(self[current_object].children)
            yield current_object, self[current_object]


class BlockObject():
    def __init__(self, parent, dimensions, coordinates, colour):
        self.parent = parent
        self.dimensions = dimensions
        self.coordinates = coordinates
        self.colour = colour
        self.children = []
        self.surface = None

    def __str__(self):
        return f'Parent: {self.parent}\nDimensions: {self.dimensions}\nCoordinates: {self.coordinates}\nColour: {self.colour}\nChildren: {self.children}\nSurface: {self.surface}'

    def __repr__(self):
        return f'Block({self.parent}, {self.dimensions}, {self.coordinates}, {self.colour}, {self.children}, {self.surface})'


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


if __name__ == "__main__":
    main()
