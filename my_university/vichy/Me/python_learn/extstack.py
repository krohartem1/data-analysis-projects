class ExtendedStack(list):
    def sum(self):
        top1 = self.pop()
        top2 = self.pop()
        self.append(top1 + top2)

    def sub(self):
        top1 = self.pop()
        top2 = self.pop()
        self.append(top1 - top2)

    def mul(self):
        top1 = self.pop()
        top2 = self.pop()
        self.append(top1 * top2)

    def div(self):
        top1 = self.pop()
        top2 = self.pop()
        if top2 != 0:
            self.append(top1 // top2)
