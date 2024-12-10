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
                   state_vector: StateVector,
                   inplace: bool = False):
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

    # @abstractmethod
    # def apply_gate_selfstate(self,
    #                gate: Gate,
    #                inplace: bool = False):
    #     """
    #     Apply gate to member state vector.

    #     Args:
    #         gate: A gate to apply
    #         inplace: whether to modify member state vector

    #     Returns:
    #         New statevector

    #     Raises:
    #         OperandOutOfBoundsError: if gate tries to act on qubits not present in state_vector
    #     """
    #     pass


    # @abstractmethod
    # def apply_circuit(self,
    #            circuit: QuantumCircuit,
    #            state_vector: StateVector,
    #            inplace: bool = False):
        
    #     """
    #     Apply quantum circuit to given state vector.

    #     Args:
    #         circuit: A circuit to apply
    #         state_vector: An operand
    #         inplace: whether to modify input state vector

    #     Returns:
    #         New statevector
    #     """
    #     pass
    
    # @abstractmethod
    # def apply_circuit_selfstate(self,
    #               circuit: QuantumCircuit,
    #               inplace: bool = False):
    #     """
    #     Apply quantum circuit to member state vector

    #     Args:
    #         circuit: A circuit to apply
    #         state_vector: An operand
    #         inplace: whether to modify input state vector

    #     Returns:
    #         New statevector
    #     """
    #     pass