import numpy as np


def genCrossCorrUsingPhaseTransform(sig, refsig, fs=1, max_tau=None):
    """
    Function computing the seconds between two real signals,
    using generelized cross correlation on the phase transform, computed using numpys real fast fourier transform

    :param sig:
    :param refsig:
    :param fs:
    :param max_tau:
    :return The shift in seconds:
    """
    # make sure the length for the FFT is larger or equal than len(sig) + len(refsig)
    n = sig.shape[0] + refsig.shape[0]

    #turns the signal and the reference signal into their respective phase transform using real fast fourier transform
    SIG = np.fft.rfft(sig, n=n)
    REFSIG = np.fft.rfft(refsig, n=n)

    #
    R = SIG * np.conj(REFSIG)

    cc = np.fft.irfft(R / np.abs(R), n=n)

    max_shift = int(n / 2)
    if max_tau:
        max_shift = np.minimum(int(fs * max_tau), max_shift)

    cc = np.concatenate((cc[-max_shift:], cc[:max_shift + 1]))

    # find the index where the signal from the two mics matches the best (The maximum of the generalised cross correlation)
    shift = np.argmax(np.abs(cc)) - max_shift
    #converts the maximum from samples to seconds using the sample frequenzy
    tau = shift / float(fs)

    return tau, cc



refsig = np.linspace(1, 10, 10)

for i in range(0, 10):
    sig = np.concatenate((np.linspace(0, 0, i), refsig, np.linspace(0, 0, 10 - i)))
    offset, _ = gcc_phat(sig, refsig)
    print(offset)