import numpy as np
import matplotlib.pyplot as plt

from emulator import MyEmulator
from grover import SearchProblem, GroverCircuit
from statevector import StateVector


sqrt, ceil, pi = np.sqrt, np.ceil, np.pi

def pretty_print_statevector(statevector):
    """
    Pretty-prints a vector of complex amplitudes with computational basis labels.

    Parameters:
    - statevector (Statevector or np.ndarray): The statevector to print.
    """
    n_qubits = int(np.log2(len(statevector)))
    for i, amplitude in enumerate(statevector):
        if not np.isclose(amplitude, 0):  # Skip near-zero amplitudes for clarity
            basis_state = format(i, f"0{n_qubits}b")  # Convert index to binary
            real_part = amplitude.real
            imag_part = amplitude.imag
            print(f"|{basis_state}>: {real_part:+.4f}{imag_part:+.4f}j")


emu = MyEmulator()
sp =  SearchProblem(N=1, marked=[0])
gr = GroverCircuit()
gr.from_search_problem(sp)

n = sp.num_qubits_required
print(n)
N = 2**n
grover = GroverCircuit().from_search_problem(sp)

state_vector = StateVector(list(
    np.ones(N) / sqrt(N)
))

n_iter = int(ceil(pi * sqrt(N) / 4)) + 1
print(n_iter)

comp = []
for k in range(1,n_iter):
    state_vector = emu.apply_circuit(grover, state_vector)
    comp.append(state_vector[0])

theta = 2 * np.arccos(np.sqrt(1 - 1/N))
rg = np.arange(1,n_iter,0.001)
theor = np.sin(theta * (2 * rg + 1) / 2)

plt.scatter(range(1,n_iter), comp, label = r'grover result')
plt.plot(rg, theor, label = r'sin($\frac{2k+1}{2} \theta$)' , ls = ":")
plt.legend(framealpha = 1)
plt.show()


