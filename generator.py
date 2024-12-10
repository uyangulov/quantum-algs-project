from circuit import Gate, QuantumCircuit
from scipy import linalg
import numpy as np

class Randomizer:

    def __init__(self,
                 m=65537,
                 a=75,
                 c=74,
                 seed=27):
        
        self.a = a
        self.c = c
        self.m = m
        self.X = self.generate_initial_num(seed, n0 = 100)
    
    def generate_initial_num(self, seed, n0):
        X = seed
        for _ in range(n0):
            X = (self.a * X + self.c) % self.m
        return X

    def rand_int(self):
        self.X = (self.a * self.X + self.c) % self.m
        return self.X

    def rand(self, L=None):
        self.X = (self.a * self.X + self.c) % self.m
        return self.X / self.m if L is None else (self.X / self.m - 0.5) * 2 * L
    
    
class RandomCircuitGenerator:
    
    def __init__(self,
                 width: int,
                 depth: int,
                 weight2q: float,
                 seed: int = 27):
        
        self.width = width  # number of qubits
        self.depth = depth
        self.w = weight2q
        self.randomizer = Randomizer(seed=seed)
        
    def get_random_unitary(self, mode: str):
        
        assert mode in ['1q', '2q'], f"{mode} is not supported, only 1q or 2q"
        if mode == '1q':
            c = [self.randomizer.rand(L=100) for _ in range(4)]
            U = 1j * np.array([[c[0], c[1] + 1j * c[2]],
                               [c[1] - 1j * c[2], c[3]]])
            
            return linalg.expm(U)
        
        c = [self.randomizer.rand(L=100) for _ in range(16)]
        U = np.array([[c[0], c[1] + 1j*c[2], c[3] + 1j*c[4], c[5] + 1j*c[6]],
                      [c[1] - 1j*c[2], c[7], c[8] + 1j*c[9], c[10] + 1j*c[11]],
                      [c[3] - 1j*c[4], c[8] - 1j*c[9], c[12], c[13] + 1j*c[14]],
                      [c[5] - 1j*c[6], c[10] - 1j*c[11], c[13] - 1j*c[14], c[15]]]) * 1j
        
        return linalg.expm(U)
    
    def generate(self):
        
        qc = QuantumCircuit()
        
        for _ in range(self.depth):
            
            rand_num = self.randomizer.rand()
            
            if rand_num >= self.w or self.width == 1:      
                q = self.randomizer.rand_int() % self.width
                U = self.get_random_unitary(mode='1q')
                qc.append(Gate([q], U))
    
            else:
                q1 = self.randomizer.rand_int() % self.width
                q2 = self.randomizer.rand_int() % self.width
                while q2 == q1: 
                    q2 = self.randomizer.rand_int() % self.width
                    
                U = self.get_random_unitary(mode='2q')
                qc.append(Gate([q1, q2], U))
                
        return qc