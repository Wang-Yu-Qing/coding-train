class node(object):
    def __init__(self, value):
        self.value = value
        self.neighbours = []
        self.parent = None
        self.checked = False
        
    def add_neighbour(self, neigh):
        self.neighbours.append(neigh)

    def set_parent(self, value):
        self.parent = value

        