import pickle
from typing import List

import plotly.graph_objects as go
from igraph import Graph
from source.paths.path_reference import get_tree_pkl_path
from source.raptor.tree_structures import Tree, Node
from source.tree_visualization.visualization_utils import create_root_node, format_text_for_plot

NODE_SIZE = 35
CANVAS_WIDTH = 1500
CANVAS_HEIGHT = 800

DEFAULT_NODE_COLOR = "#6175c1"
DEFAULT_EDGE_COLOR = "rgb(210,210,210)"
HIGHLIGHTED_NODE_COLOR = "red"
HIGHLIGHTED_EDGE_COLOR = "red"


class NewTreeVisualizer:
    def __init__(self, tree: Tree):
        self.tree = tree
        self.root_node = create_root_node(tree)
        self.nodes = []
        self.edges = []
        self.labels = []
        self.fig = go.Figure()
        self.node_index_mapping = {}

    def add_node_to_graph(self, node: Node, parent_node_id: int = None):
        """
        Recursively adds nodes from the tree to the graph.
        """
        node_id = len(self.nodes)
        self.nodes.append((node_id, node.index))
        # self.node_index_mapping[node.index] = node_id
        self.labels.append(f"Node #{node.index}<br>{format_text_for_plot(node.text)}")

        if parent_node_id is not None:
            self.edges.append((parent_node_id, node_id))

        for child_index in node.children:
            child_node = self.get_node_by_index(child_index)
            self.add_node_to_graph(child_node, node_id)

        return node_id

    def get_node_by_index(self, node_index: int) -> Node:
        """
        Retrieves a node from the tree by its index.
        """
        try:
            return next(node for node in self.tree.all_nodes.values() if node.index == node_index)
        except StopIteration:
            raise KeyError(f"Node with index {node_index} not found")

    def create_igraph_object(self):
        g = Graph(directed=True)

        for node_id, node_index in self.nodes:
            name = f"{format_text_for_plot(self.labels[node_id])}"
            self.node_index_mapping[node_id] = node_index
            vertex_id = g.add_vertex(name=name).index

        for edge in self.edges:
            target, source = edge
            g.add_edge(target, source)
        return g

    def plot_tree(self, special_nodes: List[int]):
        self.add_node_to_graph(self.root_node)

        # Create an igraph graph to use the Reingold-Tilford layout
        g = self.create_igraph_object()

        # Get Reingold-Tilford layout
        layout = g.layout_reingold_tilford(root=[0])

        # Calculate x and y values
        x_values = [layout[i][0] for i in range(len(g.vs))]
        max_y_value = max(layout[i][1] for i in range(len(g.vs)))
        y_values = [max_y_value - layout[i][1] for i in range(len(g.vs))]

        self.plot_edges(layout, max_y_value, g, special_nodes)
        self.plot_nodes(x_values, y_values, g, special_nodes)

        # Update layout
        self.fig.update_layout(
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False),
            plot_bgcolor='white',
            autosize=False,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            margin=dict(l=40, r=40, b=40, t=40),
        )

        self.fig.show()

    def plot_nodes(self, x_values: List[float], y_values: List[float], igraph_graph: Graph, special_nodes: List[int]):
        colors = [HIGHLIGHTED_NODE_COLOR if node[1] in special_nodes else DEFAULT_NODE_COLOR for node in
                  self.nodes]

        marker_dict = dict(
            symbol="circle",
            size=NODE_SIZE,
            color=colors,
            line=dict(color="black", width=1),
        )

        node_scatter = go.Scatter(
            x=x_values, y=y_values,
            mode='markers+text',
            marker=marker_dict,
            text=[str(index) for _, index in self.nodes],
            hoverinfo='text',
            hovertext=[vertex["name"] for vertex in igraph_graph.vs],
            textposition="top center"
        )

        self.fig.add_trace(node_scatter)

    def plot_edges(self, layout: List[List[float]], max_y_value: float, igraph_graph: Graph, special_nodes: List[int]):
        all_edges = [(edge.source, edge.target) for edge in igraph_graph.es]
        mapped_edges = [(self.node_index_mapping[source], self.node_index_mapping[target]) for source, target in
                        all_edges]
        special_edges = [(source, target) for source, target in mapped_edges
                         if source in special_nodes and target in special_nodes]
        reverse_map = {v: k for k, v in self.node_index_mapping.items()}
        unmapped_edges = [(reverse_map[source], reverse_map[target]) for source, target in special_edges]

        for edge in igraph_graph.es:
            x0, y0 = layout[edge.source]
            x1, y1 = layout[edge.target]
            y0 = max_y_value - y0  # Flip y-axis for edges
            y1 = max_y_value - y1  # Flip y-axis for edges

            edge_color = HIGHLIGHTED_EDGE_COLOR if (edge.source, edge.target) in unmapped_edges else DEFAULT_EDGE_COLOR

            self.fig.add_trace(go.Scatter(
                x=[x0, x1, None], y=[y0, y1, None],
                mode='lines',
                line=dict(width=1, color=edge_color)
            ))


def main():
    pkl_path = get_tree_pkl_path()
    with open(pkl_path, "rb") as file:
        tree_object = pickle.load(file)

    trail = [-1, 37, 9]
    new_tree_visualizer = NewTreeVisualizer(tree_object)
    new_tree_visualizer.plot_tree(trail)


if __name__ == '__main__':
    main()
