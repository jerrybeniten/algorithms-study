from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Create a circuit with 2 qubits and 2 classical bits
qc = QuantumCircuit(2, 2)

# Step 1: Put the first qubit into superposition (like your coin flip before)
qc.h(0)

# Step 2: Entangle the second qubit with the first
qc.cx(0, 1)

# Step 3: Measure both qubits
qc.measure([0,1], [0,1])

# Run simulation
sim = AerSimulator()
result = sim.run(qc, shots=1000).result()
counts = result.get_counts()

print("Measurement results:", counts)
print(qc.draw())
