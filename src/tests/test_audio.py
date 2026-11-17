import os
from dsp.audio_engine import Sound

sound_device = Sound() 

def test_MP3():
    assert sound_device.play_mp3("tests/test.mp3") == True, "ERROR: The test does not recognise the stablished route"

def test_white_noise():
    array = sound_device.generate_white_noise(2)
    assert array.any() == True, "ERROR: The array could not be generated or the duration value was invalid"
    assert sound_device.play_array(array) == True, "The Array could not be reproduced"

def test_compare_motors():
    white_noise = sound_device.generate_white_noise(3)
    assert white_noise.any() == True, "ERROR: The array could not be generated or the duration value was invalid"

    original_motor, sample_rate = sound_device.to_array("tests/concorde-motor.mp3")
    sound_device.compare_psd(white_noise, original_motor)