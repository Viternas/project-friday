

class StateManagement:
    def __init__(self, MemoryClass):
        self.memory = MemoryClass
        return

    def get_checkpoint(self):
        checkpoints = list(self.memory.graph.nodes(data=True))

        available_tasks = [
            (checkpoint_uuid, data) for checkpoint_uuid, data in checkpoints
            if data.get('ready_to_start', True) and not data.get('completed', False)
        ]
        return available_tasks[0]

    def update_checkpoint(self, checkpoint_uuid):
        self.memory.graph.nodes[checkpoint_uuid]['completed'] = True
        successors = list(self.memory.graph.successors(checkpoint_uuid))
        if successors:
            next_node = successors[0]
            self.memory.graph.nodes[next_node]['ready_to_start'] = True

    def add_node_for_checkpoint(self, data):
        self.memory.graph.add_node
