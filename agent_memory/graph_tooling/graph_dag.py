import ast
import numpy as np
from loguru import logger
from typing import Dict, List, Set, Tuple
import networkx as nx
import matplotlib.pyplot as plt



class GraphDag:
    def __init__(self, checkpoints: dict = None):
        self.checkpoints = checkpoints
        self.graph = nx.DiGraph()

    def build_checkpoints(self):
        for checkpoint in self.checkpoints:
            self.graph.add_node(
                checkpoint.checkpoint_uuid,
                checkpoint_uuid=checkpoint.checkpoint_uuid,
                checkpoint_iterator=checkpoint.checkpoint_iterator,
                checkpoint_description=checkpoint.checkpoint_description,
                checkpoint_review_criteria=checkpoint.checkpoint_review_criteria,
                ready_to_start=False,
                completed=False

            )

        for i in range(len(self.checkpoints) - 1):
            current_checkpoint = self.checkpoints[i]
            next_checkpoint = self.checkpoints[i + 1]
            self.graph.add_edge(
                current_checkpoint.checkpoint_uuid,
                next_checkpoint.checkpoint_uuid,
                dependency_type='checkpoint_step'
            )

        initial_tasks = list(self.find_initial_tasks())
        if initial_tasks:  # Check if there are any initial tasks
            self.graph.nodes[initial_tasks[0]]['ready_to_start'] = True

    def add_execution_steps(self, step_object):

        self.graph.add_node(
            step_object.step_uuid,
            step_function_name=step_object.function_name,
            step_function_signature=step_object.function_signature,
            step_function_execution_start=step_object.execution_start,
            step_function_execution_end=step_object.execution_end,
            step_function_execution_duration=step_object.execution_duration,
            step_function_step_uuid=step_object.step_uuid,
            step_function_checkpoint_uuid=step_object.checkpoint_uuid,
            step_function_previous_step_uuid=step_object.previous_step_uuid,
            step_function_status=step_object.status,
            step_function_function_output=step_object.function_output,
            step_function_rror=step_object.error,
            step_function_cost=step_object.cost,
            step_function_function_output_type=step_object.function_output_type,
            step_function_has_iter=step_object.has_iter,
            step_function_is_empty=step_object.is_empty,
            step_function_has_markdown=step_object.has_markdown,
            step_function_iteration_count=step_object.iteration_count,
            step_state_function_run=step_object.function_output,
            step_state_review=step_object.function_output,
        )

        # Add edge from parent checkpoint to this step
        self.graph.add_edge(
            step_object.checkpoint_uuid,
            step_object.step_uuid,
            dependency_type='checkpoint_parent'
        )

        # Add edge from previous step if it exists and isn't the checkpoint
        if step_object.previous_step_uuid and step_object.previous_step_uuid != step_object.checkpoint_uuid:
            self.graph.add_edge(
                step_object.previous_step_uuid,
                step_object.step_uuid,
                dependency_type='step_sequence'
            )

    def analyze_dependencies(self) -> Dict[str, List[str]]:
        """Analyzes and validates the dependency structure"""
        analysis = {
            "circular_dependencies": self.find_circular_dependencies(),
            "missing_dependencies": self.find_missing_dependencies(),
            "execution_groups": self.generate_execution_groups(),
            "isolated_tasks": self.find_isolated_tasks(),
            "terminal_tasks": self.find_terminal_tasks(),
            "initial_tasks": self.find_initial_tasks()
        }
        return analysis

    def find_circular_dependencies(self) -> List[List[str]]:
        """Identifies any circular dependencies in the graph"""
        try:
            cycles = list(nx.simple_cycles(self.graph))
            return cycles
        except nx.NetworkXNoCycle:
            return []

    def find_missing_dependencies(self) -> List[str]:
        """Identifies referenced dependencies (edges) that point to non-existent nodes"""
        missing = []
        nodes = list(self.graph.nodes())

        for node in nodes:
            for dependency in self.graph.successors(node):
                if dependency not in nodes:
                    missing.append(dependency)

        return missing

    def generate_execution_groups(self) -> List[Set[str]]:
        """Generates execution groups based on dependency structure"""
        if self.find_circular_dependencies():
            raise ValueError("Cannot generate execution groups with circular dependencies")

        execution_groups = []
        remaining_nodes = set(self.graph.nodes())

        while remaining_nodes:
            # Find all nodes that have no dependencies in remaining set
            available = {
                node for node in remaining_nodes
                if not any(pred in remaining_nodes for pred in self.graph.predecessors(node))
            }

            if not available:
                break

            execution_groups.append(available)
            remaining_nodes -= available

        return execution_groups

    def find_isolated_tasks(self) -> Set[str]:
        """Identifies tasks with no dependencies or dependents"""
        return {
            node for node in self.graph.nodes()
            if self.graph.in_degree(node) == 0 and self.graph.out_degree(node) == 0
        }

    def find_terminal_tasks(self) -> Set[str]:
        """Identifies terminal tasks (tasks with no dependents)"""
        return {
            node for node in self.graph.nodes()
            if self.graph.out_degree(node) == 0 and self.graph.in_degree(node) > 0
        }

    def find_initial_tasks(self) -> Set[str]:
        """Identifies initial tasks (tasks with no dependencies)"""
        return {
            node for node in self.graph.nodes()
            if self.graph.in_degree(node) == 0 and self.graph.out_degree(node) > 0
        }

    def get_parallel_execution_paths(self) -> List[List[str]]:
        """
        Identifies groups of nodes that can be executed in parallel.
        Returns a list of lists, where each inner list contains node IDs
        that can be executed in parallel.
        """
        if self.find_circular_dependencies():
            raise ValueError("Cannot determine parallel paths with circular dependencies")

        parallel_paths = []
        for group in self.generate_execution_groups():
            path_group = []
            for node_id in group:
                if node_id in self.graph:  # Check if node exists in graph
                    path_group.append(node_id)
            if path_group:  # Only append non-empty groups
                parallel_paths.append(path_group)

        return parallel_paths

    def get_critical_path(self) -> List[str]:
        """
        Identifies the critical path (longest dependency chain) in the graph.
        Returns a list of node IDs representing the critical path.
        """
        try:
            # Convert graph to weighted graph for critical path
            weighted_graph = self.graph.copy()
            for edge in weighted_graph.edges():
                weighted_graph[edge[0]][edge[1]]['weight'] = -1

            # Find the critical path using longest path in DAG
            critical_path = nx.dag_longest_path(weighted_graph)

            return critical_path

        except nx.NetworkXUnfeasible:
            raise ValueError("Cannot determine critical path in cyclic graph")

    def visualise_mermaid(self) -> str:
        """
        Builds a Mermaid diagram from a NetworkX DiGraph.

        Args:
            graph (nx.DiGraph): The task dependency graph.

        Returns:
            str: Mermaid diagram representation.
        """
        mermaid_lines = ["graph TD"]

        # Add nodes to Mermaid
        for node, attrs in self.graph.nodes(data=True):
            label = attrs.get('checkpoint_description', node)  # Default to node ID if no name
            action_type = attrs.get('action_type', "General")  # Default to "General"
            mermaid_lines.append(f'    {node}["{label} ({action_type})"]')

        # Add edges to Mermaid
        for source, target in self.graph.edges():
            mermaid_lines.append(f'    {source} --> {target}')

        # Optionally style specific nodes (like initial or terminal)
        initial_nodes = {node for node in self.graph.nodes() if self.graph.in_degree(node) == 0}
        terminal_nodes = {node for node in self.graph.nodes() if self.graph.out_degree(node) == 0}

        for node in initial_nodes:
            mermaid_lines.append(f'    style {node} fill:#bbf,stroke:#333,stroke-width:4px,color:black;')

        for node in terminal_nodes:
            mermaid_lines.append(f'    style {node} fill:#fbb,stroke:#333,stroke-width:4px,color:black;')

        return '\n'.join(mermaid_lines)

    def visualise_plt(self):
        plt.figure(figsize=(12, 8))

        # Create layout for the graph
        pos = nx.spring_layout(self.graph, k=1, iterations=50)

        # Draw nodes with different colors based on type (checkpoint vs step)
        checkpoint_nodes = [node for node in self.graph.nodes if 'checkpoint_iterator' in self.graph.nodes[node]]
        step_nodes = [node for node in self.graph.nodes if 'step_function_name' in self.graph.nodes[node]]

        # Draw checkpoint nodes
        nx.draw_networkx_nodes(self.graph, pos,
                               nodelist=checkpoint_nodes,
                               node_color='lightblue',
                               node_size=2000,
                               alpha=0.7)

        # Draw step nodes
        nx.draw_networkx_nodes(self.graph, pos,
                               nodelist=step_nodes,
                               node_color='lightgreen',
                               node_size=2000,
                               alpha=0.7)

        # Draw edges with different colors based on type
        edge_colors = []
        edge_types = []
        for u, v, data in self.graph.edges(data=True):
            if data.get('dependency_type') == 'checkpoint_step':
                edge_colors.append('blue')
                edge_types.append('checkpoint_step')
            elif data.get('dependency_type') == 'step_sequence':
                edge_colors.append('green')
                edge_types.append('step_sequence')
            elif data.get('dependency_type') == 'checkpoint_parent':
                edge_colors.append('red')
                edge_types.append('checkpoint_parent')
            else:
                edge_colors.append('gray')
                edge_types.append('other')

        # Draw edges
        nx.draw_networkx_edges(self.graph, pos,
                               edge_color=edge_colors,
                               arrows=True,
                               arrowsize=20)

        # Add node labels (shortened UUIDs for clarity)
        labels = {node: node[:8] + '...' for node in self.graph.nodes()}
        nx.draw_networkx_labels(self.graph, pos, labels, font_size=8)

        # Add edge labels
        edge_labels = nx.get_edge_attributes(self.graph, 'dependency_type')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels, font_size=6)

        plt.title("Task Dependency Graph", pad=20)
        plt.axis('off')

        # Add legend
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue',
                       markersize=15, label='Checkpoint'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightgreen',
                       markersize=15, label='Step'),
            plt.Line2D([0], [0], color='blue', label='checkpoint Step'),
            plt.Line2D([0], [0], color='green', label='Step Sequence'),
            plt.Line2D([0], [0], color='red', label='Checkpoint Parent')
        ]
        plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))

        plt.tight_layout()
        plt.show()