import pickle
from typing import List

import plotly.graph_objects as go
from igraph import Graph
from source.paths.path_reference import get_tree_pkl_path
from source.raptor.tree_structures import Tree, Node
from source.tree_visualization.visualization_utils import create_root_node, format_text_for_plot


class NewTreeVisualizer:
    def __init__(self, tree: Tree):
        self.tree = tree
        self.root_node = create_root_node(tree)
        self.nodes = []
        self.edges = []
        self.labels = []
        self.special_nodes = []

    def add_node_to_graph(self, node: Node, parent_node_id: int = None, depth: int = 0, x_offset: int = 0):
        """
        Recursively adds nodes from the tree to the graph.
        """
        node_id = len(self.nodes)
        self.nodes.append((node_id, node.index, depth, x_offset))
        self.labels.append(f"Node #{node.index}<br>{format_text_for_plot(node.text)}")

        if parent_node_id is not None:
            self.edges.append((parent_node_id, node_id))

        child_x_offset = x_offset
        for child_index in node.children:
            child_node = self.get_node_by_index(child_index)
            self.add_node_to_graph(child_node, node_id, depth + 1, child_x_offset)
            child_x_offset += 1

        return node_id

    def get_node_by_index(self, node_index: int) -> Node:
        """
        Retrieves a node from the tree by its index.
        """
        try:
            return next(node for node in self.tree.all_nodes.values() if node.index == node_index)
        except StopIteration:
            raise KeyError(f"Node with index {node_index} not found")

    def highlight_nodes(self, trail: List[int]):
        self.special_nodes = trail

    def plot_tree(self):
        self.add_node_to_graph(self.root_node)

        # Create an igraph graph to use the Reingold-Tilford layout
        g = Graph(directed=True)
        for node_id, node_index, _, _ in self.nodes:
            g.add_vertex(name=f"Node #{node_index}<br>{format_text_for_plot(self.labels[node_id])}")
        for edge in self.edges:
            g.add_edge(edge[0], edge[1])

        # Get Reingold-Tilford layout
        layout = g.layout_reingold_tilford(root=[0])

        # Calculate x and y values
        x_values = [layout[i][0] for i in range(len(g.vs))]
        max_y_value = max(layout[i][1] for i in range(len(g.vs)))
        y_values = [max_y_value - layout[i][1] for i in range(len(g.vs))]  # Flip y-axis

        colors = ["red" if node[1] in self.special_nodes else "blue" for node in self.nodes]

        marker_dict = dict(
            symbol="circle",
            size=20,  # Increase node size
            color=colors,
            line=dict(color="black", width=1),
        )

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=x_values, y=y_values,
            mode='markers+text',
            marker=marker_dict,
            text=[str(index) for _, index, _, _ in self.nodes],
            hoverinfo='text',
            hovertext=[vertex["name"] for vertex in g.vs],
            textposition="top center"
        ))

        # Add edges
        for edge in g.es:
            x0, y0 = layout[edge.source]
            x1, y1 = layout[edge.target]
            y0 = max_y_value - y0  # Flip y-axis for edges
            y1 = max_y_value - y1  # Flip y-axis for edges
            fig.add_trace(go.Scatter(
                x=[x0, x1, None], y=[y0, y1, None],
                mode='lines',
                line=dict(width=1, color='gray')
            ))

        # Update layout
        fig.update_layout(
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False),
            plot_bgcolor='white',
            autosize=False,
            width=1200,
            height=800,
            margin=dict(l=40, r=40, b=40, t=40),
        )

        fig.show()


def main():
    pkl_path = get_tree_pkl_path()
    with open(pkl_path, "rb") as file:
        tree_object = pickle.load(file)

    trail = [-1, 37, 9]
    new_tree_visualizer = NewTreeVisualizer(tree_object)
    new_tree_visualizer.highlight_nodes(trail)
    new_tree_visualizer.plot_tree()


if __name__ == '__main__':
    main()