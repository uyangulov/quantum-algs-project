import pytest
import numpy as np
from math import floor, log2
from grover import SearchProblem
from statevector import StateVector
from emulator import MyEmulator
from itertools import product

class TestSearchProblem:

    @pytest.fixture
    def search_problem(self):
        """Fixture to create a SearchProblem instance."""
        return SearchProblem(N=8, marked=[3, 5])
    
    @pytest.fixture
    def search_problem_1q(self):
        """Fixture to create a SearchProblem instance."""
        return SearchProblem(N=1, marked=[0])
    
    @pytest.fixture
    def emulator(self):
        """Fixture to create a SearchProblem instance."""
        return MyEmulator()


    def test_num_qubits_required(self):
        """Test edge cases for the number of qubits required."""
        # Test for N = 1 (should require 1 qubit)
        sp = SearchProblem(N=1, marked=[0])
        assert sp.num_qubits_required == 1, f"Expected 1 qubit for N = {sp.size}"

        # Test for N = 2 (should require 2 qubits)
        sp = SearchProblem(N=2, marked=[0, 1])
        assert sp.num_qubits_required == 2, f"Expected 2 qubits for N = {sp.size}"

        # Test for N = 16 (should require 4 qubits)
        sp = SearchProblem(N=16, marked=[1, 3, 7, 15])
        assert sp.num_qubits_required == 5, f"Expected 5 qubits for N = {sp.size}"

    def test_invalid_marked_numbers(self):
        """Test for invalid marked numbers (greater than or equal to N)."""
        with pytest.raises(ValueError):
            SearchProblem(N=8, marked=[10])  # 10 is larger than or equal to N (8)

        with pytest.raises(ValueError):
            SearchProblem(N=2, marked=[2])  # 2 is equal to N (2)

        with pytest.raises(ValueError):
            SearchProblem(N=2, marked=[-1])  # negative input


    
    def test_oracle_circuit(self, emulator):
        """Test the oracle circuit output"""

        #iterate number of qubits
        for nq in range(1, 4):

            #iterate all possible marked answers
            for triplet in product([0,1], repeat=nq):

                #create search problem instance
                sp = SearchProblem(N=2**nq, marked=[*triplet])
                N = 2 ** sp.num_qubits_required
                circuit = sp.oracle_circuit()

                #flips signs by oracle
                sv = emulator.apply_circuit(
                    circuit,
                    StateVector(list(np.ones(N)/np.sqrt(N)))
                ).vector

                #check correct phases are flipped
                compare = np.ones(N) / np.sqrt(N)
                compare[sp.marked_numbers] = -1 / np.sqrt(N)
            
                assert np.allclose(sv, compare), "Oracle matrix does not match the expected transformation"


        
