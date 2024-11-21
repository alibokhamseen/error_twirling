# error_twirling

We twirl arbitrary error channels to get a mixture of pauli errors to use in fast stabilizer quantum simulations. We follow the procedure outlined in https://www.nature.com/articles/s41598-019-46722-7.


$$
\tau_W(\overline{M}) = \frac{1}{|W|} \sum_{w \in W} w \overline{M} w^\dagger
$$

# Pauli Twirling Simulation

This project implements a quantum error correction technique called **Pauli Twirling**, which simplifies arbitrary noise channels into Pauli channels. Our work is based on the framework presented in *"Constructing Smaller Pauli Twirling Sets for Arbitrary Error Channels"* by Zhenyu Cai and Simon Benjamin, and aims to improve simulation efficiency by reducing the size of the twirling gate set.

## How It Works

### Input:
- A **Noise Channel**: The input error channel represented in terms of Pauli basis.

### Intermediate Outputs:
1. **Generate Twirling Set**: Derive a minimal twirling gate set from the noise channel.
2. **Operate on Noise Channel**: Apply the twirling set to transform the noise channel into a Pauli channel.

### Final Output:
- **Probabilities of Pauli Matrices**: The resultant Pauli channel expressed as a probability distribution over Pauli errors.

## Features
- Efficiently generates optimized twirling sets using the symmetries in noise channels.
- Simulates the twirling operation to calculate error probabilities.
- Outputs results for use in quantum error correction simulations and analysis.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/pauli-twirling.git
   cd pauli-twirling
2. Set up a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Example: Pauli Basis for the Noise Channel



