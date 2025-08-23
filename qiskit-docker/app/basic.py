from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Create a quantum circuit with 1 qubit and 1 classical bit
qc = QuantumCircuit(1, 1)

# Apply Hadamard gate -> puts qubit in superposition (0 + 1 at once)
qc.h(0)

# Measure the qubit -> collapses into 0 or 1 randomly
qc.measure(0, 0)

# Use AerSimulator backend
simulator = AerSimulator()

# Transpile and run
from qiskit import transpile
compiled_circuit = transpile(qc, simulator)

result = simulator.run(compiled_circuit, shots=1000).result()

# Show counts of results
counts = result.get_counts()
print("Measurement results:", counts)

# Draw the circuit
print(qc.draw())
