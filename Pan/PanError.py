class PanError(Exception):
    def __init__(self, v):
        self.value = v

    def __str__(self):
        return self.value
