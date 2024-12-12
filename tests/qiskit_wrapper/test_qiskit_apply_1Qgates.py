import pytest
import numpy as np
from statevector import StateVector
from qiskit_wrapper import QiskitWrapperEmulator
from circuit import Gate


# Pauli-X gate matrix
PAULI_X_MATRIX = np.array([[0, 1], 
                           [1, 0]])  

# Pauli-Y gate matrix
PAULI_Y_MATRIX = np.array([[0, -1j],
                           [1j, 0]])  

# Pauli-Z gate matrix
PAULI_Z_MATRIX = np.array([[1, 0],
                           [0, -1]])  

 # Hadamard gate matrix
HADAMARD_MATRIX = np.array([[1/np.sqrt(2), 1/np.sqrt(2)], 
                            [1/np.sqrt(2), -1/np.sqrt(2)]]) 

# T gate matrix
T_GATE_MATRIX = np.array([[1, 0], 
                          [0, np.exp(1j * np.pi / 4)]])  

# Example 2-qubit gate (CNOT gate)
CNOT_GATE_MATRIX = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
])

sqrt2 = np.sqrt(2)
sqrt6 = np.sqrt(6)

class TestSingleQubitInputs:

    @pytest.fixture
    def emulator(self):
        return QiskitWrapperEmulator()

    @pytest.fixture
    def single_qubit_0(self):
        return StateVector(1)  # |0⟩ state

    @pytest.fixture
    def single_qubit_1(self):
        return StateVector([0, 1])  # |1⟩ state

    @pytest.fixture
    def single_qubit_superposition(self):
        return StateVector([1 / np.sqrt(2), 1 / np.sqrt(2)])  # (|0⟩ + |1⟩)/√2

    @pytest.fixture
    def pauli_x_gate(self):
        return Gate([0], PAULI_X_MATRIX)  # Pauli-X gate

    @pytest.fixture
    def pauli_y_gate(self):
        return Gate([0], PAULI_Y_MATRIX)  # Pauli-Y gate

    @pytest.fixture
    def pauli_z_gate(self):
        return Gate([0],  PAULI_Z_MATRIX)  # Pauli-Z gate

    @pytest.fixture
    def hadamard_gate(self):
        return Gate([0], HADAMARD_MATRIX)  # Hadamard gate

    @pytest.fixture
    def t_gate(self):
        return Gate([0], T_GATE_MATRIX)  # T gate
    
    @pytest.fixture
    def two_qubit_gate(self):
        # Example of a 2-qubit gate (CNOT) which is invalid for a single-qubit state vector
        return Gate([0, 1], CNOT_GATE_MATRIX)


    def test_pauli_x(self, emulator, single_qubit_0, single_qubit_1, pauli_x_gate):
        assert np.allclose(emulator.apply_gate(pauli_x_gate, single_qubit_0).vector, [0, 1])
        assert np.allclose(emulator.apply_gate(pauli_x_gate, single_qubit_1).vector, [1, 0])

    def test_pauli_y(self, emulator, single_qubit_0, single_qubit_1, pauli_y_gate):
        assert np.allclose(emulator.apply_gate(pauli_y_gate, single_qubit_0).vector, [0, 1j])
        assert np.allclose(emulator.apply_gate(pauli_y_gate, single_qubit_1).vector, [-1j, 0])

    def test_pauli_z(self, emulator, single_qubit_0, single_qubit_1, pauli_z_gate):
        assert np.allclose(emulator.apply_gate(pauli_z_gate, single_qubit_0).vector, [1, 0])
        assert np.allclose(emulator.apply_gate(pauli_z_gate, single_qubit_1).vector, [0, -1])

    def test_hadamard(self, emulator, single_qubit_0, single_qubit_1, hadamard_gate):
        
        assert np.allclose(emulator.apply_gate(hadamard_gate, single_qubit_0).vector, [1 / sqrt2, 1 / sqrt2])
        assert np.allclose(emulator.apply_gate(hadamard_gate, single_qubit_1).vector, [1 / sqrt2, -1 / sqrt2])

    def test_t_gate(self, emulator, single_qubit_0, single_qubit_1, t_gate):
        t_phase = np.exp(1j * np.pi / 4)
        assert np.allclose(emulator.apply_gate(t_gate, single_qubit_0).vector, [1, 0])
        assert np.allclose(emulator.apply_gate(t_gate, single_qubit_1).vector, [0, t_phase])

    def test_superposition(self, emulator, single_qubit_superposition, pauli_z_gate):
        assert np.allclose(
            emulator.apply_gate(pauli_z_gate, single_qubit_superposition).vector,
            [1 / sqrt2, -1 / sqrt2]
        )

    def test_two_qubit_gate_throws(self, emulator, single_qubit_0, two_qubit_gate):
        with pytest.raises(Exception):
            emulator.apply_gate(two_qubit_gate, single_qubit_0)


