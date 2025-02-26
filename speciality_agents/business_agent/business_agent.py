def create_business_agent():
    class BusinessAgent:
        def __init__(self, data=None):
            self.agent = data

        def run(self):
            # Implementation here
            pass

    return BusinessAgent()
    
if __name__ == '__main__':
    run = create_business_agent()
    