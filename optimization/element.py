class Element:

    name = ''
    importance = 0
    min_width = 0
    max_width = 0
    min_height = 0
    max_height = 0
    requirements = None

    def __init__(self, name, importance, min_width, max_width, min_height,
                 max_height, requirements):
        self.name = name
        self.importance = importance
        self.requirements = requirements

        self.min_width = min_width
        self.min_height = min_height
        self._min_area = min_width * min_height

        self.max_width = max_width
        self.max_height = max_height
        self._max_area = max_width * max_height

    def __repr__(self):
        return '[Element "%s" importance=%d size_range=(%d,%d)~(%d,%d) requirements=%s]' % \
                (self.name, self.importance, self.min_width, self.min_height, self.max_width,
                 self.max_height, self.requirements)
