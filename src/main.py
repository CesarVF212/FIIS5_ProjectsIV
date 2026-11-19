import threading
import sounddevice as sd

from visualization.renderer import Render
from acoustics.motor import MotorSound
from dsp.audio_engine import Sound

from physics.trajectory import *

AUDIO_SAMPLES = 44100
AUDIO_BLOCKS = 256
AUDIO_DELTA_TIME = 1 / AUDIO_SAMPLES * AUDIO_BLOCKS
AUDIO_CHANNELS = 2

FPS = 120
SIMULATION_DELTA = 1 / 120
time = 0.0

INITIAL_HEIGH = 8500
INITIAL_MACH = 0.95


motor = MotorSound(duration=AUDIO_DELTA_TIME)
def audio_callback(outdata, frames, time_info, status):
    
    if(status):
        print(status, flush=True)

    chunk = motor.generate() 
    outdata[:] = chunk
        
    

if __name__ == "__main__":

    velocity = calculate_velocity_from_Mach(INITIAL_HEIGH, INITIAL_MACH)
    print("La velocidad inicial es de ", velocity)
    # Instanciate the audio engine.
    sound_engine = Sound()

    # Create  a direct stream flow with the sound device.
    with sd.OutputStream(
        samplerate=AUDIO_SAMPLES, 
        blocksize=AUDIO_BLOCKS, 
        channels=AUDIO_CHANNELS, 
        callback=audio_callback
    ):

        print("h")
