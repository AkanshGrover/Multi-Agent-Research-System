#basic code, gonna be replaced in future
class Memory:
    def __init__(self):
        self.history = {}

    def add(self, what, ans):
        self.history[what] = ans

    def get(self, what):
        return self.history.get(what)

    def get_all(self):
        return self.history

    def last(self, n=5):
        items = list(self.history.items())
        return items[-n:]