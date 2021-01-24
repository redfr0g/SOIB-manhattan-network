class Node:
    def __init__(self, id, buffer_size):
        self.id = id
        self.buffer_in = []
        self.buffer_out = []
        self.buffer_max = buffer_size
