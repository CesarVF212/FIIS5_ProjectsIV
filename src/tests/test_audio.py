import os
from dsp.audio_engine import Sound

sound_device = Sound() 

def test_MP3():
    assert sound_device.play_mp3("tests/test.mp3") == True, "ERROR: The test does not recognise the stablished route"

def test_white_noise():
    array = sound_device.generate_white_noise(2)
    assert array.any() == True, "ERROR: The array could not be generated or the duration value was invalid"
    assert sound_device.play_array(array) == True, "The Array could not be reproduced"