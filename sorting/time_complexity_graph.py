from matplotlib import pyplot as plt

class CounterArray(list):
    def __init__(self, l: list):
        super().__init__(l,)
        self.reads = 0
        self.writes = 0
    
    def __getitem__(self, *args, **kwargs):
        self.reads += 1
        return super().__getitem__(*args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        self.writes += 1
        return super().__setitem__(*args, **kwargs)