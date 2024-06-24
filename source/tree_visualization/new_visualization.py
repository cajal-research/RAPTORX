import pickle
from typing import List
import plotly.graph_objects as go
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

        # Create plotly figure
        fig = go.Figure()

        # Add nodes
        x_values = [x_offset for _, _, _, x_offset in self.nodes]
        y_values = [-depth for _, _, depth, _ in self.nodes]  # Invert depth to have root at the top
        colors = ["red" if index in self.special_nodes else "blue" for _, index, _, _ in self.nodes]

        marker_dict = dict(
            symbol="circle",
            size=10,
            color=colors,
            line=dict(color="black", width=1),
        )

        fig.add_trace(go.Scatter(
            x=x_values, y=y_values,
            mode='markers+text',
            marker=marker_dict,
            text=[str(index) for _, index, _, _ in self.nodes],
            hoverinfo='text',
            hovertext=[format_text_for_plot(label) for label in self.labels],
            textposition="top center"
        ))

        # Add edges
        for edge in self.edges:
            x0, y0 = x_values[edge[0]], y_values[edge[0]]
            x1, y1 = x_values[edge[1]], y_values[edge[1]]
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
            plot_bgcolor='white'
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
