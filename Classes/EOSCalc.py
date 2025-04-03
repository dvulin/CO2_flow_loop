import numpy as np

class EOSCalc:
    def __init__(self, components, T, P, z):
        self.components = components  # Kritični parametri komponenata
        self.T = T  # Temperatura u K
        self.P = P  # Tlak u bar
        self.z = np.array(z)  # Molarne frakcije smjese
        self.R = 8.314  # Plinska konstanta (J/(mol*K))
    
    def solve_eos(self):
        raise NotImplementedError("solve_eos must be implemented in subclass")
    
    def solve_phase_equilibrium(self):
        raise NotImplementedError("solve_phase_equilibrium must be implemented in subclass")