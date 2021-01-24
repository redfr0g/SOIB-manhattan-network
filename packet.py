class Packet:
    def __init__(self, id, node_from, node_to, route, ttl):
        self.id = id
        self.node_from = node_from
        self.node_to = node_to
        self.route = route
        self.ttl = ttl

