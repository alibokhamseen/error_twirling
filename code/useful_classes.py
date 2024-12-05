import numpy as np
from itertools import product
from functools import reduce

"""
    Classes for internal use. User doesn't need to import this themselves.
"""

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
            self.multi_p = {
                label: self._kronecker_product(label) for label in self.multi_p_string
            }

    def _kronecker_product(self, label: str) -> np.ndarray:
        """
        Computes the Kronecker product of single-qubit Pauli matrices based on the given label.
        
        Args:
            label (str): A string of Pauli operators (e.g., "IXZ").
            
        Returns:
            np.ndarray: The multi-qubit Pauli matrix corresponding to the label.
        """
        result = self.single_p[label[0]]
        for pauli in label[1:]:
            result = np.kron(result, self.single_p[pauli])
        return result
    
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


class Q_states:
    def __init__(self, n) -> None:
        self.n = n
        self.states = {}
        self._generate_vector_states()
        
    def _generate_vector_states(self) -> None:
        z = np.array([1, 0])
        o = np.array([0, 1])
        q_state = {"0": z, "1": o}
        states = ["".join(p) for p in product(["0", "1"], repeat=self.n)]
        for s in states:
            self.states[s] = reduce(np.kron, [q_state[q] for q in list(s)])
