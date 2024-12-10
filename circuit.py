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
    A class to represent a quantum circuit consisting of qubits and gates.

    This class allows for the creation of a quantum circuit, where qubits are labeled
    from 0 to num_qubits-1. Gates can be appended to the circuit, and the circuit 
    structure can be analyzed in terms of the layers required to execute the gates on qubits.

    Attributes:
    gates (list): A list of Gate objects representing the gates applied to the circuit.
    
    Methods:
    __init__(gates: list[Gate]):
        Initializes the quantum circuit with a list of gates. The number of qubits
        is automatically determined based on the gates provided.

    append(gate: Gate):
        Appends a gate to the quantum circuit, adjusting the number of qubits if necessary.

    compression_list():
        Generates a list of gate layers that represent the layers of gates that can be applied
        simultaneously. Each layer contains the indices of the gates that can be applied
        to the qubits simultaneously, ensuring that no two gates in the same layer act on the
        same qubit.

    num_qubits (property):
        The number of qubits in the quantum circuit. (Maximum index of qubit + 1)

    depth (property):
        The number of layers (depth) in the quantum circuit, representing the maximum number
        of sequential layers of gates that can be applied.

    Notes:
    - The `gates` argument should be a list of Gate objects

    """

    def __init__(self, gates: list[Gate] = None):

        if gates is None:
            self.gates = []  # Create a new list for each instance
        else:
            self.gates = gates
        
    @property
    def num_qubits(self):
        """
        Returns the number of qubits in the quantum circuit. This is dynamically calculated
        based on the gates applied in the circuit.

        Returns:
        int: The number of qubits in the quantum circuit.
        """
        if self.gates:
            return max((max(gate.qubit_indices) for gate in self.gates), default=0) + 1
        
        #empty list
        return 0
    
    @property
    def num_non_idle_qubits(self):
        """
        Returns the number of non-idle qubits in the quantum circuit. 

        Returns:
        int: The number of qubits in the quantum circuit.
        """
        unique_qubits = {qubit for gate in self.gates for qubit in gate.qubit_indices}
        return len(unique_qubits)
        

    @property
    def depth(self):
        """
        Returns the depth (number of layers) of the quantum circuit, representing the maximum
        number of sequential layers of gates that can be applied to the qubits.

        The depth is determined by finding the maximum layer index from the compression list of gates.

        Returns:
        int: The number of layers in the quantum circuit.
        """
        return len(self.compression_list())

    def append(self, gate: Gate):
        """
        Appends a gate to the quantum circuit, adjusting the number of qubits if necessary.

        Args:
        gate (Gate): A Gate object representing the gate to be added to the circuit.
        """
        self.gates.append(gate)

    def compression_list(self):
        """
        Generates a list of gate layers representing the gates that can be applied simultaneously.

        Each layer contains the indices of the gates that can be applied to the qubits simultaneously,
        ensuring that no two gates in the same layer act on the same qubit.

        Returns:
        list: A list of layers, where each layer is a list of gate indices that can be applied simultaneously.
        """
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



