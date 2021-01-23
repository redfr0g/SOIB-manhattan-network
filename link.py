class Link:
    def __init__(self, id, node_from_id, node_to_id, direction):
        self.id = id
        self.node_from_id = node_from_id
        self.node_to_id = node_to_id
        # Direction: "Uplink" = node_from_id -> node_to_id | "Downlink" = node_from_id <- node_to_id
        self.direction = direction