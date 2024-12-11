import pytest
import numpy as np
from statevector import StateVector
from circuit import Gate
from emulator import MyEmulator, OperandOutOfBoundsError
from defitions import CX, CY, CZ

class TestCustomOperators:

    @pytest.fixture
    def emulator(self):
        return MyEmulator()
    
    @pytest.fixture
    def one_qubit_state(self):
        # Initial 2-qubit state with distinct coefficients
        return StateVector(1)

    @pytest.fixture
    def two_qubit_state(self):
        # Initial 2-qubit state with distinct coefficients |00>, |10>, |01>, |11>
        return StateVector([0.6 + 0.2j, -0.3 + 0.1j, 0.4 - 0.5j, -0.2 + 0.7j])

    @pytest.fixture
    def three_qubit_state(self):
        # Initial 3-qubit state with distinct coefficients
        return StateVector([
            0.1 + 0.3j, -0.4 + 0.7j, 0.2 - 0.5j, 0.8 + 0.1j,
            -0.6 + 0.2j, 0.3 + 0.4j, -0.7 - 0.3j, 0.5 - 0.9j
        ])
    
    def test_one_qubit_input_throws(self, emulator, one_qubit_state):
        """Check for two-qubit gates emulator throws error on single qubit input"""
        with pytest.raises(OperandOutOfBoundsError):
            two_qubit_gate  = Gate([0,2], CX)
            emulator.apply_gate(two_qubit_gate, one_qubit_state)

    def test_apply_cx_gate(self, emulator, two_qubit_state):
        """Test applying CX gate (controlled-X) on a 2-qubit state."""
        cx_gate = Gate([0, 1], CX) 
        result = emulator.apply_gate(cx_gate, two_qubit_state)
        expected_result = two_qubit_state.vector.copy()
        #a|00> + b|10> + c|01> + d|11> ---> #a|00> + b|11> +  c|01> + d|10> == a|00> + d|10> + c|01> +  + b|11>
        #(a,b,c,d) -> (a,d,c,b)
        expected_result[1], expected_result[3] = expected_result[3], expected_result[1]
        assert np.allclose(result.vector, expected_result)

    def test_apply_cx_gate_rev(self, emulator, two_qubit_state):
        """Test applying CX reverse gate (controlled-X) on a 2-qubit state."""
        cx_gate = Gate([1, 0], CX) 
        result = emulator.apply_gate(cx_gate, two_qubit_state)
        expected_result = two_qubit_state.vector.copy()
        #a|00> + b|10> + c|01> + d|11> ---> #a|00> + b|10> + c|11> + d|01> = a|00> + b|10> + d|01> + c|11> 
        #(a,b,c,d) -> (a,b,d,c)
        expected_result[2], expected_result[3] = expected_result[3], expected_result[2]
        assert np.allclose(result.vector, expected_result)

    def test_apply_cy_gate(self, emulator, two_qubit_state):
        """Test applying CY gate (controlled-Y) on a 2-qubit state."""
        cy_gate = Gate([0, 1], CY) 
        result = emulator.apply_gate(cy_gate, two_qubit_state)
        expected_result = two_qubit_state.vector.copy()
        #a|00> + b|10> + c|01> + d|11> ---> #a|00> + ib|11> + c|01> - id|10>
        #(a,b,c,d) -> (a,-id,c,ib)
        expected_result[1], expected_result[3] = -1j * expected_result[3], 1j * expected_result[1]
        assert np.allclose(result.vector, expected_result)

    def test_apply_cy_gate_rev(self, emulator, two_qubit_state):
        """Test applying CY gate (controlled-Y) on a 2-qubit state."""
        cy_gate = Gate([1, 0], CY)  # Controlled-X gate on qubit 0 (control) and qubit 1 (target)
        result = emulator.apply_gate(cy_gate, two_qubit_state)
        expected_result = two_qubit_state.vector.copy()
        #a|00> + b|10> + c|01> + d|11> ---> a|00> + b|10> + ic|11> - id|01>
        #(a,b,c,d) -> (a,b,-id,+ic)
        expected_result[2], expected_result[3] = -1j * expected_result[3], 1j * expected_result[2]
        assert np.allclose(result.vector, expected_result)

    def test_invalid_qubit_index_throws_error(self, emulator, two_qubit_state):
        """Check that applying a 2-qubit gate to a state with an invalid qubit index raises an error."""
        with pytest.raises(OperandOutOfBoundsError):
            # Gate indices out of bounds for a 2-qubit state
            invalid_gate = Gate([0, 2], CX)  # Trying to apply a 2-qubit gate but on qubit 2 (doesn't exist in 2-qubit state)
            emulator.apply_gate(invalid_gate, two_qubit_state)

    def test_identity_gate_on_two_qubit_state(self, emulator, two_qubit_state):
        """Ensure applying an identity gate on a 2-qubit state leaves the state unchanged."""
        identity_gate = Gate([0, 1], np.eye(4))  # Identity gate on qubits 0 and 1 (4x4 identity matrix for 2-qubits)
        result = emulator.apply_gate(identity_gate, two_qubit_state)
        
        # Identity gate should leave the state unchanged
        assert np.allclose(result.vector, two_qubit_state.vector)

    def test_apply_cx_gate_multiple_times(self, emulator, two_qubit_state):
        """Test applying CX gate twice on a 2-qubit state results in the identity operation."""
        cx_gate = Gate([0, 1], CX)  # Apply CX gate twice
        result_first = emulator.apply_gate(cx_gate, two_qubit_state)
        result_second = emulator.apply_gate(cx_gate, result_first)  # Applying CX again should return to original state
        
        assert np.allclose(result_second.vector, two_qubit_state.vector)
