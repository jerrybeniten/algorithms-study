FROM python:3.10-slim

# Install Qiskit with Aer (simulator) and matplotlib (optional for visualization)
RUN pip install --no-cache-dir qiskit qiskit-aer matplotlib

# Set work directory
WORKDIR /app

# Default command: open Python shell
CMD ["python3"]

# docker build -t qiskit-sim .
# docker run -it qiskit-sim

