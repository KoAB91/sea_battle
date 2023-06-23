class BoardOutException(Exception):

    def __init__(self, text):
        self.text = text


class ShipCreatingException(Exception):

    def __init__(self, text):
        self.text = text
