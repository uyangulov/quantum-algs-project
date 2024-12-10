import pytest
import numpy as np
from statevector import StateVector
from emulator import MyEmulator
from circuit import Gate
from abstract_emulator import OperandOutOfBoundsError

class TestMyEmulator:
    
    @pytest.fixture
    def emulator(self):
        return MyEmulator()  # Emulator instance for each test
    
    @pytest.fixture
    def state_vector_0(self):
        # |0⟩ state
        return StateVector([1,0])
    
    @pytest.fixture
    def state_vector_1(self):
        # |1⟩ state
        return StateVector([0,1])
  
    
    @pytest.fixture
    def pauli_x_gate(self):
        # Pauli-X (bit-flip) gate matrix
        matrix = np.array([[0, 1], [1, 0]])
        return Gate([0], matrix)
    
    @pytest.fixture
    def hadamard_gate(self):
        # Hadamard gate matrix
        matrix = np.array([[1/np.sqrt(2), 1/np.sqrt(2)], [1/np.sqrt(2), -1/np.sqrt(2)]])
        return Gate([0], matrix)
    
    def test_apply_pauli_x_gate_on_0(self, emulator, state_vector_0, pauli_x_gate):
        # Test applying Pauli-X (bit-flip) gate on |0⟩ state
        result = emulator.apply_gate(pauli_x_gate, state_vector_0)
        assert np.isclose(result[0], 0)  # After X, state should be |1⟩
        assert np.isclose(result[1], 1)

    def test_apply_pauli_x_gate_on_1(self, emulator, state_vector_1, pauli_x_gate):
        # Test applying Pauli-X (bit-flip) gate on |1⟩ state
        result = emulator.apply_gate(pauli_x_gate, state_vector_1)
        assert np.isclose(result[0], 1)  # After X, state should be |0⟩
        assert np.isclose(result[1], 0)
    
    def test_apply_hadamard_on_0(self, emulator, state_vector_0, hadamard_gate):
        # Test applying Hadamard gate on |0⟩ state
        result = emulator.apply_gate(hadamard_gate, state_vector_0)
        assert np.isclose(result[0], 1/np.sqrt(2))  # Hadamard transforms |0⟩ to (|0⟩ + |1⟩)/sqrt(2)
        assert np.isclose(result[1], 1/np.sqrt(2))
    
    def test_apply_hadamard_on_1(self, emulator, state_vector_1, hadamard_gate):
        # Test applying Hadamard gate on |1⟩ state
        result = emulator.apply_gate(hadamard_gate, state_vector_1)
        assert np.isclose(result[0], 1/np.sqrt(2))  # Hadamard transforms |1⟩ to (|0⟩ - |1⟩)/sqrt(2)
        assert np.isclose(result[1], -1/np.sqrt(2))
    
    def test_apply_gate_out_of_bounds(self, emulator, state_vector_0):
        # Test applying a gate with qubit indices out of bounds
        with pytest.raises(OperandOutOfBoundsError):
            # Using qubit index 1, which is out of bounds for a 1-qubit state vector
            invalid_gate = Gate([1], np.array([[0, 1], [1, 0]]))
            emulator.apply_gate(invalid_gate, state_vector_0)
    
    def test_apply_identity_gate(self, emulator, state_vector_0):
        # Identity gate (should not modify the state vector)
        identity_matrix = np.array([[1, 0], [0, 1]])
        identity_gate = Gate([0], identity_matrix)
        result = emulator.apply_gate(identity_gate, state_vector_0)
        assert result[0] == 1  # No change to state
        assert result[1] == 0