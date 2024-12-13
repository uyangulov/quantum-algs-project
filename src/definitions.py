import numpy as np
cos, sin, exp = np.cos, np.sin, np.exp

# 1) Pauli X, Y, Z matrices
I = np.eye(2)
X = np.array([[0, 1], [1, 0]])  # Pauli X
Y = np.array([[0, -1j], [1j, 0]])  # Pauli Y
Z = np.array([[1, 0], [0, -1]])  # Pauli Z

# 2) T and H gate matrices
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]])  # T gate
H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])  # Hadamard (H) gate

# 3) CNOT, CX, CZ, CY matrices
# CNOT (Controlled NOT) gate
CNOT = np.array([[1, 0, 0, 0],
                 [0, 0, 0, 1],
                 [0, 0, 1, 0],
                 [0, 1, 0, 0]])

# CX matrix is the same as CNOT in 2-qubits (Control-X)
CX = CNOT

# CZ (Controlled-Z) gate
CZ = np.array([[1, 0, 0, 0],
               [0, 1, 0, 0],
               [0, 0, 1, 0],
               [0, 0, 0, -1]])

# CY (Controlled-Y) gate
CY = np.array([[1, 0, 0, 0],
               [0, 0, 0, -1j],
               [0, 0, 1, 0],
               [0, 1j, 0, 0]])

#qulacs definition
#https://docs.qulacs.org/ja/latest/guide/2.0_python_advanced.html
def RX(theta):
    theta2 = theta/2
    return np.array([
        [cos(theta2), 1j*sin(theta2)],
        [1j*sin(theta2), cos(theta2)],
    ])

def RZ(theta):
    theta2 = theta/2
    return np.array([
        [exp(1j*theta2), 0],
        [0, exp(-1j*theta2)],
    ])