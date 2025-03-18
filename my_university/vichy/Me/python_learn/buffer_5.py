class Buffer:
    def __init__(self):
        self.sum = 0
        self.arr = []

    def add(self, *a):
        for x in a:
            self.sum += x
            self.arr.append(x)
            if len(self.arr) == 5:
                print(self.sum)
                self.sum = 0
                self.arr.clear()

    def get_current_part(self):
        return self.arr


buf = Buffer()
buf.add(1, 2, 3)
buf.get_current_part()  # вернуть [1, 2, 3]
buf.add(4, 5, 6)  # print(15) – вывод суммы первой пятерки элементов
buf.get_current_part()  # вернуть [6]
buf.add(7, 8, 9, 10)  # print(40) – вывод суммы второй пятерки элементов
buf.get_current_part()  # вернуть []
buf.add(
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
)  # print(5), print(5) – вывод сумм третьей и четвертой пятерки
buf.get_current_part()
