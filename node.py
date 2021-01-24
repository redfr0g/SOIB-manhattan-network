class Node:
    def __init__(self, id):
        self.id = id
        self.buffer_in = []
        self.buffer_out = []
        self.buffer_max = 10
