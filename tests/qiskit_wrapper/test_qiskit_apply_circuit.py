import pytest
import numpy as np
from statevector import StateVector
from circuit import Gate, QuantumCircuit
from qiskit_wrapper import QiskitWrapperEmulator
from definitions import X, CX


class TestApplyCircuit:

    @pytest.fixture
    def emulator(self):
        # Create an instance of the emulator for testing
        return QiskitWrapperEmulator()

    @pytest.fixture
    def single_qubit_state(self):
        return StateVector(1)  # State |0>

    @pytest.fixture
    def two_qubit_state(self):
        return StateVector(2)  # State |00>

    @pytest.fixture
    def x_gate(self):
        # Create a Pauli-X (NOT) gate for single-qubit
        return Gate([0], X)

    @pytest.fixture
    def cnot_gate(self):
        # Create a CNOT gate with qubit 0 as control and qubit 1 as target
        return Gate([0, 1], CX)

    def test_single_qubit_gate(self, emulator, single_qubit_state, x_gate):
        """Test applying a single-qubit gate (X gate) to a single-qubit state |0>."""
        # Create a simple quantum circuit with 1 qubit
        circuit = QuantumCircuit()
        circuit.append(x_gate)  # Apply the X gate

        # Apply the circuit to the initial state |0>
        output = emulator.apply_circuit(circuit, single_qubit_state)

        # Expected output should be |1> after applying X
        expected = StateVector([0, 1])

        # Check if the result matches the expected state vector
        assert np.allclose(output.vector, expected.vector), f"Expected {expected.vector}, but got {output.vector}"

    def test_two_qubit_gate(self, emulator, two_qubit_state, cnot_gate):
        """Test applying a two-qubit gate (CNOT gate) on a 2-qubit state |00>."""
        # Create a quantum circuit with 2 qubits
        circuit = QuantumCircuit()
        circuit.append(cnot_gate)  # Apply the CNOT gate

        # Apply the circuit to the initial state |00>
        output = emulator.apply_circuit(circuit, two_qubit_state)

        # After applying the CNOT gate, the state should remain |00>
        expected = StateVector([1, 0, 0, 0])

        # Check if the result matches the expected state vector
        assert np.allclose(output.vector, expected.vector), f"Expected {expected.vector}, but got {output.vector}"

    def test_cx_gate_multiple_times(self, emulator, two_qubit_state, cnot_gate):
        """Test applying CX gate twice on a 2-qubit state results in the identity operation."""
        # Apply the CNOT gate once
        result_first = emulator.apply_gate(cnot_gate, two_qubit_state)
        
        # Apply the CNOT gate again on the resulting state
        result_second = emulator.apply_gate(cnot_gate, result_first)
        
        # The second application should return the state to the original state
        assert np.allclose(result_second.vector, two_qubit_state.vector), f"Expected {two_qubit_state.vector}, but got {result_second.vector}"

    def test_single_qubit_circuit(self, emulator, single_qubit_state, x_gate):
        """Test applying a single-qubit gate (X gate) in a simple circuit."""
        # Create a circuit with 1 qubit and apply the X gate
        circuit = QuantumCircuit()
        circuit.append(x_gate)

        # Apply the circuit to the state |0>
        output = emulator.apply_circuit(circuit, single_qubit_state)

        # After applying X, the state should be |1>
        expected = StateVector([0, 1])
        assert np.allclose(output.vector, expected.vector), f"Expected {expected.vector}, but got {output.vector}"

    def test_two_qubit_circuit(self, emulator, two_qubit_state, cnot_gate):
        """Test applying a two-qubit gate (CNOT gate) in a simple two-qubit circuit."""
        # Create a circuit with 2 qubits
        circuit = QuantumCircuit()
        circuit.append(cnot_gate)

        # Apply the circuit to the state |00>
        output = emulator.apply_circuit(circuit, two_qubit_state)

        # The state should remain |00> after applying the CNOT gate
        expected = StateVector([1, 0, 0, 0])
        assert np.allclose(output.vector, expected.vector), f"Expected {expected.vector}, but got {output.vector}"

