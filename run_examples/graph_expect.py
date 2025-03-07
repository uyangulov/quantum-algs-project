from qaoa import QAOA_MaxCut_Circuit
from scipy.optimize import minimize
import numpy as np
from emulator import MyEmulator
from statevector import StateVector
import matplotlib.pyplot as plt

edges = [(0,1), (1,2), (2,3), (3,0)]

def prepare_3_layer(x):
    qaoa_circ = QAOA_MaxCut_Circuit(num_qubits=4, edges=edges)
    for i in range(0,6,2): 
        b, g = x[i], x[i]+1
        qaoa_circ.add_layer(g, b)
    return qaoa_circ

def expectation(x, backend = "MyEmulator", shots = None):
    circ = prepare_3_layer(x)
    return circ.expectation_val(backend, shots)

def get_probs(x):
    emu = MyEmulator()
    opt_circ = prepare_3_layer(x)
    vec = emu.apply_circuit(
        opt_circ,
        StateVector(opt_circ.num_qubits)
    )
    return np.abs(vec.vector)**2

n_iter = 30
"""
Honest expectation <Ψ|H|Ψ>
"""
expectations_honest = list()
probs_honest = list()
x = np.array([435, -344,52, 332,35,22])
for i in range(n_iter):

    result = minimize(expectation, x, 
                      args = ('MyEmulator', None), 
                      options={'maxiter': 1},
                      method='powell')
    x, fun = result.x, result.fun
    expectations_honest.append(fun)
    probs_honest.append(get_probs(x))

"""
Sumulated measurement <Ψ|H|Ψ>
"""
expectations_stat = list()
probs_stat = list()
shots = 1000
x = np.array([435, -344,52, 332,35,22])
for i in range(n_iter):

    result = minimize(expectation, x, 
                      args=('MyEmulator', shots),
                      options={'maxiter': 1},
                      method='powell')
    
    x, fun = result.x, result.fun
    expectations_stat.append(fun)
    probs_stat.append(get_probs(x))


fig, (ax, ax2, ax3) = plt.subplots(nrows=3, ncols=1, sharex=True, constrained_layout = True)

ax.set_ylabel("<Ψ|H|Ψ>")
ax.plot(expectations_stat, label = "Measurement statistic")
ax.plot(expectations_honest, label = "<Ψ|H|Ψ>")
#ax.set_xlabel("Iter")
ax.grid()
ax.legend()

N = len(probs_stat[0])
n = int(np.log2(N))
z_basis = [format(i,"b").zfill(n) for i in range(N)]

ax2.imshow(np.transpose(probs_stat), interpolation="hamming")
ax2.set_title("by statistic")
ax2.set_yticks(range(N), z_basis)
ax3.imshow(np.transpose(probs_honest), interpolation="hamming")
ax3.set_title("by <Ψ|H|Ψ>")
ax3.set_yticks(range(N), z_basis)

plt.show()
