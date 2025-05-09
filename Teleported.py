import json
from datetime import datetime
import numpy as np
from qiskit import QuantumCircuit, execute, Aer

class QuantumTeleporter:
    def __init__(self):
        self.backend = Aer.get_backend('qasm_simulator')

    def perform_teleportation(self, initial_state: str = '+', save: bool = False) -> dict:
        # Create a simple teleportation circuit
        qc = QuantumCircuit(3, 3)
        
        # Initialize the state to teleport (simplified example)
        if initial_state == '+':
            qc.h(0)  # |+⟩ state
        elif initial_state == '1':
            qc.x(0)  # |1⟩ state
        # Entangle qubits 1 and 2
        qc.h(1)
        qc.cx(1, 2)
        # Bell measurement on qubits 0 and 1
        qc.cx(0, 1)
        qc.h(0)
        qc.measure([0, 1], [0, 1])
        # Conditional corrections on qubit 2
        qc.cx(1, 2)
        qc.cz(0, 2)
        qc.measure(2, 2)

        # Execute the circuit
        job = execute(qc, self.backend, shots=1024)
        result = job.result()
        counts = result.get_counts()

        # Simulate the teleported state (for demonstration)
        teleported_state = [1/np.sqrt(2), 1/np.sqrt(2)] if initial_state == '+' else [0, 1]

        # Collect results
        experience = {
            'timestamp': datetime.now().isoformat(),
            'initial_state': initial_state,
            'counts': counts,
            'teleported_state': [complex(x).real + complex(x).imag * 1j for x in teleported_state],
            'circuit_depth': qc.depth(),
            'total_gates': qc.size()
        }

        # Save results if requested
        if save:
            self.save_results(experience)

        return experience

    def save_results(self, experience: dict, filename: str = None):
        """Save teleportation results to a JSON file."""
        if filename is None:
            timestamp = experience['timestamp'].replace(':', '-').replace('.', '-')
            filename = f"teleportation_results_{experience['initial_state']}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(experience, f, indent=4)
        print(f"Results saved to {filename}")

# Run an example
teleporter = QuantumTeleporter()
experience = teleporter.perform_teleportation(initial_state='+', save=True)
