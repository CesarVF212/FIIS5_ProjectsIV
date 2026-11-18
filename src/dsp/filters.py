import scipy as sp
import numpy as np

class SoundFilters:

    def apply_lowPass(self, array, freq, order=4):
        normal_cutoff = freq / self.nyq

        b, a = sp.signal.butter(order, normal_cutoff, btype="low")
        y = sp.signal.filtfilt(b, a, array)
        return y

    
    def apply_peaking_eq(self, array, freq, gain_db, Q=1.0):
        w0 = 2 * np.pi * (freq / self.nyq)
        
        alpha = np.sin(w0) / (2 * Q)
        A = 10.0 ** (gain_db / 40.0) 

        # Coeficients.
        b0 = 1 + alpha * A
        b1 = -2 * np.cos(w0)
        b2 = 1 - alpha * A
        
        a0 = 1 + alpha / A
        a1 = -2 * np.cos(w0)
        a2 = 1 - alpha / A

        # Normalization.
        b = np.array([b0, b1, b2]) / a0
        a = np.array([a0, a1, a2]) / a0

        y = sp.signal.filtfilt(b, a, array)
        return y
    
    
    def apply_highPass(self, array, freq, order=4):
        normal_cutoff = freq / self.nyq
    
        b, a = sp.signal.butter(order, normal_cutoff, btype="high")
        y = sp.signal.filtfilt(b, a, array)
        return y;