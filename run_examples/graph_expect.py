from qaoa import QAOA_MaxCut_Circuit
from scipy.optimize import minimize
import numpy as np
from emulator import MyEmulator
from qiskit_wrapper import QiskitWrapperEmulator
from statevector import StateVector
import matplotlib.pyplot as plt
import networkx as nx 

NUM_LAYERS = 2


edges = []
# Open and read the file
for i in range(15):
    for j in range(i+1,15):
        f = np.random.binomial(1,0.5)
        if (f>0):
            edges.append((i,j))


# with open("el.txt", "r") as file:
#     for line in file:
#         # Split each line into two integers and add as a tuple to the edges list
#         node1, node2 = map(int, line.split())
#         edges.append((node1, node2))

print(edges)
num_qubits = max(index for edge in edges for index in edge) + 1
emulator = QiskitWrapperEmulator()


def prepare_circuit(x):
    qaoa_circ = QAOA_MaxCut_Circuit(num_qubits=num_qubits, edges=edges)
    for layer in range(NUM_LAYERS):
        beta = x[2 * layer]
        gamma = x[2 * layer + 1]
        qaoa_circ.add_layer(beta, gamma)
    return qaoa_circ

def expectation(x, backend = emulator, shots = None):
    circ = prepare_circuit(x)
    return circ.expectation_val(backend, shots)

def get_probs(x):
    emu = MyEmulator()
    opt_circ = prepare_circuit(x)
    vec = emu.apply_circuit(
        opt_circ,
        StateVector(opt_circ.num_qubits)
    )
    return np.abs(vec.vector)**2

        
# """
# Honest expectation <Ψ|H|Ψ>
# """
# expectations_honest = list()
# probs_honest = list()
# x = np.array([435, -344,52, 332,35,22])
# for i in range(n_iter):

#     result = minimize(expectation, x, 
#                       args = (emulator, None), 
#                       options={'maxiter': 1},
#                       method='powell')
#     x, fun = result.x, result.fun
#     expectations_honest.append(fun)
#     probs_honest.append(get_probs(x))

"""
Sumulated measurement <Ψ|H|Ψ>
"""

histories  = dict()
circ = QAOA_MaxCut_Circuit(edges=edges, num_qubits=num_qubits)
exact = -circ.get_exact_result()[0]
print(exact)


MAX_NUM_SHOTS_LOG = 2
MAX_LAUNCHES_COUNT = 10
MAX_ITER = 3



histories = dict()
times_histories = dict()

for NUM_SHOTS in range(1,21,4):

    history = [0]
    times = [0]

    for LAUNCHES_COUNT in np.arange(MAX_LAUNCHES_COUNT):

        print(LAUNCHES_COUNT)
        x0 = np.random.uniform(0, 2 * np.pi, size = 2 * NUM_LAYERS)
        result = minimize(expectation, x0 = x0,
                            args=(emulator, NUM_SHOTS),
                            options={'maxiter': MAX_ITER},
                            method='powell')
        
        print(f"fun {result.nfev}")
        history.append(-result.fun)
        times.append(times[-1] + result.nfev)
    
    print(history)
    histories[NUM_SHOTS] = history  
    times_histories[NUM_SHOTS] = times  


fig, (ax1, ax2) = plt.subplots(ncols=2)

for NUM_SHOTS, history in histories.items():
    times = times_histories[NUM_SHOTS]
    ax1.plot(np.array(times)*NUM_SHOTS, np.maximum.accumulate(history), label=f"NUM_SHOTS={NUM_SHOTS}")

ax1.axhlines(y=exact, xmin=0, xmax=1, ls = ":", color = "red")
ax1.grid()
# Add labels, title, and legend
ax1.set_title('Optimization Progress for Different NUM_SHOTS')
ax1.legend(title='NUM_SHOTS')



G = nx.Graph()
G.add_edges_from(edges)

# Default node colors if not provided
node_colors = ["lightblue"] * len(G.nodes)

nx.draw(
    G, ax=ax2, 
    with_labels=True,
    node_color=node_colors, node_size=800, font_size=12, font_color="black"
)

# Show the plot  bn Aw
plt.grid(True)
plt.show()

    
# fig, (ax, ax2, ax3) = plt.subplots(nrows=3, ncols=1, sharex=True, constrained_layout = True)

# ax.set_ylabel("<Ψ|H|Ψ>")
# ax.plot(expectations_stat, label = "Measurement statistic")
# ax.plot(expectations_honest, label = "<Ψ|H|Ψ>")
# #ax.set_xlabel("Iter")
# ax.grid()
# ax.legend()

# N = len(probs_stat[0])
# n = int(np.log2(N))
# z_basis = [format(i,"b").zfill(n) for i in range(N)]

# ax2.imshow(np.transpose(probs_stat), interpolation="hamming")
# ax2.set_title("by statistic")
# ax2.set_yticks(range(N), z_basis)
# ax3.imshow(np.transpose(probs_honest), interpolation="hamming")
# ax3.set_title("by <Ψ|H|Ψ>")
# ax3.set_yticks(range(N), z_basis)

# plt.show()
