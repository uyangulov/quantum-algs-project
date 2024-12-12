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

    def __init__(self):
        self.gates = []

    def from_search_problem(self, problem: SearchProblem):

        if not isinstance(problem, SearchProblem):
            raise ValueError(f'SearchProblem instance required, not {type(problem)}')

        qubits_required = problem.num_qubits_required
        
        #row of hadamards
        self.__append_H__(qubits_required)

        #oracle circuit
        oracle_circuit = problem.oracle_circuit()
        self.concat(oracle_circuit)

        #diffusion operator
        self.__append_H__(qubits_required)
        reflection_circuit = self.__make__reflection__circuit__(qubits_required)
        self.concat(reflection_circuit)
        self.__append_H__(qubits_required)

        return self

    
    def __make__reflection__circuit__(self, n):
        
        reflection_matrix = -np.eye(2**n)
        reflection_matrix[0, 0] = 1
        reflection_circuit = QiskitQuantumCircuit(n)
        reflection_circuit.append(
            Operator(reflection_matrix), qargs = range(n)
        )
        reflection_circuit = PassManager(
            Unroll3qOrMore(basis_gates=['cx', 'rx', 'rz', 'ry'])
        ).run(reflection_circuit)

        print(reflection_matrix)

        circuit = QuantumCircuit().from_qiskit(reflection_circuit)
        return circuit

    def __append_H__(self, n):
        for index in range(n):
            self.append(Gate([index], H, f"Hadamard_{index}"))



    
    



        



        


# #construct oracle matrix by answer
# def oracle(answer : list[int]):
#     n = len(answer)
#     num = sum([2**i * answer[i] for i in range(n)])
#     print(num)
#     N = 2**n
#     diag_arr = np.full(shape=(N,), fill_value=1)
#     diag_arr[num] = -1
#     mat = np.diag(diag_arr)
#     return mat
    
# def hadamard(n):
#     H = (1 / np.sqrt(2)) * np.array([[1, 1], 
#                                    [1, -1]])
#     return reduce(np.kron, [H] * n)


# #num of qubits
# n = 3
# N = 2**n


# state_vector = np.ones(shape=(N,))
# state_vector /= np.sqrt(N)
# ans = np.random.randint(0, 2, size=n)
# num = sum([2**i * ans[i] for i in range(n)])
# print(ans)

# orr  = oracle(ans)
# had  = hadamard(n)

# theta = 2 * np.arccos(np.sqrt(1 - 1/N))
# #n_iter = int(np.pi/4 * np.sqrt(N)) + 1
# n_iter = 100

# comp = []

# for k in range(1, n_iter):

#     state_vector = orr @ state_vector
#     state_vector = had @ state_vector
#     state_vector = -state_vector
#     state_vector[0] = -state_vector[0]
#     state_vector = had @ state_vector

#     comp.append(state_vector[num])

# rg = np.arange(1,n_iter,0.01)
# theor = np.sin(theta * (2 * rg + 1) / 2)
# print(theor)

# # plt.scatter(range(1,n_iter), comp, label = r'grover result')
# # plt.plot(rg, theor, label = r'sin($\frac{2k+1}{2} \theta$)' , ls = ":")
# # plt.legend(framealpha = 1)
# # plt.show()



    

    