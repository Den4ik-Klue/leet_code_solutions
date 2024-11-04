class Node:
    def __init__(self, grid_state, x, y):
        self.grid_state = grid_state
        self.x = x
        self.y = y

        self.left = self.get_new_node(x, y - 1)
        self.right = self.get_new_node(x, y + 1)
        self.up = self.get_new_node(x - 1, y)
        self.down = self.get_new_node(x + 1, y)

        self.path_success = False

    def get_new_node(self, x, y):
        next_node = [node for node in self.grid_state['0'] if node == (x, y)]

        if not self.grid_state['0'] and self.grid_state['2'][0] == (x, y):
            return {'x': x, 'y': y, 'grid_statement': None}
        elif not next_node:
            return None

        new_state = self.deep_copy(self.grid_state)
        return {
            'x': x,
            'y': y,
            'grid_statement': self.update_statement(new_state, next_node[0])
        }

    def update_statement(self, new_state, next_node):
        new_state['0'].remove(next_node)
        new_state['1'].append(next_node)
        return new_state

    def finish(self):
        if not self.path_success:
            self.path_success = True

    def deep_copy(self, original):
        return {key: list(value) for key, value in original.items()}


class Grid:
    NODES_STATEMENT = {
        '1': [],
        '0': [],
        '2': [],
        '-1': []
    }

    def __init__(self, grid):
        self.grid = grid
        self.nodes_statement = self.create_statement()

    def create_statement(self):
        nodes_statement = {key: list(value) for key, value in self.NODES_STATEMENT.items()}

        for x, row in enumerate(self.grid):
            for y, elem in enumerate(row):
                nodes_statement[str(elem)].append((x, y))

        return nodes_statement


def unique_paths_iii(grid):
    if sum(len(row) for row in grid) == 2:
        return 1

    grid_instance = Grid(grid)
    robot = grid_instance.nodes_statement['1'][0]
    node = Node(grid_instance.nodes_statement, robot[0], robot[1])

    next_nodes = [node.left, node.right, node.down, node.up]
    next_nodes = [n for n in next_nodes if n is not None]

    return parse_binary_tree_plus(next_nodes, 0) if next_nodes else 0


def parse_binary_tree_plus(nodes, paths_count):
    for node in nodes:
        if node['grid_statement'] is None:
            paths_count += 1

            continue

        new_node = Node(node['grid_statement'], node['x'], node['y'])

        next_nodes = [new_node.left, new_node.right, new_node.down, new_node.up]
        next_nodes = [n for n in next_nodes if n is not None]

        if next_nodes:
            paths_count = parse_binary_tree_plus(next_nodes, paths_count)

    return paths_count


grid = [[0, 1], [2, 0]]
print(unique_paths_iii(grid))

grid = [[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 2]]
print(unique_paths_iii(grid))

grid = [[1, 2]]
print(unique_paths_iii(grid))
