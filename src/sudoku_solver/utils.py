import pygame
import pygame.locals as py_locals


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


class BlockObject:
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


class MyGUI:
    BASE_UNIT = 20

    def __init__(self, window_title, window_size):
        if not pygame.font:
            raise ImportError("Fonts not imported")

        pygame.display.set_caption(window_title)
        self.window = pygame.display.set_mode(window_size)

        self.colours = {
            'bg_color': (230, 220, 205),
            'title_colour': (238, 201, 0),
            'board_colour': (105, 95, 80),
            'tile_colour': (134, 122, 102),
            'black': (0, 0, 0),
            'white': (255, 255, 255)
        }

        self.block_list = MyList('window', self.window)
        self.text_list = {}
        self.button_list = []

    # -------------------------- GUI Drawing ----------------------------

    def blit_text(self):
        for name, text_object in self.text_list.items():
            text, position, parent = text_object
            self.block_list[parent].surface.blit(text, position)

    def draw_board(self):

        def draw_recurse(block_iter):
            try:
                block_name, block_info = next(block_iter)
            except StopIteration:
                self.blit_text()
                return True

            self.create_surface(block_info)

            draw_recurse(block_iter)

            parent_surface = self.block_list[block_info.parent].surface
            block_pos = [int(coord * self.BASE_UNIT) for coord in block_info.coordinates]
            parent_surface.blit(block_info.surface, block_pos)

        block_iter = iter(self.block_list)
        draw_recurse(block_iter)
        pygame.display.flip()

    # -------------------------- Object Creation ----------------------------

    def create_button(self, function, name, parent, dimensions, coordinates, colour):
        # Coordinates need to be referenced from window, not parent surface
        parent_tmp = parent
        overall_coords = list(coordinates)
        while parent_tmp != 'window':
            overall_coords[0] += self.block_list[parent_tmp].coordinates[0]
            overall_coords[1] += self.block_list[parent_tmp].coordinates[1]
            parent_tmp = self.block_list[parent_tmp].parent

        # Create rect object for simplicity of collision detection
        button_rect = py_locals.Rect([int(coord * self.BASE_UNIT) for coord in overall_coords],
            [int(dim * self.BASE_UNIT) for dim in dimensions])
        self.button_list.append((name, button_rect, function))

        # Create surface as usual
        self.block_list.append(name, parent, dimensions, coordinates, colour)
        return self.block_list[name]

    def create_block(self, name, parent, dimensions, coordinates, colour):
        self.block_list.append(name, parent, dimensions, coordinates, colour)
        return self.block_list[name]

    def create_text(self, name, value, parent, colour, size):
        coords = [int(n * self.BASE_UNIT // 2) for n in self.block_list[parent].dimensions]
        font = pygame.font.Font(None, size)
        text = font.render(str(value), 1, self.colours[colour])
        pos = (text.get_rect(centerx=coords[0],
            centery=coords[1]))
        self.text_list[name] = [text, pos, parent]

    def create_surface(self, block_info):
        block_size = [int(dim * self.BASE_UNIT) for dim in block_info.dimensions]

        block = pygame.Surface(block_size)
        block = block.convert()
        block.fill(self.colours[block_info.colour])
        block_info.surface = block
