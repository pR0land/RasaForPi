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

    #reverts back to sample representation of signal using the invers real fast fourier transform
    cc = np.fft.irfft(normalizedCrossSpectrum, n=n)

    # we then make calculate how much the maximum shift can be, either the mean of the signals, or the maximum time
    # in seconds as times the sample rate
    maxShift = int(n / 2)
    if maxShiftInSec:
        maxShift = np.minimum(int(fs * maxShiftInSec), maxShift)

    # we then only take the last part of the signal, and the first part of the signal
    # this is done because the shift cant be longer than maxshift, since the mics are only that far appart
    # the reason we take the last part of the signal first, is because these represent the negative lag
    # ei the lag where the refference signal is the one leading the input signal meaning the refference mic is the one
    # getting the signal first.
    # The other half is the positive lag, representing the situation where the input signal is the one which captures
    # the signal first.
    cc = np.concatenate((cc[-maxShift:], cc[:maxShift + 1]))

    # find the index where the signal from the two mics matches the best (The maximum of the generalised cross correlation)
    # then subtract the maximum shift, since if the lag was from the second part of the signal, the lag is positive
    # but as the negative lag is saved in the same array we need to subtrack those indexes
    # on the other hand, if the lag was in the first part of the signal, the lag should be negative, duo to the mics
    # being shifted, so its the refference mic capturing the signal last.
    sampleShift = np.argmax(np.abs(cc)) - maxShift
    #converts the maximum from samples to seconds using the sample frequenzy
    shiftInSec = sampleShift / float(fs)

    return shiftInSec
