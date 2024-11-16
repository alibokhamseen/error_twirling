import numpy as np
from useful_classes import Paulis
from typing import List
from sympy import Matrix





def basis(e: np.ndarray, p: Paulis) -> List[np.ndarray]:
    """
    Finds the Pauli basis elements from that contribute to the noise operator `e`.

    Args:
        e (np.ndarray): The noise operator matrix.
        p (Paulis): An object containing a collection of Pauli matrices in `p.multi_p`.

    Returns:
        List[np.ndarray]: A list of Pauli basis elements for which Tr(g @ e) != 0.
    """
    return [g for g in p.multi_p if np.trace(g @ e) != 0]

def find_generating_set(V):
    """
    Finds the minimal generating set Ṽ for the given set V of Pauli operators.

    Args:
        V (list[str]): List of Pauli operators as strings (e.g., ["IX", "IZ", "YX"]).

    Returns:
        list[str]: Minimal independent generating set Ṽ.
    """
    # Map Pauli operators to binary vectors
    binary_vectors = [pauli_to_binary(v) for v in V]

    # Perform Gaussian elimination (mod 2)
    M = Matrix(binary_vectors)
    M_reduced, _ = M.rref()  # Reduced row echelon form

    # Extract independent operators
    independent_indices = [i for i, row in enumerate(M_reduced.tolist()) if any(row)]
    return [V[i] for i in independent_indices]

def pauli_to_binary(pauli):
    """
    Converts a Pauli operator to its binary vector representation.

    Args:
        pauli (str): Pauli operator (e.g., "IX", "IZ").

    Returns:
        list[int]: Binary vector representation.
    """
    mapping = {'I': (0, 0), 'X': (1, 0), 'Z': (0, 1), 'Y': (1, 1)}
    return [bit for char in pauli for bit in mapping[char]]


def main():
    p = Paulis(2)
    print(find_generating_set(['XX', "YY", "ZI", 'II', "ZZ"]))
    print(find_generating_set(['IX', 'IZ', 'YX', 'ZX', 'YY']))

if __name__ == "__main__":
    main()
