# BB84 with a simple intercept-resend eavesdropper (Eve)
# Expect ~25% Quantum Bit Error Rate (QBER) in the sifted key on average.
# Run with: python /app/bb84_with_eve.py
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import random

N = 64

# Alice: random bits & bases
alice_bits = [random.randint(0, 1) for _ in range(N)]
alice_bases = [random.randint(0, 1) for _ in range(N)]  # 0 = Z, 1 = X

# Eve: intercept-resend strategy
# She measures each qubit in a random basis, then resends the collapsed state to Bob.
eve_bases = [random.randint(0, 1) for _ in range(N)]

# Simulator
sim = Aer.get_backend('aer_simulator')

# Helper to prepare a single-qubit state for Alice
def prepare_state(bit, base):
    qc = QuantumCircuit(1, 1)
    if bit == 1:
        qc.x(0)
    if base == 1:
        qc.h(0)
    return qc

# Eve intercepts and resends
eve_measurements = []
eve_resend_circuits = []
for a_bit, a_base, e_base in zip(alice_bits, alice_bases, eve_bases):
    qc = prepare_state(a_bit, a_base)

    # Eve's measurement
    qc_eve = qc.copy()
    if e_base == 1:
        qc_eve.h(0)
    qc_eve.measure(0, 0)
    tqc_eve = transpile(qc_eve, sim)
    eve_bit = int(sim.run(tqc_eve, shots=1, memory=True).result().get_memory()[0])
    eve_measurements.append(eve_bit)

    # Eve resends the state she measured in her chosen basis
    resend = QuantumCircuit(1, 1)
    if e_base == 1:
        resend.h(0)  # prepare X-basis |+> or |-> from Z basis later
    if eve_bit == 1:
        resend.x(0)
    eve_resend_circuits.append(resend)

# Bob: random bases & measurement on Eve's resent qubits
bob_bases = [random.randint(0, 1) for _ in range(N)]
bob_results = []
for resend, b_base in zip(eve_resend_circuits, bob_bases):
    qc_bob = resend.copy()
    if b_base == 1:
        qc_bob.h(0)
    qc_bob.measure(0, 0)
    tqc_bob = transpile(qc_bob, sim)
    bob_bit = int(sim.run(tqc_bob, shots=1, memory=True).result().get_memory()[0])
    bob_results.append(bob_bit)

# Sifting: keep only indices where Alice and Bob used the same basis
sifted_indices = [i for i,(ab,bb) in enumerate(zip(alice_bases, bob_bases)) if ab == bb]
alice_key = [alice_bits[i] for i in sifted_indices]
bob_key   = [bob_results[i] for i in sifted_indices]

# Compute QBER (fraction of mismatched bits in sifted key)
if len(alice_key) > 0:
    errors = sum(1 for a,b in zip(alice_key, bob_key) if a != b)
    qber = errors / len(alice_key)
else:
    errors = 0
    qber = 0.0

print("Alice bases:", alice_bases)
print("Eve bases  :", eve_bases)
print("Bob bases  :", bob_bases)
print("Sifted idx :", sifted_indices)
print("Alice key  :", alice_key)
print("Bob key    :", bob_key)
print(f"Sifted length: {len(alice_key)}  Errors: {errors}  QBER: {qber:.2%}")
