class Properties:

    visual_display = 0  # 0...5
    text_input = 0      # 0...5
    touch_pointing = 0  # 0...5
    mouse_pointing = 0  # 0...5

    def __init__(self, visual_display=0, text_input=0, touch_pointing=0, mouse_pointing=0):
        assert 0 <= visual_display <= 5
        assert 0 <= text_input <= 5
        assert 0 <= touch_pointing <= 5
        assert 0 <= mouse_pointing <= 5

        self.visual_display = visual_display
        self.text_input = text_input
        self.touch_pointing = touch_pointing
        self.mouse_pointing = mouse_pointing
