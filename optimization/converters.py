"""Conversion methods for communication between frontend and backend."""
import json

from user import User
from device import Device
from widget import Widget
from element import Element
from properties import Properties


class OurJSONEncoder(json.JSONEncoder):
    """Encode objects related to optimization problem formulation to JSON.

    Ensure all data can be recovered when decoded from JSON.
    """

    def default(self, o):
        """Overload method to add annotations for class instances."""
        if isinstance(o, Device) or isinstance(o, Element) or \
           isinstance(o, Widget) or isinstance(o, Properties) or \
           isinstance(o, User):
            # Add __class__ property to identify later
            out = {'__class__': o.__class__.__name__}

            variables = vars(o)
            for key, value in variables.iteritems():
                if key == 'users':
                    out[key] = [u.id for u in value]
                elif hasattr(value, '__class__'):
                    out[key] = self.default(value)
                else:
                    out[key] = value
            return out
        elif isinstance(o, list):
            out = []
            for item in o:
                if hasattr(item, '__class__'):
                    out.append(self.default(item))
                else:
                    out.append(item)
            return out
        try:
            return json.JSONEncoder.default(self, o)
        except:
            # Basic types such as ints cannot be encoded by JSONEncoder
            return o


def our_inputs_to_json(elements, devices, users):
    """Convert optimization problem specification to JSON."""
    return json.dumps(
        {'elements': elements, 'devices': devices, 'users': users},
        cls=OurJSONEncoder, indent=2, sort_keys=True).decode('utf-8')


def _our_json_decode(o):
    """Unpack JSON objects using __class__ annotations."""
    if isinstance(o, dict) and '__class__' in o:
        class_name = o['__class__']
        del o['__class__']
        if class_name == 'Properties':
            keys = o.keys()
            return Properties(**dict((k, o[k]) for k in keys))
        elif class_name == 'Element':
            return Element(**o)  # Unpack dict as keyword-arguments
        elif class_name == 'Device':
            o['affordances'] = _our_json_decode(o['affordances'])
            return Device(**o)
        elif class_name == 'Widget':
            o['requirements'] = _our_json_decode(o['requirements'])
            return Widget(**o)
        elif class_name == 'User':
            return User(**o)
    elif isinstance(o, list):
        out = []
        for item in o:
            out.append(_our_json_decode(item))
        return out
    return o


def json_to_our_inputs(s):
    """Convert JSON problem formulation from frontend to Python structures."""
    # Convert to Python structures
    out = json.loads(s, object_hook=_our_json_decode)

    # Fix Device.users lists which is originally just UIDs
    devices = out['devices']
    elements = out['elements']
    users = out['users']
    user_id_to_device = dict((u.id, u) for u in users)
    for device in devices:
        device.users = [user_id_to_device[uid] for uid in device.users]

    return elements, devices, users


def our_output_to_json(output):
    """Convert optimizer output to JSON interpretable by frontend."""
    cleaned_output = {}
    for device, assignments in output.items():
        cleaned_output[device.name] = assignments
        for i, assignment in enumerate(assignments):
            element = assignment['element']
            widget = assignment['widget']
            assignment['selected_widget_index'] = element.widgets.index(widget)
            del assignment['widget']

    return json.dumps(cleaned_output, cls=OurJSONEncoder,
                      indent=2, sort_keys=True).decode('utf-8')
