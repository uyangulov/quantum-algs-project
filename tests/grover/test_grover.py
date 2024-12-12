import pytest
import numpy as np

from qiskit_wrapper import QiskitWrapperEmulator
from emulator import MyEmulator
from grover import SearchProblem, GroverCircuit
from statevector import StateVector


class TestGrover:

    @pytest.fixture
    def search_problem(self):
        """Fixture to create a SearchProblem instance."""
        return SearchProblem(N=8, marked=[6])
    
    @pytest.fixture
    def my_emulator(self):
        """Fixture to create a SearchProblem instance."""
        return MyEmulator()
    
    @pytest.fixture
    def qiskit_emulator(self):
        return QiskitWrapperEmulator()
    
    # def test_grover_my_emulator(self, search_problem, my_emulator):

    #     num_qubits = search_problem.num_qubits_required
    #     N = 2**num_qubits
    #     n_iter = 100
    #     circuit = GroverCircuit().from_search_problem(search_problem)
    #     state_vector = StateVector(list(np.ones(N)/np.sqrt(N)))

    #     for k in range(1, n_iter):
    #         state_vector = my_emulator.apply_ci

    #     theta = 2 * np.arccos(np.sqrt(1 - 1/N))

    def test_grover_my_emulator(self, search_problem, my_emulator):

        num_qubits = search_problem.num_qubits_required
        N = 2**num_qubits
        circuit = GroverCircuit().__make__reflection__circuit__(num_qubits)

        sv = my_emulator.apply_circuit(
            circuit,
            StateVector(list(np.ones(2**N)/np.sqrt(N)))
        ).vector

