from vertexai.preview import agent_tools

class MCPClient:
    def __init__(self):
        self.controller = agent_tools.Controller()

    def broadcast_event(self, event_type, payload):
        self.controller.publish(event_type, payload)

    def listen(self, event_type):
        return self.controller.subscribe(event_type)
