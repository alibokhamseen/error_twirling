# Twirling Error Channels

We twirl arbitrary error channels to get a mixture of pauli errors to use in fast stabilizer quantum simulations. 


# Pauli Twirling

This project implements implemets twirling using the full Pauli set. Our work takes a state-based-error-model (see below for details) and returns a Pauli twirled error channel.



## How It Works

Pauli Twirling is implemented by the `twirl()` function.
```bash
twirl(error: dict[str, dict]) -> dict[str, float]
```

### Inputs:
- **error: dict[str, dict]**\
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
   Note individual sums of error probabilities of each state shouldn't exceed 1.
   
   The "error" input to be twirled is a dictionary with states as keys whose values are error instructions formated as dictionaries. Note that it is optional to include identity operations. Whenever probabilities of error instructions associated to a state is less than one, we assign identity to complete the sum.

### Final Output:
- **dict[str, dict]**: Twirled channel as a Pauli mixture with associated probabilities.

## Main Feature:
- Twirl highly customizable error models



## Example: 
available in [View the Tutorial Notebook](code/twirling101.py)

# Installation Instructions
Follow these steps to install and set up the this package:

### 1. Clone the Repository
Clone the repository to your local machine in your appropriate directory:

```bash
git clone https://github.com/alibokhamseen/error_twirling.git
```

### 2. Navigate to the Project Directory
Move into the project's main directory:

```bash
cd error_twirling
```

```python
from twirling import twirl
```

