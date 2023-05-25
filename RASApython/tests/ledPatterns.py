import time


class LedPattern(object):
    def __init__(self, show=None, number=12):
        self.pixels_number = number
        self.pixels = [0] * 4 * number

        if not show or not callable(show):
            def dummy(data):
                pass
            show = dummy

        self.show = show
        self.stop = False

    def wakeup(self, direction=0):
        position = int((direction + 15) / (360 / self.pixels_number)) % self.pixels_number

        pixels = [0, 0, 0, 24] * self.pixels_number
        pixels[position * 4 + 2] = 48

        self.show(pixels)

    def listen(self):
        pixels = [0, 0, 0, 24] * self.pixels_number

        self.show(pixels)
    def showSinglePixel(self, pixelToShow):
        pixels = []
        for i in range(12):
            if i == pixelToShow:
                for j in range(3):
                    pixels.append(0)
                pixels.append(24)
            else:
                for j in range(4):
                    pixels.append(0)
        self.show(pixels)
    def off(self):
        self.show([0] * 4 * 12)

