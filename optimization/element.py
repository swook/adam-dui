from widget import Widget

class Element:

    name = ''
    importance = 0
    widgets = []

    def __init__(self, name, importance, widgets):
        assert len(widgets) > 0
        for widget in widgets:
            assert isinstance(widget, Widget)

        self.name = name
        self.importance = importance
        self.widgets = widgets

    def __repr__(self):
        return '[Element %s (%d)]' % (self.name, self.importance)
