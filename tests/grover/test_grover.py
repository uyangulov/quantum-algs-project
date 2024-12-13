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
