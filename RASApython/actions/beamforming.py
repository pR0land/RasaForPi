import numpy as np
import sounddevice as sd
from scipy.signal import fftconvolve

# Define microphone positions as a 4x2 NumPy array
mic_pos = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])

# Define constants for speed of sound and sampling frequency
sound_speed = 343.0 # lydens hastighed i luft
fs = 44100 # vores sampling frekvens

# Define frequencies of desired signal, time window, and FFT size
frequencies = np.arange(500, 1500, 100) # eksempler på frekvenser som vi kigger efter i vores beregninger
time_window = np.linspace(0, 0.1, int(fs * 0.1))
fft_size = 2048 # vores sample rate i vores fast fourier transform

# Define initial angle of user's voice
sound_origin_angle = 0


# Define function for DOA (Direction of Arrival) estimation based on cross-correlation
def doa_estimation(sound_signals_matrix):
    # Compute cross-correlation matrix
    cc_matrix = np.dot(sound_signals_matrix, sound_signals_matrix.T.conj()) / sound_signals_matrix.shape[1]

    # Compute eigenvalues and eigenvectors of cross-correlation matrix
    eig_vals, eig_vecs = np.linalg.eig(cc_matrix)

    # Sort eigenvalues in descending order and get corresponding eigenvectors
    indices = eig_vals.argsort()[::-1]
    eig_vals = eig_vals[indices]
    eig_vecs = eig_vecs[:, indices]

    # Compute DOA as angle between first two eigenvectors
    w = eig_vecs[:, 0]
    v = eig_vecs[:, 1]
    sound_origin_angle_estimate = np.angle(np.dot(w.T.conj(), v))

    return sound_origin_angle_estimate


# Define callback function for recording and beamforming
def callback(indata, frames, time, status):
    # Extract recorded signal for each microphone
    # X = np.vstack((indata[:, 0], indata[:, 1], indata[:, 2], indata[:, 3])) # <----- Add when we have more microphones
    recorded_signal = np.vstack((indata[:, 0])) #                            <----- Remove when we have more microphones

    # Compute DOA estimation based on cross-correlation
    theta_est = doa_estimation(recorded_signal)

    # Update angle of user's voice
    global sound_origin_angle
    sound_origin_angle = theta_est * 180 / np.pi
    print("Current angle:", sound_origin_angle)  # Add this line to print the angle

    # Compute beamformed signal for each microphone and sum the results
    beamformer_output = np.zeros_like(recorded_signal[0], dtype=np.complex64)
    for i in range(len(mic_pos)):
        # Compute steering vector based on current frequency and updated angle
        steering_vector = np.exp(-2j * np.pi * i / sound_speed * np.dot(mic_pos, np.array([np.cos(sound_origin_angle), np.sin(sound_origin_angle)])))

        # Compute beamformer weights based on current frequency and updated steering vector
        beamforming_weights = np.conj(steering_vector) / np.dot(np.conj(steering_vector), steering_vector)

        # Apply beamforming to recorded signals for current frequency
        beamformed_signal = fftconvolve(beamforming_weights, recorded_signal[i], mode='valid')[0]
        beamformer_output += beamformed_signal

    # Play back beamformed signal
    sd.play(beamformer_output.real, samplerate=fs)

# Prints available sound devices
print(sd.query_devices(device=None, kind=None))

# Start recording and beamforming
with sd.InputStream(channels=1, blocksize=2048, samplerate=fs, callback=callback):
    sd.sleep(123456789)
