# reproduce well known results
# https://dojo.qulacs.org/en/latest/notebooks/5.3_quantum_approximate_optimazation_algorithm.html


from qaoa import QAOA_MaxCut_Circuit
from scipy.optimize import minimize
import numpy as np
import pytest

def expectation(x, backend: str):
    edges = [(0,1), (1,2), (2,3), (3,0)]
    gamma, beta = x
    qaoa_circ = QAOA_MaxCut_Circuit(num_qubits=4, edges=edges)
    qaoa_circ.add_layer(gamma,beta)
    for gate in qaoa_circ.gates:
        print(gate)
    print(qaoa_circ.num_qubits)
    return qaoa_circ.expectation_val(backend)

class TestQAOA:

    @pytest.fixture
    def atol(self):
        return 1e-3

    def test_my_emulator_expectation(self, atol):
        x0 = np.array( [0.1, 0.1 ])
        result = minimize(expectation, x0, args="MyEmulator", options={'maxiter':500}, method='powell')

        assert np.allclose(result.fun, -1, atol = atol), "value after optimization incorrect"
        assert np.allclose(result.x, [1.17809152, 0.39269362], atol = atol), "(beta, gamma) after optimization  incorrect" 

    def test_qiskit_expectation(self, atol):
        x0 = np.array( [0.1, 0.1 ])
        result = minimize(expectation, x0, args="Qiskit", options={'maxiter':500}, method='powell')

        assert np.allclose(result.fun, -1, atol = atol), "value after optimization incorrect"
        assert np.allclose(result.x, [1.17809152, 0.39269362], atol = atol), "(beta, gamma) after optimization  incorrect" 