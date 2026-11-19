import numpy as np

SPEED_OF_SOUND_IN_STRATOSPHERE = 295.07

def calculate_velocity_from_Mach(height, mach):

    if height < 0 or mach < 0:
        return ValueError("ERROR: Wrong units for height or Mach number")

    # Calculate the temperature of the air.
    if(height < 11000):
        temperature = 288.15 - 0.0065 * height
        c = np.sqrt(1.4 * 285.05 * temperature)
        return c

    else:
        return SPEED_OF_SOUND_IN_STRATOSPHERE