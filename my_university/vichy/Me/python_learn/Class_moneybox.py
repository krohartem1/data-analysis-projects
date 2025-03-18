class MoneyBox:
    def __init__(self, capacity):
        self.count = capacity

    def can_add(self, v):
        if self.count - v >= 0:
            return True
        else:
            return False

    def add(self, v):
        self.count -= v
