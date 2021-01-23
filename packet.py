class Packet:
    def __init__(self, uuid, node_from, node_to, route, ttl):
        self.uuid = uuid
        self.node_from = node_from
        self.node_to = node_to
        self.route = route
        self.ttl = ttl

