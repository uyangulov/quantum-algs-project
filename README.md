# Quantum Computing Emulator and Algorithms

This project implements a quantum computing emulator and algorithms such as Grover's Search and QAOA (Quantum Approximate Optimization Algorithm) using custom Python code. It includes examples of running quantum circuits, simulating quantum operations, and testing various components.

## Project Overview

- **Emulator**: A custom-built quantum emulator to simulate quantum gates and circuits.
- **Algorithms**: Implementations of Grover's Search and QAOA.
- **Testing**: Unit tests for validating different components of the emulator and algorithms.
- **Examples**: Example scripts to run and test quantum circuits and algorithms.

## Directory Structure

- `run_examples/`: Contains example scripts for running quantum algorithms and simulating quantum circuits.
  - `a.py`: A basic example script.
  - `distribution_after_qaoa.py`: Example of running QAOA and displaying the resulting distribution.
  - `graph_expect.py`: Graph-based expectations used in QAOA or Grover's algorithm.
  - `run_grover_instance.py`: Running an instance of Grover's search algorithm.

- `src/`: Source code for the quantum emulator and algorithms.
  - `abstract_emulator.py`: Defines the abstract base class for the quantum emulator.
  - `circuit.py`: Contains classes and functions to build and manipulate quantum circuits.
  - `definitions.py`: Contains various constant definitions used in the quantum emulator and algorithms.
  - `emulator.py`: Implements the quantum emulator logic and gate operations.
  - `generator.py`: Generates random quantum circuits.
  - `grover.py`: Implements Grover's search algorithm.
  - `qaoa.py`: Implements the Quantum Approximate Optimization Algorithm.
  - `qiskit_wrapper.py`: Interface to Qiskit for running quantum circuits on real quantum hardware.
  - `statevector.py`: Implements the state vector simulator for quantum circuits.

- `temp/`: Temporary files used during the execution of the project.
  - `test_launches.py`: Example script to test the launch of the quantum emulator.

- `tests/`: Unit tests for the project.
  - `emulator/`: Tests for the quantum emulator.
  - `grover/`: Tests for the Grover's algorithm.
  - `qaoa/`: Tests for the QAOA implementation.
  - `qiskit_wrapper/`: Tests for the Qiskit wrapper integration.

## Requirements

To run the project, you need the following Python packages:

- `numpy`
- `pytest`
- `qiskit` (for quantum hardware integration)

Install the required packages using `pip`:

```bash
pip install numpy pytest qiskit

