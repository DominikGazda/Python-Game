class Score:
    def __init__(self):
        self.result = 0

    def reset(self):
        self.result = 0

    def add_score(self, value):
        self.result += value
        # print(self.result)

    def save(self):
        pass

    def score_get(self):
        return self.result
