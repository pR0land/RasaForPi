import speechRecon as sr
import directionOfArrival as DOA
from pixels import Pixels

pixels = Pixels()
with sr.SpeechRecon() as spre:
    for chunk in spre.readChunk():
        doa = DOA.getDoa(chunk,spre.RATE)
        pixels.showAngle(doa)
        print(doa)
