'''
from qiskit import QuantumCircuit, Aer, transpile, assemble

# Create a simple 2-qubit circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Run simulation
sim = Aer.get_backend("aer_simulator")
qobj = assemble(transpile(qc, sim))
result = sim.run(qobj).result()
print(result.get_counts())
'''