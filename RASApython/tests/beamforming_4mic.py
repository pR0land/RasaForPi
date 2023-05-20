import pyaudio
import numpy as np
import scipy
import respeaker

sound_speed = 340.
mic_dist = 0.081  # Dist between (diagonal) mics in meters. Dist from documentation
max_time_dif = mic_dist / sound_speed

mic_pairs = [[0, 2], [1, 3]]

sample_rate = 16000


def crossCorrelation(signal_1, signal_2, fs=1, max_tau=None, interp=1):
    """
    :param signal_1:    Det ene signal. der bruges i cross-correlation
    :param signal_2:    Det andet signal brugt i beregningen
    :param fs:
    :param max_tau:
    :param interp:
    :return:
    """

    # For at sikre præcise beregninger sætter vi "n" i vores fft til lig med summen af længderne af signalerne
    n = signal_1.shpe[0] + signal_2.shape[0]

    fft_1 = np.fft.rfft(signal_1, n=n)
    fft_2 = np.fft.rfft(signal_2, n=n)
    r = fft_1 * np.conj(fft_2)

    cross_correlation = np.fft.irfft(r / np.abs(r), n=(interp * n))

    max_shift = int(interp * n / 2)

    if max_tau:
        max_shift = np.minimum(int(interp * fs * max_tau), max_shift)

    cross_correlation = np.concatenate((cross_correlation[-max_shift:], cross_correlation[:max_shift + 1]))

    # find max cross correlation index
    shift = np.argmax(np.abs(cross_correlation)) - max_shift

    tau = shift / float(interp * fs)

    return tau, cross_correlation


def calculateDirection():
    tau = [0, 0]
    theta = [0, 0]

    for i, v in enumerate(mic_pairs):
        tau[i], _ = crossCorrelation(SIGNAL1, SIGNAL2, fs=sample_rate, max_tau=max_time_dif, interp=1)
        theta[i] = np.arcsin(tau[i] / max_time_dif) * 180 / np.pi

    if np.abs(theta[0]) < np.abs(theta[1]):
        if theta[1] > 0:
            best_guess = (theta[0] + 360) % 360
        else:
            best_guess = (180 - theta[0])
    else:
        if theta[0] < 0:
            best_guess = (theta[1] + 360) % 360
        else:
            best_guess = (180 - theta[1])

        best_guess = (best_guess + 270) % 360

    best_guess = (-best_guess + 120) % 360

    return best_guess


if __name__ == '__main__':
    pass