class TestSingleQubitGates00State:
    
    @pytest.fixture
    def emulator(self):
        return QiskitWrapperEmulator()

    @pytest.fixture
    def two_qubit_00(self):
        return StateVector([1, 0, 0, 0])  # |00⟩ state

    def test_apply_pauli_x_first_qubit(self, emulator, two_qubit_00):
        pauli_x_gate_first = Gate([0], PAULI_X_MATRIX)  # Pauli-X gate on the first qubit
        result = emulator.apply_gate(pauli_x_gate_first, two_qubit_00)
        expected_result = [0, 1, 0, 0]  # Pauli-X on first qubit of |00⟩ -> |10⟩
        assert np.allclose(result.vector, expected_result)

    def test_apply_pauli_x_second_qubit(self, emulator, two_qubit_00):
        pauli_x_gate_second = Gate([1], PAULI_X_MATRIX)  # Pauli-X gate on the second qubit
        result = emulator.apply_gate(pauli_x_gate_second, two_qubit_00)
        expected_result = [0, 0, 1, 0]  # Pauli-X on second qubit of |00⟩ -> |01⟩
        assert np.allclose(result.vector, expected_result)

    def test_apply_pauli_y_first_qubit(self, emulator, two_qubit_00):
        pauli_y_gate_first = Gate([0], PAULI_Y_MATRIX)  # Pauli-Y gate on the first qubit
        result = emulator.apply_gate(pauli_y_gate_first, two_qubit_00)
        expected_result = [0, 1j, 0, 0]  # Pauli-Y on first qubit of |00⟩ -> i|10⟩
        assert np.allclose(result.vector, expected_result)

    def test_apply_pauli_y_second_qubit(self, emulator, two_qubit_00):
        pauli_y_gate_second = Gate([1], PAULI_Y_MATRIX)  # Pauli-Y gate on the second qubit
        result = emulator.apply_gate(pauli_y_gate_second, two_qubit_00)
        expected_result = [0, 0, 1j, 0]  # Pauli-Y on second qubit of |00⟩ -> i|01⟩
        assert np.allclose(result.vector, expected_result)

    def test_apply_pauli_z_first_qubit(self, emulator, two_qubit_00):
        pauli_z_gate_first = Gate([0], PAULI_Z_MATRIX)  # Pauli-Z gate on the first qubit
        result = emulator.apply_gate(pauli_z_gate_first, two_qubit_00)
        expected_result = [1, 0, 0, 0]  # Pauli-Z on first qubit of |00⟩ -> |00⟩
        assert np.allclose(result.vector, expected_result)

    def test_apply_pauli_z_second_qubit(self, emulator, two_qubit_00):
        pauli_z_gate_second = Gate([1], PAULI_Z_MATRIX)  # Pauli-Z gate on the second qubit
        result = emulator.apply_gate(pauli_z_gate_second, two_qubit_00)
        expected_result = [1, 0, 0, 0]  # Pauli-Z on second qubit of |00⟩ -> |00⟩
        assert np.allclose(result.vector, expected_result)

    def test_apply_t_first_qubit(self, emulator, two_qubit_00):
        t_gate_first = Gate([0], T_GATE_MATRIX)  # T gate on the first qubit
        result = emulator.apply_gate(t_gate_first, two_qubit_00)
        expected_result = [1, 0, 0, 0]  # T on first qubit of |00⟩ -> |00⟩
        assert np.allclose(result.vector, expected_result)

    def test_apply_t_second_qubit(self, emulator, two_qubit_00):
        t_gate_second = Gate([1], T_GATE_MATRIX)  # T gate on the second qubit
        result = emulator.apply_gate(t_gate_second, two_qubit_00)
        expected_result = [1, 0, 0, 0]  # T on second qubit of |00⟩ -> |00⟩
        assert np.allclose(result.vector, expected_result)



