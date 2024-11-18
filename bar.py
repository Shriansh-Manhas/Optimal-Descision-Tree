import matplotlib.pyplot as plt
import numpy as np

# Data for each result
results = {
    'HiCuts': {'bytes_per_rule': 1878.9, 'memory_access': 5, 'num_node': 19304},
    'HyperCuts': {'bytes_per_rule': 2194.5, 'memory_access': 5, 'num_node': 22903},
    'EffiCuts': {'bytes_per_rule': 1765, 'memory_access': 6, 'num_node': 16556},
    'CutSplit': {'bytes_per_rule': 219.24, 'memory_access': 12, 'num_node': 1749},
    'Best Merged Tree': {'bytes_per_rule': 809.63, 'memory_access': 6, 'num_node': 15077}
}

# Extract metrics
algorithms = list(results.keys())
bytes_per_rule = [results[alg]['bytes_per_rule'] for alg in algorithms]
memory_access = [results[alg]['memory_access'] for alg in algorithms]
num_nodes = [results[alg]['num_node'] for alg in algorithms]

# Bar width
bar_width = 0.25
x = np.arange(len(algorithms))

# Create bar graphs
plt.figure(figsize=(15, 5))

# Plot bytes per rule
plt.subplot(1, 3, 1)
plt.bar(x, bytes_per_rule, color='blue', width=bar_width)
plt.xticks(x, algorithms, rotation=45)
plt.ylabel('Bytes per Rule')
plt.title('Bytes per Rule Comparison')

# Plot memory access
plt.subplot(1, 3, 2)
plt.bar(x, memory_access, color='green', width=bar_width)
plt.xticks(x, algorithms, rotation=45)
plt.ylabel('Memory Access')
plt.title('Memory Access Comparison')

# Plot number of nodes
plt.subplot(1, 3, 3)
plt.bar(x, num_nodes, color='orange', width=bar_width)
plt.xticks(x, algorithms, rotation=45)
plt.ylabel('Number of Nodes')
plt.title('Number of Nodes Comparison')

# Show plots
plt.tight_layout()
plt.show()
