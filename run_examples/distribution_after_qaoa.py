from qaoa import QAOA_MaxCut_Circuit
from scipy.optimize import minimize
import numpy as np
from emulator import MyEmulator
from statevector import StateVector
import matplotlib.pyplot as plt


edges = [(0,1), (1,2), (2,3), (3,0)]

def prepare_2_layer(x):
    beta1, beta2, gamma1, gamma2 = x
    qaoa_circ = QAOA_MaxCut_Circuit(num_qubits=4, edges=edges)
    qaoa_circ.add_layer(gamma1, beta1)
    qaoa_circ.add_layer(gamma2, beta2)
    return qaoa_circ

def expectation(x, backend):
    circ = prepare_2_layer(x)
    return circ.expectation_val(backend)

x0 = np.array([0.1, 0.1, 0.2, 0.3])
result = minimize(expectation, x0, args='MyEmulator', options={'maxiter':500}, method='powell')
print(result.x)
print(result.fun)

emu = MyEmulator()
opt_circ = prepare_2_layer(result.x)
num_qubits = opt_circ.num_qubits
vec = StateVector(num_qubits)
vec = emu.apply_circuit(opt_circ, vec)

print(vec.vector)

##  Square of the absolute value observation probability
probs = np.abs(vec.vector)**2
print(probs)

## a bit string which can be acquired from z axis projective measurement
z_basis = [format(i,"b").zfill(num_qubits) for i in range(probs.size)]

fig, ax = plt.subplots()
ax.set_xlabel("states")
ax.set_ylabel("probability(%)")
ax.bar(z_basis, probs*100)
plt.show()