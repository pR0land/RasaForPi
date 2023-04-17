import numpy as np
import sounddevice as sd
from scipy.signal import fftconvolve

# Define microphone positions as a 4x2 NumPy array
mic_pos = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])

# Define constants for speed of sound and sampling frequency
c = 343.0
fs = 44100

# Define frequencies of desired signal, time window, and FFT size
frequencies = np.arange(500, 1500, 100)
t = np.linspace(0, 0.1, int(fs * 0.1))
nfft = 2048

# Define initial angle of user's voice
theta = 0


# Define function for DOA estimation based on cross-correlation
def doa_estimation(X):
    # Compute cross-correlation matrix
    R = np.dot(X, X.T.conj()) / X.shape[1]

    # Compute eigenvalues and eigenvectors of cross-correlation matrix
    eigvals, eigvecs = np.linalg.eig(R)

    # Sort eigenvalues in descending order and get corresponding eigenvectors
    idx = eigvals.argsort()[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]

    # Compute DOA as angle between first two eigenvectors
    w = eigvecs[:, 0]
    v = eigvecs[:, 1]
    theta_est = np.angle(np.dot(w.T.conj(), v))

    return theta_est


# Define callback function for recording and beamforming
def callback(indata, frames, time, status):
    # Extract recorded signal for each microphone
    # X = np.vstack((indata[:, 0], indata[:, 1], indata[:, 2], indata[:, 3])) # <----- Add when we have more microphones
    X = np.vstack((indata[:, 0])) #                                          <----- Remove when we have more microphones

    # Compute DOA estimation based on cross-correlation
    theta_est = doa_estimation(X)

    # Update angle of user's voice
    global theta
    theta = theta_est * 180 / np.pi
    print("Current angle:", theta)  # Add this line to print the angle

    # Compute beamformed signal for each microphone and sum the results
    Y = np.zeros_like(X[0], dtype=np.complex64)
    for i in range(len(mic_pos)):
        # Compute steering vector based on current frequency and updated angle
        A = np.exp(-2j * np.pi * i / c * np.dot(mic_pos, np.array([np.cos(theta), np.sin(theta)])))

        # Compute beamformer weights based on current frequency and updated steering vector
        w = np.conj(A) / np.dot(np.conj(A), A)

        # Apply beamforming to recorded signals for current frequency
        y = fftconvolve(w, X[i], mode='valid')[0]
        Y += y

    # Play back beamformed signal
    sd.play(Y.real, samplerate=fs)


# Prints available sound devices
print(sd.query_devices(device=None, kind=None))

# Start recording and beamforming
with sd.InputStream(channels=1, blocksize=2048, samplerate=fs, callback=callback):
    sd.sleep(123456789)
