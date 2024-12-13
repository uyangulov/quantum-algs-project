from qaoa import QAOA_MaxCut_Circuit
from scipy.optimize import minimize
import numpy as np

edges = [(0,1), (1,2), (2,3), (3,0)]

def expectation(x):
    gamma, beta = x
    qaoa_circ = QAOA_MaxCut_Circuit(num_qubits=4, edges=edges)
    qaoa_circ.add_layer(gamma,beta)
    for gate in qaoa_circ.gates:
        print(gate)
    print(qaoa_circ.num_qubits)
    return qaoa_circ.expectation_val("Qiskit")


x0 = np.array( [0.1, 0.1 ])
result = minimize(expectation, x0, options={'maxiter':500}, method='powell')
print(result.fun) # value after optimization
print(result.x) # (beta, gamma) after optimization