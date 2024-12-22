from qaoa import QAOA_MaxCut_Circuit
from scipy.optimize import minimize
import numpy as np
from emulator import MyEmulator
from statevector import StateVector
import matplotlib.pyplot as plt
import networkx as nx 
from qiskit_wrapper import QiskitWrapperEmulator


# Build and visualize the graph using networkx
def visualize_graph(edges, node_colors=None):
    G = nx.Graph()
    G.add_edges_from(edges)
    
    # Default node colors if not provided
    node_colors = node_colors or ["lightblue"] * len(G.nodes)
    
    # Draw the graph
    plt.figure(figsize=(6, 6))
    nx.draw(
        G, with_labels=True, node_color=node_colors, node_size=800, font_size=12, font_color="black"
    )
    plt.title("Graph Visualization")
    plt.show()

# Define edges for the graph
edges = [(0,1),(1,2),(2,0)]


# Prepare a 2-layer QAOA circuit
def prepare_2_layer(x):
    beta1, beta2, gamma1, gamma2 = x
    qaoa_circ = QAOA_MaxCut_Circuit(num_qubits=3, edges=edges)
    qaoa_circ.add_layer(gamma1, beta1)
    qaoa_circ.add_layer(gamma2, beta2)
    return qaoa_circ

# Define the expectation value computation
def expectation(x, backend):
    circ = prepare_2_layer(x)
    return circ.expectation_val(backend)

# Initial parameters for the optimizer
x0 = np.array([0.1, 0.1, 0.2, 0.3])
emulator = QiskitWrapperEmulator()

# Perform optimization
result = minimize(expectation, x0, args=emulator, options={'maxiter': 500}, method='Powell')
print("Optimized parameters:", result.x)
print("Optimized expectation value:", result.fun)

# Apply the optimized circuit
emu = MyEmulator()
opt_circ = prepare_2_layer(result.x)
num_qubits = opt_circ.num_qubits
vec = StateVector(num_qubits)
vec = emu.apply_circuit(opt_circ, vec)

# Print state vector
print("State vector:", vec.vector)

# Calculate probabilities
probs = np.abs(vec.vector) ** 2
print("State probabilities:", probs)

# Map bitstrings to states
z_basis = [format(i, "b").zfill(num_qubits) for i in range(probs.size)]

# # Plot probability distribution
# fig, ax = plt.subplots()
# ax.set_xlabel("States")
# ax.set_ylabel("Probability (%)")
# ax.bar(z_basis, probs * 100)
# plt.show()


# Visualize the input graph
max_prob_bitstring = z_basis[np.argmax(probs)]
node_colors = ["red" if bit == "0" else "green" for bit in max_prob_bitstring]
visualize_graph(edges, node_colors=node_colors)