import numpy as np
from useful_classes import Paulis, Q_states
from sympy import Matrix


def _validate_error_channel(error_matrix, n_qubits):
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
    print(error_matrix)

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
            kraus_operators.append(np.sqrt(prob) * P.multi_p[error] @ np.outer(s, s)  )
        i_kraus += np.sqrt(1 - e_prob) * P.multi_p["I" * num_qubits] @ np.outer(s, s)
    kraus_operators.append(i_kraus)
    for k in kraus_operators:
        print(k)
    return kraus_operators

def _get_pauli_probabilities(E: np.ndarray, W: list[str], P: Paulis) -> list[float]:
    """
    Extract probabilities of Pauli errors from an error channel matrix.

    Parameters:
    - E (np.ndarray): The error channel matrix.
    - W (list[str]): Twirling set of Pauli operators as strings.

    Returns:
    - list[float]: A list of probabilities corresponding to each Pauli error in W.
    """
    d = 2 ** P.n
    probabilities = []
    for w in W:
        # Compute the coefficient c_v for the Pauli operator
        c_w = np.trace(P.multi_p[w] @ E) / d
        # Calculate the probability as the squared magnitude of c_v
        probabilities.append(np.abs(c_w) ** 2)
    return np.array(probabilities)

def twirl(error: dict[str: dict], num_qubits: int) -> dict[str: float]:
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
    P = Paulis(num_qubits)
    K = get_kraus_operators(error, P)
    E = sum([np.matmul(k.T, k) for k in K])
    _validate_error_channel(E, num_qubits)
    
    probabilities = np.zeros(4 ** num_qubits)
    for k in K:
        twirling_set = P.multi_p_string
        probabilities += _get_pauli_probabilities(k, twirling_set, P)
    results = {key: value for key, value in zip(twirling_set, probabilities) if value != 0}
    return results



def main():
    p1, p2, p3 = 0.1, 0.1, 0.1
    error = {
    "01" : {"IX": p3},
    "10" : {"XX": p2, "XI": p3},
    "11" : {"IX": p1, "XI": p2, "XX": p3}
    }
    error = {
    "11" : {"XX": 1}
    }
    num_qubits = 2

    error = {
        # "0" : {"I" : 1},
        "1" : {"X" : 1}
    }
    num_qubits = 1
    
    twirling_results = twirl(error, num_qubits)
    print(twirling_results)

if __name__ == "__main__":
    main()
