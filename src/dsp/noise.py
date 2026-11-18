import numpy as np

class SoundGenerator: 

    def generate_white_noise(self, durationSeconds, mean = 0, std_deviation = 0.1):

        if durationSeconds <= 0: return False

        num_samples = int(self.samplerate * durationSeconds)

        # Generate the values using a normal distribution.
        array = np.random.normal(mean, std_deviation, num_samples)

        # Basic filtering. High and Low pass filters around the audible spectrum.
        array = self.apply_highPass(array, 20, 4)
        array = self.apply_lowPass(array, 20000, 4)
        return array