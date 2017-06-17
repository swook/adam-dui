class Device:
    def __init__(self):
        self.name = None
        self.capacity = None

    def __init__(self, name,capacity):
        self.name = name
        self.capacity = capacity

    def __repr__(self):
        return 'Device %s (%d)' % (self.name, self.capacity)

    #     name     = 'tv|laptop|phone|watch'
    # capacity = 20 |  10  |  6  |  2
