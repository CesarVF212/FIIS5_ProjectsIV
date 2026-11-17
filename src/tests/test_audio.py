import os
from dsp.audio_engine import SoundDevice

def test_MP3():
    soundDevice = SoundDevice() 
    assert soundDevice.play_mp3("tests/test.mp3") == True, "ERROR: The test does not recognise the stablished route"