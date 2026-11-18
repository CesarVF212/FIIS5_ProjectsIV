import threading
import sounddevice as sd

from visualization.renderer import Render
from acoustics.motor import MotorSound
from dsp.audio_engine import Sound

AUDIO_SAMPLES = 44100
AUDIO_BLOCKS = 256
AUDIO_DELTA_TIME = 1 / AUDIO_SAMPLES * AUDIO_BLOCKS
AUDIO_CHANNELS = 2

motor = MotorSound(duration=AUDIO_DELTA_TIME)
def audio_callback(outdata, frames, time_info, status):
    
    if(status):
        print(status, flush=True)

    chunk = motor.generate() 
    outdata[:] = chunk
        
    

if __name__ == "__main__":

    # Instanciate the audio engine.
    sound_engine = Sound()

    # Create  a direct stream flow with the sound device.
    with sd.OutputStream(
        samplerate=AUDIO_SAMPLES, 
        blocksize=AUDIO_BLOCKS, 
        channels=AUDIO_CHANNELS, 
        callback=audio_callback
    ):

        renderer = Render()
        renderer.run()