import os
import sounddevice as sd
import soundfile as sf

class SoundDevice():

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
