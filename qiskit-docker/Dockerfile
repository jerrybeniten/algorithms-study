FROM python:3.10-slim

# Avoid interactive prompts during image build
ENV DEBIAN_FRONTEND=noninteractive

# Install system deps (optional but handy for scientific Python)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \ 
    && rm -rf /var/lib/apt/lists/*

# Install Qiskit + Aer simulator + Matplotlib (optional for plotting)
RUN pip install --no-cache-dir qiskit qiskit-aer matplotlib

# Set working directory
WORKDIR /app

# Default command: open Python REPL
CMD ["python3"]
