from game_messages import Message

import item_functions
import utils.geometry_utils

from utils.geometry_utils import Circle, Cone, Coordinate, Line, Rect

class Item:
    def __init__(self, use_function=None, targeting=False, targeting_message=None, targeting_structure=None, **kwargs):
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.targeting_structure = targeting_structure
        self.function_kwargs = kwargs

    def to_json(self):
        if self.targeting_message:
            targeting_message_json = self.targeting_message.to_json()
        else:
            targeting_message_json = None

        if self.use_function:
            use_function_json = self.use_function.__name__
        else:
            use_function_json = None

        if self.targeting_structure:
            targeting_structure_json = self.targeting_structure.to_json()
        else:
            targeting_structure_json = None

        json_data = {
            'use_function': use_function_json,
            'targeting': self.targeting,
            'targeting_message': targeting_message_json,
            'targeting_structure': targeting_structure_json,
            'function_kwargs': self.function_kwargs
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        use_function_name = json_data.get('use_function')
        targeting = json_data.get('targeting')
        targeting_message_json = json_data.get('targeting_message')
        targeting_structure_json = json_data.get('targeting_structure')
        function_kwargs = json_data.get('function_kwargs', {})

        if use_function_name:
            use_function = getattr(item_functions, use_function_name)
        else:
            use_function = None

        if targeting_message_json:
            targeting_message = Message.from_json(targeting_message_json)
        else:
            targeting_message = None

        if targeting_structure_json:
            struct_name = targeting_structure_json.get('struct_name')
            if struct_name == 'Coordinate':
                targeting_structure = Coordinate.from_json(targeting_structure_json)
            elif struct_name == 'Circle':
                targeting_structure = Circle.from_json(targeting_structure_json)
            elif struct_name == 'Cone':
                targeting_structure = Cone.from_json(targeting_structure_json)
            elif struct_name == 'Line':
                targeting_structure = Line.from_json(targeting_structure_json)
            elif struct_name == 'Rect':
                targeting_structure = Rect.from_json(targeting_structure_json)
            else:
                targeting_structure = Coordinate.from_json(targeting_structure_json)
        else:
            targeting_structure_json = None

        item = Item(use_function, targeting, targeting_message, **function_kwargs)

        return item
