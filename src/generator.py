from circuit import Gate, QuantumCircuit
from scipy import linalg
import numpy as np

class Randomizer:
    """
    A class for generating random numbers

    Attributes:
        m (int): The modulus parameter
        a (int): The multiplier parameter
        c (int): The increment parameter
        X (int): The current state of the random number generator.
    
    Methods:
        generate_initial_num(seed, n0):
            Generates the initial state of the random number generator.

        rand_int():
            Generates the next random integer in the sequence.

        rand(L=None):
            Generates a random floating-point number in [0, 1) or scaled to [-L, L].
    """

    def __init__(self,
                 m=65537,
                 a=75,
                 c=74,
                 seed=27):
        """
        Initializes the random number generator with given parameters.

        Args:
            m (int): The modulus parameter. Default is 65537.
            a (int): The multiplier parameter. Default is 75.
            c (int): The increment parameter. Default is 74.
            seed (int): The initial seed value. Default is 27.
        """
        self.a = a
        self.c = c
        self.m = m
        self.X = self.generate_initial_num(seed, n0=100)

    def generate_initial_num(self, seed, n0):
        """
        Generates the initial state of the random number generator.

        Args:
            seed (int): The initial seed value.
            n0 (int): Number of iterations to "warm up" the generator.

        Returns:
            int: The initial state after warming up.
        """
        X = seed
        for _ in range(n0):
            X = (self.a * X + self.c) % self.m
        return X

    def rand_int(self):
        """
        Generates the next random integer in the sequence.

        Returns:
            int: The next random integer.
        """
        self.X = (self.a * self.X + self.c) % self.m
        return self.X

    def rand(self, L=None):
        """
        Generates a random floating-point number.

        Args:
            L (float, optional): If provided, scales the output to [-L, L].

        Returns:
            float: A random floating-point number in [0, 1) or scaled to [-L, L].
        """
        self.X = (self.a * self.X + self.c) % self.m
        return self.X / self.m if L is None else (self.X / self.m - 0.5) * 2 * L

class RandomCircuitGenerator:
    """
    A class for generating random quantum circuits with a specified width, n_gates, and 2-qubit gate weight.

    Attributes:
        width (int): The number of qubits in the quantum circuit.
        n_gates (int): The number of n_gates in the quantum circuit.
        w (float): The probability weight of inserting a 2-qubit gate.
        randomizer (Randomizer): A Randomizer instance used for generating random numbers.

    Methods:
        get_random_unitary(mode):
            Generates a random unitary matrix for 1-qubit or 2-qubit gates.

        generate():
            Generates a random quantum circuit based on the specified parameters.
    """

    def __init__(self,
                 width: int,
                 n_gates: int,
                 weight2q: float,
                 seed: int = 27):
        """
        Initializes the random circuit generator.

        Args:
            width (int): The number of qubits in the circuit.
            n_gates (int): The number of gates in the circuit.
            weight2q (float): The probability for inserting 2-qubit gates.
            seed (int, optional): The seed for the random number generator. Default is 27.
        """
        self.width = width
        self.n_gates = n_gates
        self.w = weight2q
        self.randomizer = Randomizer(seed=seed)

    def get_random_unitary(self, mode: str):
        """
        Generates a random unitary matrix for a 1-qubit or 2-qubit gate.

        Args:
            mode (str): The type of gate ('1q' for 1-qubit, '2q' for 2-qubit).

        Returns:
            np.ndarray: A unitary matrix for the specified gate type.

        Raises:
            AssertionError: If the mode is not '1q' or '2q'.
        """
        assert mode in ['1q', '2q'], f"{mode} is not supported, only 1q or 2q"

        if mode == '1q':
            c = [self.randomizer.rand(L=100) for _ in range(4)]
            U = 1j * np.array([[c[0], c[1] + 1j * c[2]],
                               [c[1] - 1j * c[2], c[3]]])
            return linalg.expm(U)

        c = [self.randomizer.rand(L=100) for _ in range(16)]
        U = np.array([[c[0], c[1] + 1j*c[2], c[3] + 1j*c[4], c[5] + 1j*c[6]],
                      [c[1] - 1j*c[2], c[7], c[8] + 1j*c[9], c[10] + 1j*c[11]],
                      [c[3] - 1j*c[4], c[8] - 1j*c[9], c[12], c[13] + 1j*c[14]],
                      [c[5] - 1j*c[6], c[10] - 1j*c[11], c[13] - 1j*c[14], c[15]]]) * 1j
        return linalg.expm(U)

    def generate(self):
        """
        Generates a random quantum circuit based on the specified width, n_gates, and 2-qubit gate weight.

        Returns:
            QuantumCircuit: The generated random quantum circuit.
        """
        qc = QuantumCircuit()

        for _ in range(self.n_gates):
            rand_num = self.randomizer.rand()

            if rand_num >= self.w or self.width == 1:  # Add a 1-qubit gate
                q = self.randomizer.rand_int() % self.width
                U = self.get_random_unitary(mode='1q')
                qc.append(Gate([q], U))
            else:  # Add a 2-qubit gate
                q1 = self.randomizer.rand_int() % self.width
                q2 = self.randomizer.rand_int() % self.width
                while q2 == q1:
                    q2 = self.randomizer.rand_int() % self.width

                U = self.get_random_unitary(mode='2q')
                qc.append(Gate([q1, q2], U))

        return qc
