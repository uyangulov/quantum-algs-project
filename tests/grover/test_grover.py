import pytest
import numpy as np

from qiskit_wrapper import QiskitWrapperEmulator
from emulator import MyEmulator
from grover import SearchProblem, GroverCircuit
from statevector import StateVector

sqrt, log2, ceil, pi = np.sqrt, np.log2, np.ceil, np.pi

class TestGrover:

    @pytest.fixture
    def search_problem(self):
        """Fixture to create a SearchProblem instance."""
        return SearchProblem(N=8, marked=[6])
    
    @pytest.fixture
    def search_problem(self):
        """Fixture to create a SearchProblem instance."""
        return SearchProblem(N=8, marked=[1,2,3])
    
    @pytest.fixture
    def my_emulator(self):
        """Fixture to create a SearchProblem instance."""
        return MyEmulator()
    
    @pytest.fixture
    def qiskit_emulator(self):
        return QiskitWrapperEmulator()
    
    def test_inversion_circuit(self, my_emulator):
        """Test the oracle circuit output"""

        #iterate number of qubits
        for nq in range(1, 4):

            #create search problem instance
            sp = SearchProblem(N=2**nq, marked=[0])
            n = sp.num_qubits_required
            N = 2 ** n
            grover = GroverCircuit().from_search_problem(sp)
            circuit = grover.__make__reflection__circuit__(n)

            sv = my_emulator.apply_circuit(
                    circuit,
                    StateVector(list(np.ones(N)/np.sqrt(N)))
            ).vector

            #check correct phases are flipped
            compare = -np.ones(N) / np.sqrt(N)
            compare[0] = +1 / np.sqrt(N)
        
            assert np.allclose(sv, compare), "Oracle matrix does not match the expected transformation"


    def test_inversion_circuit_qiskit(self, qiskit_emulator):
        """Test the oracle circuit output"""

        #iterate number of qubits
        for nq in range(1, 4):

            #create search problem instance
            sp = SearchProblem(N=2**nq, marked=[0])
            n = sp.num_qubits_required
            N = 2 ** n
            grover = GroverCircuit().from_search_problem(sp)
            circuit = grover.__make__reflection__circuit__(n)

            sv = qiskit_emulator.apply_circuit(
                    circuit,
                    StateVector(list(np.ones(N)/np.sqrt(N)))
            ).vector

            #check correct phases are flipped
            compare = -np.ones(N) / np.sqrt(N)
            compare[0] = +1 / np.sqrt(N)
        
            assert np.allclose(sv, compare), "Oracle matrix does not match the expected transformation"

    def test_throughout_grover_test(self, my_emulator, search_problem):

        emu = MyEmulator()
        sp =  SearchProblem(N=8, marked=[1,2,7])
        gr = GroverCircuit()
        gr.from_search_problem(sp)

        n = sp.num_qubits_required
        print(n)
        N = 2**n
        grover = GroverCircuit().from_search_problem(sp)
        M = len(sp.marked_numbers)

        state_vector = StateVector(list(
            np.ones(N) / sqrt(N)
        ))

        n_iter = int(ceil(pi * sqrt(N) / 4)) + 10
        theta = 2 * np.arccos(sqrt(1-M/N))

        for k in range(1,n_iter):
            state_vector = emu.apply_circuit(grover, state_vector)
            for i, elem in enumerate(sp.marked_numbers):
                assert np.allclose(
                    np.sin(theta * (2 * k + 1) / 2),
                    M * state_vector[1] / sqrt(M))










