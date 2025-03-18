import time


class Loggable:
    def log(self, msg):
        print(str(time.ctime()) + ": " + str(msg))


class LoggableList(list, Loggable):
    def append(self, elem):
        list.append(self, elem)
        self.log(elem)


l = LoggableList()
l.append(3)
