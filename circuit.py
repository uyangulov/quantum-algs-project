import numpy as np


import numpy as np

class Gate:
    """
    A class representing a quantum gate, including the qubit indices it operates on and the gate matrix.

    Attributes:
        name (str): The name of the gate, default is "custom".
        qubit_indices (list[int]): The list of qubit indices the gate acts on.
        matrix (np.ndarray): The matrix representation of the quantum gate.
        matrix_size (int): The size of the matrix, i.e., the number of rows/columns.

    Methods:
        qubit_indices(): Returns the list of qubit indices that the gate acts on.
        __repr__(): Returns a string representation of the Gate object.
    """

    def __init__(self, qubit_indices: list[int], matrix: np.ndarray, name: str = "custom"):
        """
        Initializes a quantum gate with the specified qubit indices and matrix.

        Args:
            qubit_indices (list[int]): The indices of the qubits this gate operates on.
            matrix (np.ndarray): A 2D numpy array representing the gate matrix.
            name (str, optional): The name of the gate. Default is "custom".

        Raises:
            ValueError: If the matrix is not square or its size doesn't match the expected number of qubits.
        """
        self.name = name

        # Number of qubits the gate acts upon
        n_qubits = len(qubit_indices)
        # Size of the matrix (both dimensions)
        matrix_size = matrix.shape[0]

        # Check that the matrix is square
        if matrix_size != matrix.shape[1]:
            raise ValueError("The gate matrix must be square (equal number of rows and columns).")

        # Check that the matrix dimension matches 2^n_qubits
        expected_size = 2 ** n_qubits
        if matrix_size != expected_size:
            raise ValueError(f"Matrix size mismatch: expected {expected_size}x{expected_size} "
                             f"for {n_qubits} qubits, but got {matrix_size}x{matrix_size}.")

        # Assign the gate's properties
        self.qubit_indices = qubit_indices
        self.matrix = matrix
        self.matrix_size = matrix_size


    def __repr__(self):
        """
        Returns a string representation of the Gate object, displaying the name and qubit indices.

        Returns:
            str: A formatted string representation of the Gate.
        """
        return f"Gate(name={self.name}, qubit_indices={self.qubit_indices}, matrix_size={self.matrix_size})"
        
        
class QuantumCircuit:
    
    """
    Class assumes qubits are labeled by integers from 0 to num_qubits - 1
    """
    def __init__(self,
                 num_qubits: int = 0,
                 gates: list[Gate] = []):
        
        for gate in gates:
            for qubit_idx in gate.qubit_indices:
                assert qubit_idx < num_qubits, f"List of gates requires >= {qubit_idx + 1} qubits, \
                                                 but only {num_qubits} are available"
        
        self.num_qubits = num_qubits
        self.gates = gates
        
    def append(self, 
               gate: Gate):
        self.gates.append(gate)
        mx = max(gate.qubit_indices)+1
        self.num_qubits = max(self.num_qubits, mx)

    def compression_list(self):

        qubit_to_current_layer = [0] * self.num_qubits
        layer_to_gate_indeces = []

        for i in range(len(self.gates)):

            gate = self.gates[i]
            qubit_indeces = gate.qubit_indices

            maximum_layer = max([qubit_to_current_layer[qubit_id] \
                                 for qubit_id in qubit_indeces])
            
            if maximum_layer >= len(layer_to_gate_indeces):
                layer_to_gate_indeces.append([])

            layer_to_gate_indeces[maximum_layer].append(i)
            
            for qubit_id in qubit_indeces:
                qubit_to_current_layer[qubit_id] = maximum_layer + 1

        return layer_to_gate_indeces

                



