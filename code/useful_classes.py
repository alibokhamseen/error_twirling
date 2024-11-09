import numpy as np
from itertools import product

class Paulis:
    def __init__(self, n: int = 1) -> None:
        """
        Initializes the Paulis class to generate multi-qubit Pauli matrices.
        
        Args:
            n (int): The number of qubits for the multi-qubit Pauli matrices.
        """
        self.n = n
        self.single_p = {
            "I": np.array([[1, 0], [0, 1]], dtype=np.complex128),
            "X": np.array([[0, 1], [1, 0]], dtype=np.complex128),
            "Y": np.array([[0, -1j], [1j, 0]], dtype=np.complex128),
            "Z": np.array([[1, 0], [0, -1]], dtype=np.complex128),
        }
        
        # Generate all multi-qubit Pauli strings and matrices
        pauli_labels = ["I", "X", "Y", "Z"]
        self.multi_p_string = np.array(list(product(pauli_labels, repeat=n)), dtype=str)
        self.multi_p = {''.join(label): np.linalg.multi_dot([self.single_p[pauli] for pauli in label])
                        for label in self.multi_p_string}
    
    def get_p_mat(self, inp: str) -> np.ndarray:
        """
        Retrieves the multi-qubit Pauli matrix for the given input string.
        
        Args:
            inp (str): A string representing the Pauli operators (e.g., "IXZ").
        
        Returns:
            np.ndarray: The resulting multi-qubit Pauli matrix.
        """
        assert len(inp) == self.n, "Input length does not match the number of qubits"
        return self.multi_p[inp]

class CommutatorGeneratorTables:
    """"Create Commutator and Generator Tables for Given Matrices A & B"""
    def __init__(self, A = None, B = None, size = 3):
        self.A = A if A is not None else np.random.rand(3, 3)
        self.B = B if B is not None else np.random.rand(3, 3)
        self.size = size
        self.commutator_table = None
        self.generator_table = None

    def zeta(self, g_i, g_j):
        commutator = g_i * g_j - g_j * g_i  
        anticommutator = g_i * g_j + g_j * g_i  
        
        if commutator == 0:
            return 1 
        elif anticommutator == 0:
            return -1 
        else:
            return 0  

    def create_commutator_table(self):
        self.commutator_table = np.zeros((self.A.shape[0], self.B.shape[1]), dtype=int)

        for i in range(self.A.shape[0]):
            for j in range(self.B.shape[1]):
                try:
                    self.commutator_table[i, j] = self.zeta(self.A[i, j], self.B[i, j])
                except ValueError:
                    self.commutator_table[i, j] = 0  

        return self.commutator_table

    def generator_zeta(self, i, j):
        return 1 - 2 * (i == j)

    def create_generator_table(self):
        self.generator_table = np.zeros((self.size, self.size), dtype=int)

        for i in range(self.size):
            for j in range(self.size):
                self.generator_table[i, j] = self.generator_zeta(i, j)

        return self.generator_table