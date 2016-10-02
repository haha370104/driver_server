import threading


class thread(threading.Thread):
    function = None
    args = None
    kwargs = None

    def __init__(self, function, args, kwargs=None):
        threading.Thread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        if not self.kwargs:
            self.function(*self.args)
        else:
            self.function(*self.args, **self.kwargs)
