import numpy as np
# from functools import reduce
# from itertools import product
# import matplotlib.pyplot as plt

from circuit import QuantumCircuit, Gate
from definitions import H
from qiskit import QuantumCircuit as QiskitQuantumCircuit
from qiskit.transpiler.passes import Unroll3qOrMore
from qiskit.transpiler import PassManager
from math import log2, floor
from qiskit.quantum_info import Operator


class SearchProblem:
    """
    A class to represent a search problem, where the goal is to find marked numbers 
    within a problem space of size N. This can be used in quantum search algorithms, 
    such as Grover's algorithm, to define the problem structure and generate the corresponding
    oracle circuit.

    Attributes:
        N (int): The size of the problem space, which represents the total number of possible numbers.
        marked_numbers (list[int]): A list of marked numbers, which are the targets in the search problem.
        
    Properties:
        size (int): Returns the size of the problem space (N).
        marked_numbers (list[int]): Returns the list of marked numbers.
        num_qubits_required (int): Returns the number of qubits required to represent the problem space.
        
    Methods:
        __init__(N: int = 0, marked: list[int] = None):
            Initializes a SearchProblem instance with a problem size and a list of marked numbers.
        
        oracle_circuit():
            Generates and returns the oracle circuit for this search problem. The oracle marks the marked 
            numbers by flipping corresponding states in the quantum circuit.

    Raises:
        ValueError: If no marked numbers are provided or if any marked number is greater than or equal 
                    to the size of the problem (N).
    """

    def __init__(self, N: int = 0, marked: list[int] = None):
        """
        Initializes a SearchProblem instance with the specified problem size and marked numbers.

        Args:
            N (int): The size of the problem space, representing the total number of possible numbers.
            marked (list[int]): A list of marked numbers (target numbers to be found in the search).
        
        Raises:
            ValueError: If no marked numbers are provided or if any marked number is greater than or equal 
                        to N (problem size).
        """
        if not marked:
            raise ValueError("Instantiation of search problem requires at least one marked number")

        if any(x<0 or x >= N for x in marked):
            raise ValueError("Occurrence of marked number <= 0 or >= length of problem")

        self._marked = marked
        self._N = N

    @property
    def size(self):
        """
        Returns the size of the problem space (N), which is the total number of possible numbers.
        
        Returns:
            int: The size of the problem space.
        """
        return self._N
    
    @property
    def marked_numbers(self):
        """
        Returns the list of marked numbers that are the targets in the search problem.
        
        Returns:
            list[int]: The list of marked numbers.
        """
        return self._marked
    
    @property
    def num_qubits_required(self):
        """
        Calculates and returns the number of qubits required to represent the problem space, which is
        the logarithm (base 2) of the size of the problem space, rounded up to the nearest integer.
        
        Returns:
            int: The number of qubits required to represent the problem space.
        """
        return floor(log2(self.size)) + 1
    
    def oracle_circuit(self) -> QuantumCircuit:
        """
        Generates the oracle circuit for the search problem. The oracle flips the sign of the marked
        states in the quantum system. 
        
        Returns:
            QuantumCircuit: The oracle circuit corresponding to the search problem.
        """
        num_qubits = self.num_qubits_required
        oracle_matrix = np.eye(2**num_qubits)
        oracle_matrix[self.marked_numbers, self.marked_numbers] = -1
        oracle_circuit = QiskitQuantumCircuit(num_qubits)
        oracle_circuit.append(
            Operator(oracle_matrix), qargs = range(num_qubits)
        )
        oracle_circuit = PassManager(
            Unroll3qOrMore(basis_gates=['cx', 'rx', 'rz', 'ry'])
        ).run(oracle_circuit)

        circuit = QuantumCircuit().from_qiskit(oracle_circuit)
        return circuit
    
       
    
class GroverCircuit(QuantumCircuit):
    """
    Represents a quantum circuit implementation of Grover's search algorithm.
    This class builds the Grover's algorithm circuit from a given search problem.

    Attributes:
        gates (list): A list to store the gates in the circuit.
    """

    def __init__(self):
        """
        Initializes the GroverCircuit class.
        """
        self.gates = []

    def from_search_problem(self, problem: SearchProblem):
        """
        Constructs the Grover's algorithm circuit from a given search problem.

        The circuit is built with the following steps:
        1. Apply a row of Hadamard gates to create an equal superposition state.
        2. Apply the oracle circuit provided by the search problem.
        3. Apply the diffusion operator.

        Args:
            problem (SearchProblem): An instance of SearchProblem defining the
                                     oracle and the number of qubits required.

        Returns:
            GroverCircuit: The constructed Grover's circuit.

        Raises:
            ValueError: If the provided problem is not an instance of SearchProblem.
        """
        if not isinstance(problem, SearchProblem):
            raise ValueError(f'SearchProblem instance required, not {type(problem)}')

        qubits_required = problem.num_qubits_required

        # Apply a row of Hadamard gates
        self.__append_H__(qubits_required)

        # Add the oracle circuit
        oracle_circuit = problem.oracle_circuit()
        self.concat(oracle_circuit)

        # Add the diffusion operator
        self.__append_H__(qubits_required)
        reflection_circuit = self.__make__reflection__circuit__(qubits_required)
        self.concat(reflection_circuit)
        self.__append_H__(qubits_required)

        return self

    def __make__reflection__circuit__(self, n):
        """
        Constructs the reflection (inversion about the mean) circuit.

        This circuit implements the reflection operator used in Grover's algorithm.

        Args:
            n (int): Number of qubits.

        Returns:
            QuantumCircuit: The constructed reflection circuit.
        """
        reflection_matrix = -np.eye(2**n)
        reflection_matrix[0, 0] = 1
        reflection_circuit = QiskitQuantumCircuit(n)
        reflection_circuit.append(
            Operator(reflection_matrix), qargs=range(n)
        )
        reflection_circuit = PassManager(
            Unroll3qOrMore(basis_gates=['cx', 'rx', 'rz', 'ry'])
        ).run(reflection_circuit)

        circuit = QuantumCircuit().from_qiskit(reflection_circuit)
        return circuit

    def __append_H__(self, n):
        """
        Appends Hadamard gates to the circuit for all qubits.

        Args:
            n (int): Number of qubits to apply the Hadamard gate to.
        """
        for index in range(n):
            self.append(Gate([index], H, f"Hadamard_{index}"))





    

    