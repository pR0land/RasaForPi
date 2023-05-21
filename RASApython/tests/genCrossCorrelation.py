import numpy as np


def genCrossCorrUsingPhaseTransform(sig, refsig, fs=1, maxShiftInSec=None):
    """
    Function computing the seconds between two real signals,
    using generelized cross correlation on the phase transform, computed using numpys real fast fourier transform

    :param sig:
    :param refsig:
    :param fs:
    :param maxShiftInSec:
    :return The shift in seconds:
    """
    # make sure the length for the FFT is larger or equal than len(sig) + len(refsig)
    n = sig.shape[0] + refsig.shape[0]

    #turns the signal and the reference signal into their respective phasor transform using real fast fourier transform
    phasorSig = np.fft.rfft(sig, n=n)
    phasorRef = np.fft.rfft(refsig, n=n)

    #To compute the crossSpectrum you take the phasorrepresentation and mulitply them toghether,
    #this will multiply the magnitude of the phasors, but suptract the phase angle, therefore we instead use the
    #conjugate of the phasor representation this makes all the angles negative instead, therefore adding the angels
    #preserving the angle shift, a delayed signal would have. 
    crossSpectrum = phasorSig * np.conj(phasorRef)

    #normalizes the crossSpectrum between -1 and 1
    normalizedCrossSpectrum = (crossSpectrum / np.abs(crossSpectrum))

    cc = np.fft.irfft(normalizedCrossSpectrum, n=n)

    max_shift = int(n / 2)
    if maxShiftInSec:
        max_shift = np.minimum(int(fs * maxShiftInSec), max_shift)

    cc = np.concatenate((cc[-max_shift:], cc[:max_shift + 1]))

    # find the index where the signal from the two mics matches the best (The maximum of the generalised cross correlation)
    sampleShift = np.argmax(np.abs(cc)) - max_shift
    #converts the maximum from samples to seconds using the sample frequenzy
    shiftInSec = sampleShift / float(fs)

    return shiftInSec
