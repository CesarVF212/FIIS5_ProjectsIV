from dsp.audio_engine import Sound
import numpy as np

class MotorSound:

    def __init__(self, duration, acceleration=0):
        self.duration = duration
        self.acceleration = acceleration
        self.sound = Sound()

    def generate(self):
        white_noise = self.sound.generate_white_noise(durationSeconds=self.duration)

        # Add a Band EQ between 0 and 3000 hz.
        motor = self.sound.apply_peaking_eq(white_noise, 200, 18, 0.15)
        motor = self.sound.apply_lowPass(motor, 3500, 1)

        # Parse the stereo if needed.
        if motor.ndim == 1:
            motor = np.column_stack((motor, motor))
        return motor