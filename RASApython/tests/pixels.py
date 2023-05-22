import apa102 as a

import threading

from ledPatterns import LedPattern
from gpiozero import LED

try:
    import queue as Queue
except ImportError:
    import Queue as Queue

class Pixels:
    number_of_pixels = 12

    def __init__(self, inPattern=LedPattern):

        self.pattern = inPattern(show=self.show)
        self.me = a.APA102(num_led=self.number_of_pixels)
        self.power = LED(5)
        self.power.on()
        self.queue = Queue.Queue()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()
        self.last_direction = None

    def wakeup(self, direction=0):
        self.last_direction = direction

        def f():
            self.pattern.wakeup(direction)

        self.put(f)

    def listen(self):
        if self.last_direction:
            def f():
                self.pattern.wakeup(self.last_direction)

            self.put(f)
        else:
            self.put(self.pattern.listen)
    def showAngle(self, angle):
        pixel = self.round_angle(angle)/30
        def f():
            self.pattern.showSinglePixel(pixel)
        self.put(f)
    def put(self, func):
        self.pattern.stop = True
        self.queue.put(func)

    def _run(self):
        while True:
            func = self.queue.get()
            self.pattern.stop = False
            func()

    def off(self):
        self.put(self.pattern.off)

    def show(self, data):
        for i in range(self.number_of_pixels):
            self.me.set_pixel(i, int(data[4 * i + 1]), int(data[4 * i + 2]), int(data[4 * i + 3]))

        self.me.show()
    def round_angle(self, angle):
        remainder = angle % 30
        if remainder < 15:
            return angle - remainder
        else:
            return angle + (30 - remainder) if angle < 360 - (30 - remainder) else 0