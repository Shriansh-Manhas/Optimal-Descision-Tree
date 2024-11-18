import random
import datetime
from tree import Tree, Node

from hicuts import *
from hypercuts import *
from efficuts import *
from cutsplit import *

class HiCutsTreeMerger:
    def __init__(self, tree1, tree2, population_size=90, generations=100, mutation_rate=0.1):
        self.tree1 = tree1
        self.tree2 = tree2
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

    def fitness_function(self, merged_tree):
        """Evaluates the efficiency of the merged tree based on memory and depth."""
        result = merged_tree.compute_result()
        memory_access = result["memory_access"]
        depth = merged_tree.get_depth()
        return -(memory_access + depth)  # lower memory and depth are better

    def merge_nodes(self, node1, node2):
        """Recursively merges two nodes while preserving the original depth."""
        # Base case: If both nodes are leaves, combine their rules
        if not node1.children and not node2.children:
            combined_rules = node1.rules + node2.rules
            return Node(node1.id, node1.ranges, combined_rules, node1.depth, node1.partitions, node1.manual_partition)

        # Otherwise, create a new node with combined rules, keeping the original depth
        merged_rules = node1.rules + node2.rules
        merged_node = Node(node1.id, node1.ranges, merged_rules, node1.depth, node1.partitions, node1.manual_partition)
        
        # Recursively merge each child at the same position in both nodes
        merged_children = []
        max_children = max(len(node1.children), len(node2.children))

        for i in range(max_children):
            if i < len(node1.children) and i < len(node2.children):
                # Recursively merge corresponding children from both nodes
                merged_child = self.merge_nodes(node1.children[i], node2.children[i])
            elif i < len(node1.children):
                # Only node1 has this child; add it as-is
                merged_child = node1.children[i]
            else:
                # Only node2 has this child; add it as-is
                merged_child = node2.children[i]

            merged_children.append(merged_child)

        merged_node.children = merged_children
        return merged_node

    def merge_trees(self, tree1, tree2):
        """Combine two HiCuts trees by merging nodes from both trees recursively."""
        # Create the merged root node by merging the roots of both trees
        merged_root = self.merge_nodes(tree1.root, tree2.root)
        
        # Create the merged tree with combined rules and merged root
        merged_tree = Tree(
            tree1.rules + tree2.rules, tree1.leaf_threshold,
            {"node_merging": True, "rule_overlay": True, "region_compaction": False, "rule_pushup": False, "equi_dense": False}
        )
        merged_tree.root = merged_root
        return merged_tree


    def initialize_population(self):
        """Initialize population with various merges of two trees."""
        return [self.merge_trees(self.tree1, self.tree2) for _ in range(self.population_size)]

    def crossover(self, tree1, tree2):
        """Crossover operation between two trees by swapping sub-nodes."""
        if tree1.root.children and tree2.root.children:
            idx1, idx2 = random.randint(0, len(tree1.root.children)-1), random.randint(0, len(tree2.root.children)-1)
            # Swap a subtree between two trees
            tree1.root.children[idx1], tree2.root.children[idx2] = tree2.root.children[idx2], tree1.root.children[idx1]
        return tree1, tree2

    def mutate(self, tree):
        """Randomly rearrange nodes within a tree to introduce mutation."""
        if tree.root.children:
            idx1, idx2 = random.sample(range(len(tree.root.children)), 2)
            tree.root.children[idx1], tree.root.children[idx2] = tree.root.children[idx2], tree.root.children[idx1]

    def genetic_algorithm(self):
        """Main genetic algorithm to optimize the merge of two HiCuts trees."""
        # Initialize population
        population = self.initialize_population()

        for generation in range(self.generations):
            # Calculate fitness for each chromosome (merged tree)
            fitness_scores = [self.fitness_function(merged_tree) for merged_tree in population]

            # Selection (retain the top half based on fitness)
            population = [tree for _, tree in sorted(zip(fitness_scores, population), key=lambda x: x[0], reverse=True)[:self.population_size//2]]

            # Crossover and Mutation to create new generation
            next_generation = []
            while len(next_generation) < self.population_size:
                # Crossover
                parent1, parent2 = random.sample(population, 2)
                child1, child2 = self.crossover(parent1, parent2)
                next_generation.extend([child1, child2])

                # Mutation
                if random.random() < self.mutation_rate:
                    self.mutate(child1)
                if random.random() < self.mutation_rate:
                    self.mutate(child2)

            population = next_generation  # Move to the next generation

        # Return the best merged tree based on the final fitness
        final_fitness_scores = [self.fitness_function(merged_tree) for merged_tree in population]
        best_tree = population[final_fitness_scores.index(max(final_fitness_scores))]
        return best_tree

# Example of usage with HiCuts algorithm:
rules = load_rules_from_file("classbench/fw2_1k")  # Define the set of rules to be used in both trees

hicuts = HiCuts(rules)
hypercuts = HyperCuts(rules)
efficuts = EffiCuts(rules)
cutsplit = CutSplit(rules)

# Build trees using HiCuts
tree1 = hicuts.build_tree()
tree2 = hypercuts.build_tree(rules)
tree3 = efficuts.build_tree(rules)
tree4 = cutsplit.build_tree(rules, "hypersplit", 0)

print("HiCuts result:", tree1.compute_result())
print("HyperCuts result:", tree2.compute_result())
print("EffiCuts result:", tree3.compute_result())
print("CutSplit result:", tree4.compute_result())

# Merge using genetic algorithm
tree_merger = HiCutsTreeMerger(tree3, tree4)
best_merged_tree = tree_merger.genetic_algorithm()
# Output merged tree stats
print("Best merged tree result:", best_merged_tree.compute_result())
