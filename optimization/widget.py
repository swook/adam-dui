from properties import Properties

class Widget:
    size = 0
    requirements = {}
    visual_quality = 0

    def __init__(self, size, requirements, visual_quality):
        assert isinstance(size, int) and size > 0
        assert requirements is not None and isinstance(requirements, Properties)
        assert isinstance(visual_quality, int) and visual_quality > 0

        self.size = size
        self.requirements = requirements
        self.visual_quality = visual_quality

    def quality_metric(self):
        return self.visual_quality
