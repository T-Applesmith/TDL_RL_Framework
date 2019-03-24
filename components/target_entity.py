class Target_Entity:
    def __init__(self, entity_index, x, y, time_past=0, time_to_drop_track=60):
        self.entity_index = entity_index
        self.x = x
        self.y = y
        self.time_past = time_past
        self.time_to_drop_track = time_to_drop_track

    def to_json(self):
        json_data = {
            'entity_index': self.entity_index,
            'x': self.x,
            'y': self.y,
            'time_past': self.time_past,
            'time_to_drop_track': self.time_to_drop_track
        }

        return json_data

    def from_json(json_data):
        entity_index = json_data.get('entity_index')
        x = json_data.get('x')
        y = json_data.get('y')
        time_past = json_data.get('time_past')
        time_to_drop_track = json_data.get('time_to_drop_track')

        target_entity = Target_Entity(entity_index, x, y, time_past, time_to_drop_track)

        return target_entity

    def update_location(self, x, y):
        self.x, self.y = x, y
        return

    def increment_time(self):
        self.time_past += 1
        return

