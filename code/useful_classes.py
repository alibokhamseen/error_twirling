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
        self.multi_p_string = [''.join(p) for p in product(pauli_labels, repeat=self.n)]
        if self.n == 1:
            self.multi_p = self.single_p
        else:
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


        

    