import numpy as np
from useful_classes import Paulis, Q_states
from sympy import Matrix



def _find_generating_set(V: list[str]) -> list[str]: # for future use
    """
    Finds a generating set of vectors using sympy rref (identifies a linearly independent set)

    Args:
        V: A list of Pauli operators (e.g., ["XX", "YY", "ZZ"]).

    Returns:
        list[str]: A list of Pauli basis representing a generating set of input V
    """
    vectors = [_pauli_to_binary(v) for v in V] # Convert Pauli operators to binary vectors
    matrix = np.array(vectors)
    M = Matrix(matrix.T)
    rref_matrix, pivot_columns = M.rref()
    generating_set = [V[i] for i in pivot_columns]
    return generating_set

def _pauli_to_binary(pauli) -> list[int]: # for future use with _find_generating_set
    """
    Converts a Pauli operator to its binary vector representation.

    Args:
        pauli (str): Pauli operator (e.g., "IX", "IZ").

    Returns:
        list[int]: Binary vector representation.
    """
    mapping = {'I': (0, 0), 'X': (1, 0), 'Z': (0, 1), 'Y': (1, 1)}
    return [bit for char in pauli for bit in mapping[char]]

def _validate_error_channel(error_matrix, n_qubits): # for future use to support different type of input
    """
    Validate an error channel matrix.
    Reports all validation errors simultaneously.

    Parameters:
    - error_matrix (numpy.ndarray): The error channel matrix to validate.
    - n_qubits (int): The number of qubits the error channel acts on.

    Raises:
    - ValueError: If the matrix fails any of the validation checks.
    """
    errors = [] 
    # Check if square
    if error_matrix.shape[0] != error_matrix.shape[1]:
        errors.append("Error channel matrix must be square.")
    # Check dimensionality
    expected_dim = 2 ** n_qubits
    if error_matrix.shape[0] != expected_dim:
        errors.append(f"Error channel matrix must have dimensions {expected_dim}x{expected_dim} for {n_qubits} qubits.")
    # Check Hermiticity
    if not np.allclose(error_matrix, error_matrix.conj().T):
        errors.append("Error channel matrix must be Hermitian.")
    # Check Positive Semidefiniteness
    eigenvalues = np.linalg.eigvalsh(error_matrix)
    if not np.all(eigenvalues >= 0):
        errors.append(f"Error channel matrix must be positive semidefinite. Eigenvalues: {eigenvalues}")
    # Check Trace-Preserving 
    trace = np.trace(error_matrix)
    if not np.isclose(trace, 2 ** n_qubits):
        errors.append(f"Error channel matrix trace must be {2 ** n_qubits}. Got trace: {trace}")

    if errors:
        raise ValueError("Validation errors in error channel matrix:\n" + "\n".join(errors))
    print("Error channel matrix is valid.")

def validate_kraus_operators(K: list[np.ndarray]) -> None:
    """
    Validate a list of Kraus operators to ensure they form a valid quantum channel.
    
    Args:
        K (list of np.ndarray): List of Kraus operators.

    Raises:
        ValueError: If the completeness relation is not satisfied.
        TypeError: If any Kraus operator is not a NumPy array or if the list is empty.
        ValueError: If Kraus operators have inconsistent dimensions.
    """
    # Ensure the input is a list of NumPy arrays
    if not isinstance(K, list) or not all(isinstance(k, np.ndarray) for k in K):
        raise TypeError("Kraus operators must be a list of NumPy arrays.")

    # Ensure the list is not empty
    if len(K) == 0:
        raise ValueError("The list of Kraus operators cannot be empty.")

    # Check dimensional consistency
    dims = [k.shape for k in K]
    if not all(dim == dims[0] for dim in dims):
        raise ValueError("All Kraus operators must have the same dimensions.")

    # Ensure Kraus operators are square matrices
    if not all(k.shape[0] == k.shape[1] for k in K):
        raise ValueError("Each Kraus operator must be a square matrix.")

    # Validate completeness relation
    identity = np.eye(K[0].shape[0], dtype=np.complex128)
    completeness = sum(k.conj().T @ k for k in K)
    if not np.allclose(completeness, identity, atol=1e-10):
        raise ValueError("Kraus operators do not satisfy the completeness relation.")

def get_kraus_operators(error_model: dict[str: dict], P: Paulis):
    """
    Generate Kraus operators for a given error model using multi-qubit Pauli notation.
    
    Args:
        error_model (dict[str: dict]): Error model with probabilities for each state and Pauli error. {"11" : {"ZI": 0.1}}
        P (Paulis): Object containing multi-qubit Pauli operators.
    
    Returns:
        list: List of Kraus operators as numpy arrays.
    """
    kraus_operators = []
    num_qubits = P.n
    Q = Q_states(num_qubits)
    i_kraus = np.zeros((2 ** num_qubits, 2 ** num_qubits), np.complex128)
    possible_states = Q.states
    for state in possible_states:
        e_prob = 0
        s = Q.states[state]
        instructions = error_model[state] if state in error_model.keys() else {}
        for error, prob in instructions.items():
            if error == "I" * num_qubits:
                continue
            e_prob += prob
            kraus_operators.append(np.sqrt(prob) * P.multi_p[error] @ np.outer(s, s.conj()) )
        i_kraus += np.sqrt(1 - e_prob) * P.multi_p["I" * num_qubits] @ np.outer(s, s.conj())
    kraus_operators.append(i_kraus)
    return kraus_operators

def _get_pauli_probabilities(K: list[np.ndarray], W: list[str], P: Paulis) -> list[float]:
    """
    Extract probabilities of Pauli errors from an error channel matrix.

    Parameters:
    - K (list[np.ndarray]): List of Kraus operators.
    - W (list[str]): Twirling set of Pauli operators as strings.

    Returns:
    - list[float]: A list of probabilities corresponding to each Pauli error in W.
    """
    d = 2 ** P.n
    probabilities = []
    for s in W:
        w = P.multi_p[s]
        c_w = 0
        E_m = np.zeros_like(w)
        for k in K:
            # c_w += np.trace(w @ k @ k.conj().T) / d
            E_m += w @ k @ w.conj().T
        
        c_w = np.abs(np.trace(w @ E_m) / d)
        probabilities.append(c_w)
    return np.array(probabilities)

def twirl(error: dict[str: dict]) -> dict[str: float]:
    """
    Do the twirling given a state based error model.

    Parameters:
    - error (dict[str: dict]): Error instructions. ex: {
        "0" : {"y" : 0.3},
        "1" : {"X" : 0.5, "Y" : 0.3}
        }
    - num_qubits (int): Number of qubits in error channel to twirl

    Returns:
    - dict[str: float]: A dict of each Pauli error with its probability.
    """
    num_qubits = len(next(iter(error)))
    P = Paulis(num_qubits)
    K = get_kraus_operators(error, P)
    validate_kraus_operators(K)
    twirling_set = P.multi_p_string
    probabilities = _get_pauli_probabilities(K, twirling_set, P)
    results = {key: value for key, value in zip(twirling_set, probabilities) if value > 1e-8}
    return results



def main():
    p1, p2, p3 = 0.3, 0.3, .3
    error = {
    "01" : {"IX": p3},
    "10" : {"XX": p2, "XI": p3},
    "11" : {"IX": p1, "XI": p2, "XX": p3}
    }
    error = {
    "11" : {"XX": 0.1}
    }

    error = {
        # "0" : {"I" : 1},
        "1" : {"X" : 0.2}
    }
    
    twirling_results = twirl(error)
    print(twirling_results)

if __name__ == "__main__":
    main()
