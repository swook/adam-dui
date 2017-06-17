class Element:
    name = ''
    type = ''
    size = 0
    importance = 0

    def __init__(self, name, type, size, importance):
        self.name = name
        self.type = type
        self.size = size
        self.importance = importance

    def exampleSet(self):
        exampleElements = [
            ['default']
            ['control']
            ['display']


        ]
        return exampleElements

    def __repr__(self):
        return 'Element %s (%d) %d!' % (self.name, self.size, self.importance)
