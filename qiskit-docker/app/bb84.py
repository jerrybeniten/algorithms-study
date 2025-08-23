# BB84 Quantum Key Distribution (simplified, no eavesdropper)
# Run with: python /app/bb84.py
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import random

# Number of qubits (raw key length before sifting)
N = 32

# Step 1: Alice generates random bits and bases (0 = Z basis, 1 = X basis)
alice_bits = [random.randint(0, 1) for _ in range(N)]
alice_bases = [random.randint(0, 1) for _ in range(N)]

# Step 2: Prepare circuits for each qubit encoding
circuits = []
for bit, base in zip(alice_bits, alice_bases):
    qc = QuantumCircuit(1, 1)
    if bit == 1:
        qc.x(0)  # encode |1> if bit is 1
    if base == 1:
        qc.h(0)  # switch to X basis
    # Bob's basis choice will be applied just before measurement
    circuits.append(qc)

# Step 3: Bob chooses random bases and measures
bob_bases = [random.randint(0, 1) for _ in range(N)]
bob_results = []

sim = Aer.get_backend('aer_simulator')
for qc, base in zip(circuits, bob_bases):
    qc2 = qc.copy()
    if base == 1:
        qc2.h(0)  # measure in X basis
    qc2.measure(0, 0)
    tqc = transpile(qc2, sim)
    result = sim.run(tqc, shots=1, memory=True).result()
    bit = int(result.get_memory()[0])
    bob_results.append(bit)

# Step 4: Publicly compare bases and keep only matches (sifting)
sifted_indices = [i for i,(ab,bb) in enumerate(zip(alice_bases, bob_bases)) if ab == bb]
alice_key = [alice_bits[i] for i in sifted_indices]
bob_key   = [bob_results[i] for i in sifted_indices]

print("Alice bits :", alice_bits)
print("Alice bases:", alice_bases)
print("Bob bases  :", bob_bases)
print("Bob results:", bob_results)
print("Sifted idx :", sifted_indices)
print("Alice key  :", alice_key)
print("Bob key    :", bob_key)
print("Key length :", len(alice_key))