class TestSingleQubitGatesSuperposState:

    @pytest.fixture
    def emulator(self):
        return QiskitWrapperEmulator()

    @pytest.fixture
    def two_qubit_state(self):
        # superposition state:
        # (|00⟩ + 2|10⟩ + i|01⟩ - |11⟩)/√6
        return StateVector([1/sqrt6, 2/sqrt6, 1j/sqrt6, -1/sqrt6])
    
    def test_apply_pauli_x_first_qubit(self, emulator, two_qubit_state):
        pauli_x_gate_first = Gate([0], PAULI_X_MATRIX)  # Pauli-X on the first qubit
        result = emulator.apply_gate(pauli_x_gate_first, two_qubit_state)
        # (|10⟩ + 2|00⟩ + i|11⟩ - |01⟩)/√6
        expected_result = [2/sqrt6, 1/sqrt6, -1/sqrt6, 1j/sqrt6]  # Pauli-X on first qubit
        assert np.allclose(result.vector, expected_result)

    def test_apply_pauli_x_second_qubit(self, emulator, two_qubit_state):
        # (|01⟩ + 2|11⟩ + i|00⟩ - |10⟩)/√6
        pauli_x_gate_second = Gate([1], PAULI_X_MATRIX)  # Pauli-X on the second qubit
        result = emulator.apply_gate(pauli_x_gate_second, two_qubit_state)
        expected_result = [1j/sqrt6, -1/sqrt6, 1/sqrt6, 2/sqrt6]  # Pauli-X on second qubit
        assert np.allclose(result.vector, expected_result)

    def test_apply_pauli_y_first_qubit(self, emulator, two_qubit_state):
        # (i|10⟩ - 2i|00⟩ - |11⟩ + i|01⟩)/√6
        pauli_y_gate_first = Gate([0], PAULI_Y_MATRIX)  # Pauli-Y on the first qubit
        result = emulator.apply_gate(pauli_y_gate_first, two_qubit_state)
        expected_result = [-2j/sqrt6, 1j/sqrt6, +1j/sqrt6, -1/sqrt6]  # Pauli-Y on first qubit
        assert np.allclose(result.vector, expected_result)

    def test_apply_pauli_y_second_qubit(self, emulator, two_qubit_state):
        # (i|01⟩ + |00⟩ + 2i|11⟩ + i|10⟩)/√6
        pauli_y_gate_second = Gate([1], PAULI_Y_MATRIX)  # Pauli-Y on the second qubit
        result = emulator.apply_gate(pauli_y_gate_second, two_qubit_state)
        expected_result = [1/sqrt6, 1j/sqrt6, 1j/sqrt6, 2j/sqrt6]  # Pauli-Y on second qubit
        assert np.allclose(result.vector, expected_result)

    def test_apply_pauli_z_first_qubit(self, emulator, two_qubit_state):
        # (|00⟩ + i|01⟩ - 2|10⟩ + |11⟩)/√6
        pauli_z_gate_first = Gate([0], PAULI_Z_MATRIX)  # Pauli-Z on the first qubit
        result = emulator.apply_gate(pauli_z_gate_first, two_qubit_state)
        expected_result = [1/sqrt6, -2/sqrt6, 1j/sqrt6, 1/sqrt6]  # Pauli-Z on first qubit
        assert np.allclose(result.vector, expected_result)

    def test_apply_pauli_z_second_qubit(self, emulator, two_qubit_state):
        # (|00⟩ - i|01⟩ + 2|10⟩ + |11⟩)/√6
        pauli_z_gate_second = Gate([1], PAULI_Z_MATRIX)  # Pauli-Z on the second qubit
        result = emulator.apply_gate(pauli_z_gate_second, two_qubit_state)
        expected_result = [1/sqrt6, 2/sqrt6, -1j/sqrt6, 1/sqrt6]  # Pauli-Z on second qubit
        assert np.allclose(result.vector, expected_result)
