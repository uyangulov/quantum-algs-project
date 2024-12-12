import pytest
from circuit import QuantumCircuit, Gate
from qiskit import QuantumCircuit as QiskitQC, QuantumRegister as QiskitQReg
from qiskit.circuit.library import UnitaryGate
import numpy as np
from qiskit.quantum_info import Operator
from definitions import X as X_matrix, Y as Y_matrix


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


from generator import RandomCircuitGenerator

class TestQuantumCircuitDepth:
    """
    Test class for verifying the behavior of the QuantumCircuit depth
    method and comparison with Qiskit-generated circuit depth.
    """

    @pytest.fixture
    def empty_circuit(self):
        return QuantumCircuit()

    def test_single_gate(self):
        """Test for a single gate on a single qubit."""


        gate1 = Gate(qubit_indices=[0], matrix=IDENTITY2)
        circuit = QuantumCircuit([gate1])

        # Expected depth = 1 (since only one gate exists)
        assert circuit.depth == 1

        qiskit_circuit = circuit.to_qiskit()
        assert qiskit_circuit.depth() == 1  # One gate in Qiskit circuit

    def test_separate_qubit_gates(self):
        """Test for two gates on separate qubits."""
        gate1 = Gate(qubit_indices=[0], matrix=IDENTITY2)
        gate2 = Gate(qubit_indices=[1], matrix=IDENTITY2)
        circuit = QuantumCircuit([gate1, gate2])

        # Expected depth = 1 (both gates can be applied simultaneously)
        assert circuit.depth == 1
        qiskit_circuit = circuit.to_qiskit()
        assert qiskit_circuit.depth() == 1  # Two gates in Qiskit circuit

    def test_same_qubit_gates(self):
        """Test for two gates acting on the same qubit."""
        gate1 = Gate(qubit_indices=[0], matrix=IDENTITY2)
        gate2 = Gate(qubit_indices=[0], matrix=IDENTITY2)
        circuit = QuantumCircuit([gate1, gate2])

        # Expected depth = 2 (since gates act on the same qubit, they can't be applied in parallel)
        assert circuit.depth == 2
        qiskit_circuit = circuit.to_qiskit()
        assert qiskit_circuit.depth() == 2  # Two gates in Qiskit circuit

    def test_multiple_gate_layers(self):
        """Test for multiple gates with different qubit overlaps."""
        gate1 = Gate(qubit_indices=[0], matrix=IDENTITY2, name="Gate1")
        gate2 = Gate(qubit_indices=[1], matrix=IDENTITY2, name="Gate2")
        gate3 = Gate(qubit_indices=[2], matrix=IDENTITY2, name="Gate3")
        gate4 = Gate(qubit_indices=[0,1], matrix=IDENTITY4, name="Gate4")
        gate5 = Gate([1, 2], matrix=IDENTITY4, name="Gate5")
        circuit = QuantumCircuit([gate1, gate2, gate3, gate4, gate5])

        # Expected depth = 3 (since gates overlap and must be scheduled accordingly)
        assert circuit.depth == 3

        qiskit_circuit = circuit.to_qiskit()
        assert qiskit_circuit.depth() == 3  # Five gates in Qiskit circuit

    def test_no_gates(self, empty_circuit):
        assert empty_circuit.depth == 0
        assert empty_circuit.to_qiskit().depth() == 0

    def test_generated_circ(self):
        """Test circuit generated with Random Circuit Generator"""
        for n in range(0,100,20):
            gen = RandomCircuitGenerator(n,n,0.37)
            circ = gen.generate()
            qc = circ.to_qiskit()
            assert circ.depth == qc.depth(), "Depths mismatch"

    
# Define pytest test cases
class TestCompressionList:

    @pytest.fixture
    def circuit(self):
        gen = RandomCircuitGenerator(152,152,0.52)
        circ = gen.generate()
        return circ

    def test_no_qubit_reuse_in_layer(self, circuit):
        """Test there are no gates within same layer and acting on same qubit"""
        layers = circuit.compression_list()
        gates = circuit.gates

        for layer in layers:
            qubits_in_layer = [qubit_index for gate_index in layer for qubit_index in gates[gate_index].qubit_indices]
            assert len(set(qubits_in_layer)) == len(qubits_in_layer), f"Layer {layer} contains dupliate qubits"
    

    def test_all_gates_present(self, circuit):
        # Test case to ensure all gates are present in the layers
        layers = circuit.compression_list()
        gates = circuit.gates
        
        all_gate_indices = set(range(len(circuit.gates)))
        gate_indices_in_layers = {idx for layer in layers for idx in layer}
        
        assert all_gate_indices == gate_indices_in_layers, "Not all gates are included in the layers"

class TestQuantumCircuitFromQiskit:

    @pytest.fixture
    def qiskit_circuit(self):
        """Fixture to create a simple Qiskit quantum circuit."""
        qr = QiskitQReg(2)
        circ = QiskitQC(qr)
        circ.x(0)  # Apply X gate to qubit 0
        circ.y(1)  # Apply X gate to qubit 0
        return circ

    def test_from_qiskit_conversion(self, qiskit_circuit):
        """Test the conversion from Qiskit QuantumCircuit to custom QuantumCircuit."""
        # Create a custom QuantumCircuit instance
        custom_circuit = QuantumCircuit()

        # Convert the Qiskit circuit to custom format
        custom_circuit.from_qiskit(qiskit_circuit)

        # Check the number of gates in the custom circuit
        assert len(custom_circuit.gates) == 2, "Expected 2 gates in the custom circuit"

        # Verify the gates' qubit indices and operation types
        x_gate, h_gate = custom_circuit.gates

        assert x_gate.qubit_indices == [0], "X gate should act on qubit 0"
        assert h_gate.qubit_indices == [1], "H gate should act on qubit 1"
        
        # Further, verify gate matrices if necessary
        assert (x_gate.matrix == X_matrix).all(), "Matrix of X gate does not match"
        assert (h_gate.matrix == Y_matrix).all(), "Matrix of H gate does not match"
