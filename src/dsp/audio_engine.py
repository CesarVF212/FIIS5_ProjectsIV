import os
import sounddevice as sd
import soundfile as sf
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

from .filters import SoundFilters
from .noise import SoundGenerator

class Sound(SoundFilters, SoundGenerator):

    def __init__(self, samplerate=44100, blocksize=256, channels=2, device=None):
        self.samplerate = samplerate
        self.blocksize = blocksize
        self.channels = channels
        self.device = device
        self.nyq = 0.5 * self.samplerate


    def to_array(self, path):
        if not os.path.exists(path): return False
        data, file_sr = sf.read(path, dtype="float32", always_2d=True)
        return data, file_sr


    def to_mono(self, array):
        if(array.ndim > 1):
            array = np.mean(array, axis=1)
        return array


    def play_mp3(self, path):

        if not os.path.exists(path): return False
        data, file_sr = self.to_array(path)

        sd.play(data, samplerate=file_sr, device=self.device, blocksize=self.blocksize)
        sd.wait()
        return True


    def play_array(self, array):
        sd.play(array)
        sd.wait()
        return True


    def compare_psd(self, first_array, second_array):

        first_array = np.asarray(first_array)
        second_array = np.asarray(second_array)

        # Convert to mono arrays
        first_array = self.to_mono(first_array)
        second_array = self.to_mono(second_array)

        # Calculate the PSD using the Welch method.
        first_freq, first_density   = sp.signal.welch(first_array, self.samplerate, nperseg=4096)
        second_freq, second_density = sp.signal.welch(second_array, self.samplerate, nperseg=4096)

        # Convert to DB to see a more readable scale. Add a small epsilon to avoid zeros in the logarithm.
        first_db = 10 * np.log10(first_density + 1e-10)
        second_db = 10 * np.log10(second_density + 1e-10)

        # --- GRAPH ---- # 
        plt.figure(figsize=(12, 6))

        plt.plot(first_freq, first_db, label = "First Array", color="blue")
        plt.plot(second_freq, second_db, label = "Second Array", color="red")

        plt.title("Comparative PSD response.")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Intensity (DB)")

        # Center around the audible spectrum.
        plt.xlim(0, 22000)

        plt.show()