import pytest
from circuit import QuantumCircuit, Gate
from qiskit import QuantumCircuit as QiskitQC
from qiskit.circuit.library import UnitaryGate
import numpy as np

IDENTITY2 = np.eye(2)
IDENTITY4 = np.eye(4)  

class TestQuantumCircuit:

    @pytest.fixture
    def circuit_with_gates(self):
        """Fixture to create a QuantumCircuit with some gates."""
        gate1 = Gate([0], IDENTITY2, name="first")  # Identity gate on qubit 0
        gate2 = Gate([1, 2], IDENTITY4, name="second")  # CNOT gate on qubits 1 and 2
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
        gate3 = Gate([100, 101], IDENTITY4)  # Gate on qubits 3 and 4
        circuit = circuit_with_gates
        circuit.append(gate3)
        assert len(circuit.gates) == 3
        assert circuit.num_qubits == 102

    def test_num_non_idle_qubits(self, circuit_with_gates):
        """Test appending a gate increases the number of qubits if necessary."""
        gate3 = Gate([100, 101], IDENTITY4)  # Gate on qubits 3 and 4
        circuit = circuit_with_gates
        circuit.append(gate3)
        assert len(circuit.gates) == 3
        assert circuit.num_non_idle_qubits == 5

    def test_num_qubits_with_no_gates(self):
        """Test that the number of qubits is 0 when no gates are present."""
        circuit = QuantumCircuit()
        assert circuit.num_qubits == 0

    def test_to_qiskit(self, circuit_with_gates):
        """Test to_qiskit convertation method"""
        converted = circuit_with_gates.to_qiskit()
        expected_circuit = QiskitQC(3)
        expected_circuit.append(UnitaryGate(IDENTITY2, label="first"), [0])
        expected_circuit.append(UnitaryGate(IDENTITY4, label="second"), [1,2])

        # Compare the Qiskit circuits
        assert converted == expected_circuit  # Assert that the circuits are the same



# class TestQuantumCircuitToQiskit:

#     def create_custom_circuit(self):
#         """Create a custom quantum circuit using our QuantumCircuit implementation."""
#         gates = [
#             Gate(qubit_indices=[0], matrix=IDENTITY2),  # Identity gate on qubit 0
#             Gate(qubit_indices=[1], matrix=IDENTITY2),  # Identity gate on qubit 1
#             Gate(qubit_indices=[0, 1], matrix=IDENTITY4),  # Gate on qubits 0 and 1
#         ]
#         return CustomQuantumCircuit(gates)

#     def convert_to_qiskit(self, custom_circuit):
#         """Convert a custom quantum circuit to a Qiskit quantum circuit."""
#         num_qubits = custom_circuit.num_qubits
#         qiskit_circuit = QiskitQuantumCircuit(num_qubits)

#         # Iterate over the custom circuit's gates and map to Qiskit gates
#         for gate in custom_circuit.gates:
#             if gate.num_qubits == 1: # Single qubit gate (identity in this case)
#                 qubit = gate.qubit_indeces[0]
#                 qiskit_circuit.id(qubit)
#             elif gate.num_qubits == 2:
#                 qubits = gate.qubit_indices
#                     qiskit_circuit.id(qubits[0])
#                     qiskit_circuit.id(qubits[1])
#                 else:
#                     # For the sake of this example, using a CNOT gate as a placeholder for any 2-qubit operation
#                     qiskit_circuit.cx(qubits[0], qubits[1])

#         return qiskit_circuit

#     def test_comparison_with_qiskit_conversion(self):
#         """Test that the converted Qiskit circuit has the same depth as the custom circuit."""
#         # Create custom quantum circuit
#         custom_circuit = self.create_custom_circuit()

#         # Convert custom circuit to Qiskit
#         qiskit_circuit = self.convert_to_qiskit(custom_circuit)

#         # Get the depth of the custom circuit (from compression list)
#         custom_compression_list = custom_circuit.compression_list()
#         custom_depth = len(custom_compression_list)

#         # Get the depth of the Qiskit circuit
#         qiskit_depth = qiskit_circuit.depth()

#         # Assert the depths match
#         assert custom_depth == qiskit_depth, (
#             f"Depth mismatch: custom depth = {custom_depth}, Qiskit depth = {qiskit_depth}"
#         )