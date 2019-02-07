import json
from node import node

class graph(object):
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node.value] = node

    def get_node(self, node_value):
        try:
            return self.nodes[node_value]
        except KeyError:
            return None

    def build(self):
        self.nodes = {} # reset
        with open('bacon.json', 'r') as f:
            data = json.loads(f.read())
            for movie in data['movies']:
                movie_node = node(movie['title'])
                self.add_node(movie_node) # add_node is by reference, so any change later (add_neightbour) will count
                for actor in movie['cast']:
                    actor_node = self.get_node(actor)
                    if actor_node is None:
                        actor_node = node(actor)
                        self.add_node(actor_node)
                    actor_node.add_neighbour(movie_node)
                    movie_node.add_neighbour(actor_node)
    
    def look_through_nodes(self):
        for node in self.nodes.values():
            print('node:\n{}'.format(node.value))
            print('neighbours:')
            for n in node.neighbours:
                print(n.value, end = ', ')
            print('\n------------')

    def find_path(self, end_node, start_value):
        path = [end_node.value]
        last = end_node.parent
        while last is not None:
            path.append(last.value)
            last = last.parent
        for i in reversed(path):
            if i != end_node.value:
                print(i, end = '-->')
            else:
                print(i)

    def BFS(self, start_value, end_value):
        self.build()
        queue = []
        start = self.get_node(start_value)
        if start:
            queue.append(start)
        else:
            print('wrong name')
            return 0
        while len(queue) > 0:
            current = queue[0]
            for neighbour in current.neighbours:
                if not neighbour.checked:
                    neighbour.set_parent(current)
                    if neighbour.value == end_value:
                        print('find {}!'.format(end_value))
                        self.find_path(neighbour, start_value)
                        return 0
                    else:
                        queue.append(neighbour)
            current.checked = True
            queue.pop(0)
        print('no path between {} and {}'.format(start_value, end_value))
        
    

if __name__ == "__main__":
    g = graph()
    g.build()
    #g.look_through_nodes()
    g.BFS('Julia Roberts', 'Kevin Bacon')
    g.BFS('Julia Roberts', 'Julia Roberts')
    g.BFS('Rachel McAdams', 'Kevin Bacon')
    g.BFS('Paul Reiser', 'Kevin Bacon')
    g.BFS('Ellen Barkin', 'Kevin Bacon')
    g.BFS('Lynne Marta', 'Kevin Bacon')
    g.BFS('Mark Ruffalo', 'Kevin Bacon')