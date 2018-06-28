# Copyright 2018 AdaM Authors
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
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

    def dot(self, other):
        return self.visual_display * other.visual_display + \
               self.text_input * other.text_input + \
               self.touch_pointing * other.touch_pointing + \
               self.mouse_pointing * other.mouse_pointing

    def __repr__(self):
        return '%d|%d|%d|%d' % (self.visual_display, self.text_input, self.touch_pointing, self.mouse_pointing)
