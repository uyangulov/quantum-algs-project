from abstract_emulator import AbstractEmulator
from circuit import QuantumCircuit, Gate
from statevector import StateVector
from qiskit.circuit.library import UnitaryGate as QiskitUnitaryGate

class QiskitWrapperEmulator(AbstractEmulator):
    """
    QiskitWrapperEmulator is a wrapper class that enables the application of quantum circuits 
    and quantum gates to quantum state vectors using Qiskit. 
    
    Attributes:
        None directly, as this class does not hold state itself.
    
    Methods:
        apply_circuit(circuit: QuantumCircuit, input_vector: StateVector) -> StateVector:
            Applies a given quantum circuit to an input quantum state vector using Qiskit's statevector simulator.
        
        apply_gate(gate: Gate, input_vector: StateVector) -> StateVector:
            Applies a single quantum gate to an input quantum state vector using Qiskit's statevector simulator.
    """
    
    def apply_circuit(self, 
                      circuit: QuantumCircuit,
                      input_vector: StateVector):
        """
        Applies the given quantum circuit to the input state vector.

        Args:
            circuit (QuantumCircuit): The quantum circuit to be applied to the state vector.
            input_vector (StateVector): The input state vector to which the quantum circuit will be applied.

        Returns:
            StateVector: The resulting quantum state vector after applying the circuit.
        
        This method converts the provided `QuantumCircuit` and `StateVector` into their Qiskit equivalents, 
        evolves the state using the Qiskit statevector simulator, and returns the modified state as a new `StateVector`.
        """
        qiskit_circuit = circuit.to_qiskit()
        qiskit_state_vector = input_vector.to_qiskit()
        qiskit_modified = qiskit_state_vector.evolve(qiskit_circuit)
        output = StateVector(qiskit_modified.data.tolist())
        return output
    
    def apply_gate(self,
                   gate: Gate,
                   input_vector: StateVector):
        """
        Applies a single quantum gate to the input state vector.

        Args:
            gate (Gate): The quantum gate to be applied. This should contain the matrix representation
                         of the gate and the qubit indices to apply it on.
            input_vector (StateVector): The input state vector to which the quantum gate will be applied.

        Returns:
            StateVector: The resulting quantum state vector after applying the gate.
        
        This method converts the provided `Gate` and `StateVector` into their Qiskit equivalents, 
        evolves the state using the Qiskit statevector simulator, and returns the modified state as a new `StateVector`.
        """
        qiskit_state_vector = input_vector.to_qiskit()
        qiskit_gate = QiskitUnitaryGate(gate.matrix, label=gate.name)
        qiskit_evolved = qiskit_state_vector.evolve(qiskit_gate, qargs=gate.qubit_indices)
        output = StateVector(qiskit_evolved.data.tolist())
        return output

        