import os
import sounddevice as sd
import soundfile as sf
import numpy as np

class Sound():

    def __init__(self, samplerate=44100, blocksize=256, channels=2, device=None):
        self.samplerate = samplerate
        self.blocksize = blocksize
        self.channels = channels
        self.device = device

    def play_mp3(self, path):

        if not os.path.exists(path): return False
        data, file_sr = sf.read(path, dtype="float32", always_2d=True)
        sd.play(data, samplerate=file_sr, device=self.device, blocksize=self.blocksize)
        sd.wait()
        return True

    def play_array(self, array):
        sd.play(array)
        sd.wait()
        return True

    def generate_white_noise(self, durationSeconds, mean = 0, std_deviation = 0.1):
        if durationSeconds <= 0: return False

        num_samples = int(self.samplerate * durationSeconds)

        # Generate the values using a normal distribution.
        array = np.random.normal(mean, std_deviation, num_samples)
        return array

