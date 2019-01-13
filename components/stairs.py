class Stairs:
    def __init__(self, floor):
        self.floor = floor

    def to_json(self):
        json_data = self.floor

        return json_data

    @staticmethod
    def from_json(json_data):
        stairs = Stairs(json_data)

        return stairs
