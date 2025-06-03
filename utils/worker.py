from threading import Thread


class Worker(Thread):
    def __init__(self, function: any, **kwargs):
        self.function = function
        self.kwargs = kwargs
        super().__init__()

    def run(self):
        print("func start")
        self.function(**self.kwargs)
        print("func end")
