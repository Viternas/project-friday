def create_media_agent():
    class MediaAgent:
        def __init__(self, data=None):
            self.agent = data

        def run(self):
            # Implementation here
            pass

    return MediaAgent()
    
if __name__ == '__main__':
    run = create_media_agent()
    