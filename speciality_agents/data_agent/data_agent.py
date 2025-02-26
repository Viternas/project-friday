def create_data_agent():
    class DataAgent:
        def __init__(self, data=None):
            self.agent = data

        def run(self):
            # Implementation here
            pass

    return DataAgent()
    
if __name__ == '__main__':
    run = create_data_agent()
    