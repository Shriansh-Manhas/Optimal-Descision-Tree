
# Genetic Algorithm-Optimized Merged Tree

This repository presents the **Genetic Algorithm (GA)-optimized merged tree**, a novel approach for optimizing classification trees. The GA-merged tree demonstrates competitive performance across various metrics when compared to traditional methods such as HiCuts, HyperCuts, EffiCuts, and CutSplit.

## Performance Summary

The GA-merged tree balances memory usage, memory access, and the number of nodes to achieve efficient classification. Below is a detailed comparison:

### Key Metrics

- **Bytes per Rule:**
  - The GA-merged tree achieves a lower `bytes_per_rule` metric compared to HiCuts, HyperCuts, and EffiCuts.
  - This indicates superior memory efficiency.
  
- **Memory Access:**
  - It outperforms HyperCuts and EffiCuts but is slightly slower than HiCuts.
  - Matches the performance of CutSplit.

- **Number of Nodes:**
  - The total number of nodes in the GA-merged tree is more optimized than HiCuts, HyperCuts, and EffiCuts.
  - However, it is slightly higher than CutSplit.

## Why CutSplit Outperforms the GA-Merged Tree

While the GA-merged tree performs competitively, CutSplit has a specialized structure that provides certain advantages:

- Minimal memory footprint.
- Efficient rule partitioning.
- Refined splitting strategies to:
  - Minimize the number of leaf and non-leaf nodes.
  - Reduce memory requirements (bytes per rule).
  - Optimize the total number of nodes for highly efficient lookup performance.
 

### To run the code
python genetic_algorithm.py
