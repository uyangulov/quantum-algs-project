import math

class StateVector:
    """
    A class to represent a quantum state vector for a quantum system with a specified number of qubits.

    Attributes:
        num_qubits (int): The number of qubits in the quantum system.
        vector (list[complex]): The state vector amplitudes.
        length (int): The length of the state vector, which is 2^num_qubits.

    Methods:
        vector: Property for accessing and updating the state vector.
        __getitem__(key): Access a specific amplitude in the state vector.
        __setitem__(key, value): Update a specific amplitude in the state vector.
        from_list(new_vector): Create the state vector from a new list, checking if its length is a power of 2, and updating the number of qubits.
        from_num_qubits(num_qubits): Initialize a state vector from the number of qubits at |0> state.
    """

    def __init__(self, new_vector: list[complex] = None, num_qubits: int = None):
        """
        Initialize the StateVector either from a list or from the number of qubits.

        Args:
            new_vector (list[complex], optional): The state vector to initialize from.
            num_qubits (int, optional): The number of qubits to initialize the state vector with.

        Raises:
            ValueError: If new_vector is not a power of 2 or if num_qubits is not a positive integer.
        """
        if new_vector is not None:
            self.from_list(new_vector)  # Initialize from the list
        elif num_qubits is not None:
            self.from_num_qubits(num_qubits)  # Initialize from num_qubits
        else:
            raise ValueError("You must provide either new_vector or num_qubits.")

    @property
    def vector(self):
        """
        Get the state vector amplitudes.

        Returns:
            list[complex]: The state vector amplitudes.
        """
        return self._vector

    @vector.setter
    def vector(self, new_vector: list[complex]):
        """
        Set the state vector amplitudes.

        Args:
            new_vector (list[complex]): The new state vector amplitudes.

        Raises:
            ValueError: If the length of new_vector does not match 2^num_qubits.
        """
        if len(new_vector) != self.length:
            raise ValueError(
                f"The new vector length ({len(new_vector)}) does not match the expected length ({self.length})."
            )
        self._vector = new_vector

    @property
    def length(self):
        """
        Get the length of the state vector.

        Returns:
            int: The length of the state vector, which is 2^num_qubits.
        """
        return 2 ** self.num_qubits

    def __getitem__(self, key):
        """
        Access a specific amplitude in the state vector.

        Args:
            key (int): The index of the amplitude to access.

        Returns:
            complex: The amplitude at the specified index.
        """
        return self._vector[key]

    def __setitem__(self, key, value):
        """
        Update a specific amplitude in the state vector.

        Args:
            key (int): The index of the amplitude to update.
            value: The new value for the amplitude.

        """
        self._vector[key] = value

    def from_list(self, new_vector: list[complex]):
        """
        Update the state vector from a new list. The length of the list must be a power of 2.
        This also updates the number of qubits based on the length of the new vector.

        Args:
            new_vector (list[complex]): The new state vector.

        Raises:
            ValueError: If the length of new_vector is not a power of 2
        """
        length = len(new_vector)
        
        # Check if the length is a power of 2
        if not (length and (length & (length - 1)) == 0):  # Checks if length is power of 2
            raise ValueError("Length of the new vector must be a power of 2.")
        
        # Update num_qubits based on the length of the new vector
        self.num_qubits = int(math.log2(length))
        
        # Set the new vector
        self.vector = new_vector

    def from_num_qubits(self, num_qubits: int):
        """
        Initialize the state vector from the number of qubits.

        Args:
            num_qubits (int): The number of qubits to initialize the state vector with.

        Raises:
            ValueError: If num_qubits is not a positive integer.
        """
        if num_qubits < 1:
            raise ValueError("Number of qubits must be a positive integer.")
        
        state_vector_length = 2 ** num_qubits
        self._vector = [0] * state_vector_length
        self._vector[0] = 1  # Initialize in the |0⟩ state
        self.num_qubits = num_qubits