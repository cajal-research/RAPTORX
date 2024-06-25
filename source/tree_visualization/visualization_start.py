import pickle
from typing import List, Tuple

import plotly.graph_objects as go
from igraph import Graph, Layout
from source.paths.path_reference import get_tree_pkl_path
from source.raptor.tree_structures import Tree, Node
from source.tree_visualization.visualization_utils import create_root_node, format_text_for_plot, add_sliders, \
    compare_trails

NODE_SIZE = 35
CANVAS_WIDTH = 1500
CANVAS_HEIGHT = 800

DEFAULT_NODE_COLOR = "#6175c1"
DEFAULT_EDGE_COLOR = "rgb(210,210,210)"
HIGHLIGHTED_NODE_COLOR = "red"
HIGHLIGHTED_EDGE_COLOR = "red"

COMMON_PATH_COLOR = "purple"
CORRECT_DECISION_COLOR = "green"
WRONG_DECISION_COLOR = "red"


class TreeVisualizer:
    def __init__(self, tree: Tree):
        self.tree = tree
        self.root_node = create_root_node(tree)
        self.nodes = []
        self.edges = []
        self.labels = []
        self.fig = go.Figure()
        self.node_index_mapping = {}
        self.graph = Graph()
        self.layout = Layout()
        self.x_values = []
        self.y_values = []
        self.max_y_value = 0
        self.common_path = []
        self.correct_decision = []
        self.wrong_decision = []

    def add_node_to_graph(self, node: Node, parent_node_id: int = None):
        """
        Recursively adds nodes from the tree to the graph.
        """
        node_id = len(self.nodes)
        self.nodes.append((node_id, node.index))
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

    def create_igraph_object(self) -> Graph:
        g = Graph(directed=True)

        for node_id, node_index in self.nodes:
            name = f"{format_text_for_plot(self.labels[node_id])}"
            self.node_index_mapping[node_id] = node_index
            vertex_id = g.add_vertex(name=name).index

        for edge in self.edges:
            target, source = edge
            g.add_edge(target, source)
        return g

    def layout_position_calculations(self, graph_object: Graph):
        self.x_values = [self.layout[i][0] for i in range(len(graph_object.vs))]
        self.max_y_value = int(max(self.layout[i][1] for i in range(len(graph_object.vs))))
        self.y_values = [self.max_y_value - self.layout[i][1] for i in range(len(graph_object.vs))]
        y_axis_tick_vals = list(range(self.max_y_value + 1))
        y_axis_tick_text = [f"Layer#{level}" for level in range(self.max_y_value + 1)]
        return y_axis_tick_text, y_axis_tick_vals

    def plot_pipeline(self, actual_path: List[int], expected_path: List[int]):
        self.add_node_to_graph(self.root_node)

        # Create an igraph graph to use the Reingold-Tilford layout
        self.graph = self.create_igraph_object()

        # Get Reingold-Tilford layout
        self.layout = self.graph.layout_reingold_tilford(root=[0])

        y_axis_tick_text, y_axis_tick_vals = self.layout_position_calculations(self.graph)
        self.common_path, self.correct_decision, self.wrong_decision = compare_trails(actual_path, expected_path)
        self.plot_tree(actual_path)

        sliders_ticks = list(range(len(self.fig.frames)))
        add_sliders(self.fig, sliders_ticks)

        # Update layout
        self.fig.update_layout(
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, tickvals=y_axis_tick_vals, ticktext=y_axis_tick_text),
            plot_bgcolor='white',
            autosize=False,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            margin=dict(l=40, r=40, b=40, t=40),
            updatemenus=[dict(type="buttons", buttons=[dict(label="Play", method="animate", args=[None])])]
        )

        self.fig.show()

    def plot_tree(self, special_nodes):
        full_path = self.common_path + self.correct_decision + self.wrong_decision
        frames = []
        for i in range(len(full_path)):
            current_special_nodes = full_path[:i + 1]
            edge_scatter = self.get_edge_scatter(current_special_nodes)
            node_scatter = self.get_node_scatter(current_special_nodes)
            frame_data = edge_scatter + [node_scatter]
            frame = go.Frame(data=frame_data, name=str(i))
            frames.append(frame)

        self.fig.frames = frames

        # Add the initial frame
        self.fig.add_traces(frames[0].data)

    def get_node_scatter(self, special_nodes: List[int]):
        colors = []
        for node in self.nodes:
            current_node = node[1]

            if current_node not in special_nodes:
                colors.append(DEFAULT_NODE_COLOR)
                continue

            if current_node in self.common_path:
                colors.append(COMMON_PATH_COLOR)
            elif current_node in self.correct_decision:
                colors.append(CORRECT_DECISION_COLOR)
            elif current_node in self.wrong_decision:
                colors.append(WRONG_DECISION_COLOR)

        marker_dict = dict(
            symbol="circle",
            size=NODE_SIZE,
            color=colors,
            line=dict(color="black", width=1),
        )

        node_scatter = go.Scatter(
            x=self.x_values, y=self.y_values,
            mode='markers+text',
            marker=marker_dict,
            text=[str(index) for _, index in self.nodes],
            hoverinfo='text',
            hovertext=[vertex["name"] for vertex in self.graph.vs],
            textposition="top center"
        )

        return node_scatter

    def get_edge_scatter(self, special_nodes: List[int]):
        all_edges = [(edge.source, edge.target) for edge in self.graph.es]
        special_edges = self.get_special_edges(all_edges, special_nodes)
        reversed_special_edges = [(self.node_index_mapping[target], self.node_index_mapping[source])
                                  for target, source in special_edges]
        common_path_edges = [(source, target) for source, target in reversed_special_edges
                             if source in self.common_path and target in self.common_path]
        correct_decision_edges = [(source, target) for source, target in reversed_special_edges
                                  if source in self.correct_decision or target in self.correct_decision]
        wrong_decision_edges = [(source, target) for source, target in reversed_special_edges
                                if source in self.wrong_decision or target in self.wrong_decision]
        edge_scatter_pot = []

        for edge in self.graph.es:
            x0, y0 = self.layout[edge.source]
            x1, y1 = self.layout[edge.target]
            y0 = self.max_y_value - y0
            y1 = self.max_y_value - y1

            source = self.node_index_mapping[edge.source]
            target = self.node_index_mapping[edge.target]

            if (source, target) in common_path_edges:
                edge_color = COMMON_PATH_COLOR
            elif (source, target) in correct_decision_edges:
                edge_color = CORRECT_DECISION_COLOR
            elif (source, target) in wrong_decision_edges:
                edge_color = WRONG_DECISION_COLOR
            else:
                edge_color = DEFAULT_EDGE_COLOR
            current_scatter = go.Scatter(x=[x0, x1, None], y=[y0, y1, None], mode='lines',
                                         line=dict(width=1, color=edge_color))
            edge_scatter_pot.append(current_scatter)

        return edge_scatter_pot

    def get_special_edges(self, all_edges: List[Tuple[int, int]], special_nodes: List[int]):
        tree_object_all_edges = [(self.node_index_mapping[source], self.node_index_mapping[target])
                                 for source, target in all_edges]
        tree_object_special_edges = [(source, target) for source, target in tree_object_all_edges
                                     if source in special_nodes and target in special_nodes]
        tree_index_to_graph_index = {v: k for k, v in self.node_index_mapping.items()}
        return [(tree_index_to_graph_index[source], tree_index_to_graph_index[target])
                for source, target in tree_object_special_edges]


def load_cinderella_tree() -> Tree:
    pkl_path = get_tree_pkl_path()
    with open(pkl_path, "rb") as file:
        return pickle.load(file)


def main():
    tree_object = load_cinderella_tree()
    actual_path = [-1, 37, 9]
    expected_path = [-1, 37, 9]
    new_tree_visualizer = TreeVisualizer(tree_object)
    new_tree_visualizer.plot_pipeline(actual_path, expected_path)


if __name__ == '__main__':
    main()
