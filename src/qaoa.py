from circuit import Gate, QuantumCircuit
from definitions import H, RX, RZ, CNOT, Z
import numpy as np
from scipy.optimize import minimize
from statevector import StateVector
from emulator import MyEmulator
from qiskit_wrapper import QiskitWrapperEmulator


class QAOA_MaxCut_Circuit(QuantumCircuit):

    #create qaoa instance with 0 layers (just H to prepare state)
    def __init__(self, num_qubits: int = 1, edges: list[tuple] = None):
        
        if not isinstance(num_qubits, int):
            raise ValueError("num_layers and num_qubits must be integer")
        
        if (num_qubits <= 0):
            raise ValueError("at least 1 qubit is required")

        if any(x >= num_qubits for edge in edges for x in edge):
            raise ValueError("Amount of vertices in edges require more qubits")       
        
        #layer of hadamards
        self.gates = []
        for index in range(num_qubits):
            self.append(Gate([index], H, "Hadamard"))

        self.edges = edges
        #different from depth
        self.num_qaoa_layers = 0

    def add_layer(self, gamma: float, beta: float):
        self.__add_U_C__(gamma)
        self.__add_U_X__(beta)
        self.num_qaoa_layers += 1

    def __add_U_X__(self, beta):
        n = self.num_qubits
        for index in range(n):
            self.append(Gate([index], RX(-2 * beta), "RX"))

    def __add_U_C__(self, gamma):
        for index, jndex in self.edges:
            self.append(Gate([index,jndex], CNOT, "CNOT"))
            self.append(Gate([jndex], RZ(-2 * gamma), "RZ"))
            self.append(Gate([index,jndex], CNOT, "CNOT"))

    def expectation_val(self, backend: str = "MyEmulator"):

        emulator = None
        if backend == "Qiskit":
            emulator = QiskitWrapperEmulator()
        elif backend == "MyEmulator":
            emulator = MyEmulator()
        else:
            raise ValueError("Unknown or unsupported backend")
        
        #calculate output |result> of QAOA circuit
        result = emulator.apply_circuit(
            self, 
            StateVector(self.num_qubits)
        )

        # calculate C|result>, where C is cost hamiltonian: \sum Z_i Z_j
        evolved = result.vector.copy()
        for i, j in self.edges:
            temp = emulator.apply_gate(Gate([i], Z, "Z"), result)
            temp = emulator.apply_gate(Gate([j], Z, "Z"), temp)
            evolved = np.add(evolved, temp.vector)

        #C is hermitan so trunk small imag part, if anuy
        val = np.real(np.dot(np.conjugate(result.vector), evolved))

        return val
    


            







            