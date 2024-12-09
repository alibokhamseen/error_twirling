# Twirling Error Channels

We twirl arbitrary error channels to get a mixture of pauli errors to use in fast stabilizer quantum simulations. 


# Pauli Twirling

This project implements implemets twirling using the full Pauli set. Our work takes a state-based-error-model (see below for details) and returns a Pauli twirled error channel.



## How It Works

Pauli Twirling is implemented by the `twirl()` function.
```bash
twirl(error: dict[str: dict]) -> dict[str: float]
```

### Inputs:
- **error: dict[str: dict]**\
A state-based noise channel.

Example:
   ```bash
    p1, p2, p3 = 0.1, 0.1, 0.1
    error = {
    "01" : {"IX": p3},
    "10" : {"XX": p2, "XI": p3},
    "11" : {"IX": p1, "XI": p2, "XX": p3}
    }
   ```
   The input variable "error" is a dictionary of states 01, 10, and 11. Each state is a dictionary of the Pauli operators and their associated probabilty. State 10 applies operators XX with probability p2 and XI with probability p3.

### Final Output:
- **dict[str: dict]**: A dictionary of states, each state a dictionary of Pauli operators and their associated probability. Same structure as the input.

## Features
- Simulates the twirling operation to calculate error probabilities.
- Outputs results for use in quantum error correction simulations and analysis.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/pauli-twirling.git
   cd pauli-twirling
   ```
2. Set up a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Example: Pauli Basis for the Noise Channel
Define your noise channel in the `noise_channel.py` file. For example:

```python
noise_channel = {'IX': 0.2, 'IZ': 0.3, 'XI': 0.1, 'XX': 0.4}


