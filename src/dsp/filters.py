import scipy as sp

class SoundFilters:

    def apply_lowPass(self, array, freq, order=4):
            normal_cutoff = freq / self.nyq
    
            b, a = sp.signal.butter(order, normal_cutoff, btype="low")
            y = sp.signal.filtfilt(b, a, array)
            return y

    
    def apply_bandPass(self, array, low_freq, high_freq, order=4):
        normal_cutoff = [low_freq / self.nyq, high_freq / self.nyq]
        
        b, a = sp.signal.butter(order, normal_cutoff, btype="band")
        y = sp.signal.filtfilt(b, a, array)
        return y
    
    
    def apply_highPass(self, array, freq, order=4):
        normal_cutoff = freq / self.nyq
    
        b, a = sp.signal.butter(order, normal_cutoff, btype="high")
        y = sp.signal.filtfilt(b, a, array)
        return y;