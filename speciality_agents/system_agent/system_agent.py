def create_system_agent():
    class SystemAgent:
        def __init__(self, data=None):
            self.agent = data

        def run(self):
            # Implementation here
            pass

    return SystemAgent()
    
if __name__ == '__main__':
    run = create_system_agent()
    