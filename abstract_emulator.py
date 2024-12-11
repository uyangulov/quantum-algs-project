from abc import ABC, abstractmethod
from circuit import Gate, QuantumCircuit
from statevector import StateVector

class UnsupportedNumberOfQubits(ValueError):
    """
    Exception raised when the number of operands exceeds the allowed limit.
    """
    def __init__(self, gate: Gate):
        
        self.max_operands = 2
        self.message = \
            f"Operation '{gate.name}' received {len(gate.qubit_indices)} qubits, but a maximum of {self.max_operands} is supported. \
              Try decomposing the gate."
        
        super().__init__(self.message)

class OperandOutOfBoundsError(IndexError):
    """
    Exception raised when an operation accesses out-of-bounds indices in a state.
    """
    def __init__(self, 
                 gate: Gate,
                 size: int):

        self.message = \
            f"Operation '{gate.name}' attempted to access indices {gate.qubit_indices} on a register of size {size}."
        
        super().__init__(self.message)



class AbstractEmulator(ABC):

    @abstractmethod
    def apply_gate(self,
                   gate: Gate,
                   state_vector: StateVector):
        """
        Apply gate to given state vector.

        Args:
            gate: A gate to apply
            state_vector: An operand
            inplace: whether to modify input state vector

        Returns:
            New statevector

        Raises:
            OperandOutOfBoundsError: if gate tries to act on qubits not present in state_vector
        """
        pass

    @abstractmethod
    def apply_circuit(self,
               circuit: QuantumCircuit,
               state_vector: StateVector):
        
        """
        Apply quantum circuit to given state vector.

        Args:
            circuit: A circuit to apply
            state_vector: An operand
            inplace: whether to modify input state vector

        Returns:
            New statevector
        """
        pass
