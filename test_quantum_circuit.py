import pytest
from circuit import QuantumCircuit, Gate
import numpy as np

CNOT_GATE_MATRIX = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
])

class TestQuantumCircuit:


    @pytest.fixture
    def circuit_with_gates(self):
        """Fixture to create a QuantumCircuit with some gates."""
        gate1 = Gate([0], np.array([[1, 0], [0, 1]]))  # Identity gate on qubit 0
        gate2 = Gate([1, 2], CNOT_GATE_MATRIX)  # CNOT gate on qubits 1 and 2
        return QuantumCircuit([gate1, gate2])


    def test_initialization(self):
        """Test initialization of QuantumCircuit with no gates."""
        circuit = QuantumCircuit()
        assert circuit.gates == []
        assert circuit.num_qubits == 0

    def test_initialization_with_gates(self, circuit_with_gates):
        """Test initialization of QuantumCircuit with a list of gates."""
        circuit = circuit_with_gates
        assert len(circuit.gates) == 2
        assert circuit.num_qubits == 3

    def test_append_gate(self):
        """Test appending a new gate to the circuit."""
        gate1 = Gate([0], np.array([[1, 0], [0, 1]]))  # Identity gate
        gate2 = Gate([1], np.array([[0, 1], [1, 0]]))  # Pauli-X gate
        circuit = QuantumCircuit()
        circuit.append(gate1)
        circuit.append(gate2)
        assert len(circuit.gates) == 2
        assert circuit.num_qubits == 2

    def test_append_gate_increases_qubits(self, circuit_with_gates):
        """Test appending a gate increases the number of qubits if necessary."""
        gate3 = Gate([100, 101], CNOT_GATE_MATRIX)  # Gate on qubits 3 and 4
        circuit = circuit_with_gates
        circuit.append(gate3)
        assert len(circuit.gates) == 3
        assert circuit.num_qubits == 102

    def test_num_non_idle_qubits(self, circuit_with_gates):
        """Test appending a gate increases the number of qubits if necessary."""
        gate3 = Gate([100, 101], CNOT_GATE_MATRIX)  # Gate on qubits 3 and 4
        circuit = circuit_with_gates
        circuit.append(gate3)
        assert len(circuit.gates) == 3
        assert circuit.num_non_idle_qubits == 5

    def test_num_qubits_with_no_gates(self):
        """Test that the number of qubits is 0 when no gates are present."""
        circuit = QuantumCircuit()
        assert circuit.num_qubits == 0
