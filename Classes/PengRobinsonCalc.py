import numpy as np
import EOSCalc
from scipy.optimize import fsolve


class PengRobinsonCalc(EOSCalc):
    def __init__(self, components, T, P, z):
        super().__init__(components, T, P, z)
        
        # Izračunavanje EOS parametara
        self.a_vals, self.b_vals = zip(*[self.peng_robinson_params(T, comp) for comp in components.values()])
        self.a_vals, self.b_vals = np.array(self.a_vals), np.array(self.b_vals)
        self.a_mix = np.sum(np.outer(self.z, self.z) * np.sqrt(np.outer(self.a_vals, self.a_vals)))
        self.b_mix = np.sum(self.z * self.b_vals)
    
    def peng_robinson_params(self, T, comp):
        Tc, Pc, omega = comp["Tc"], comp["Pc"], comp["omega"]
        Tr = T / Tc
        a = 0.45724 * (self.R**2 * Tc**2) / Pc
        b = 0.07780 * (self.R * Tc) / Pc
        m = 0.37464 + 1.54226 * omega - 0.26992 * omega**2
        alpha = (1 + m * (1 - np.sqrt(Tr)))**2
        return a * alpha, b

    def peng_robinson_eos(self, V):
        return self.P - (self.R * self.T) / (V - self.b_mix) + (self.a_mix / (V**2 + 2 * self.b_mix * V - self.b_mix**2))
    
    def solve_eos(self):
        V_guess = self.R * self.T / self.P
        V_solution = fsolve(self.peng_robinson_eos, V_guess)
        return V_solution[0]

    def compute_k_factors(self, V):
        phi_L = np.exp((self.b_vals / self.b_mix) * (self.P * (V - self.b_mix) / (self.R * self.T) - 1))
        phi_V = np.exp(-np.log(self.P * (V - self.b_mix) / (self.R * self.T)))
        return phi_L / phi_V
    
    def rachford_rice(self, v):
        return np.sum(self.z * (self.K - 1) / (1 + v * (self.K - 1)))
    
    def solve_phase_equilibrium(self):
        V = self.solve_eos()
        self.K = self.compute_k_factors(V)
        v_solution = fsolve(self.rachford_rice, 0.5)
        v = v_solution[0]
        y = self.K * self.z / (1 + v * (self.K - 1))
        x = self.z / (1 + v * (self.K - 1))
        return {"vapor_fraction": v, "gas_composition": y.tolist(), "liquid_composition": x.tolist()}