# Qiskit + Docker: BB84 Examples

## Files
- `Dockerfile`: Python 3.10 + Qiskit + Aer
- `docker-compose.yml`: defines `qiskit` service (`qiskit-sim` container)
- `app/bb84.py`: BB84 without an eavesdropper
- `app/bb84_with_eve.py`: BB84 with an intercept-resend eavesdropper (shows QBER)

## Usage
```bash
# From the project folder
docker-compose up --build -d

# Run the simple BB84
docker exec -it qiskit-sim python3 /app/bb84.py

# Run the BB84 with Eve
docker exec -it qiskit-sim python3 /app/bb84_with_eve.py
```
