#basic code, gonna be replaced in future
class Memory:
    def __init__(self):
        self.history = []

    def add(self, item):
        self.history.append(item)

    def get_all(self):
        return self.history

    def last(self, n=5):
        return self.history[-n:]