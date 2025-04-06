class Dummy_Logger:
    def __init__(self):
        self.logs = []

    def info(self, msg):
        self.logs.append(('info', msg))

    def warn(self, msg):
        self.logs.append(('warn', msg))

    def error(self, msg):
        self.logs.append(('error', msg))

    def clear(self):
        self.logs.clear()


if __name__ == '__main__':
    logger = Dummy_Logger()
    logger.info(NameError("233"))
    logger.error(NameError("666"))
    print(logger.logs)
