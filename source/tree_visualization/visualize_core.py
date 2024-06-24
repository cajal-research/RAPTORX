from typing import Tuple, List

from source.raptor.tree_structures import Node, Tree
import plotly.graph_objects as go
from igraph import Graph

from source.tree_visualization.visualization_utils import format_text_for_plot, add_sliders

# Configuration Constants
MAX_CHARS_PER_LINE = 80
NODE_SHAPE = "circle-dot"
NODE_SIZE = 35
NODE_COLOR = "#6175c1"
NODE_OUTLINE_COLOR = "#000000"
NODE_OUTLINE_THICKNESS = 2
NORMAL_EDGE_COLOR = "rgb(210,210,210)"
NORMAL_EDGE_WIDTH = 2
SPECIAL_NODE_COLOR = "red"
SPECIAL_EDGE_COLOR = "red"
FIGURE_HOVER_INFO = "none"
FIGURE_OPACITY = 0.8
FIGURE_TITLE = "Tree Visualization"
FIGURE_FONT_SIZE = 12
FIGURE_MARGIN_LEFT = 40
FIGURE_MARGIN_RIGHT = 40
FIGURE_MARGIN_BOTTOM = 85
FIGURE_MARGIN_TOP = 100
PLOT_BACKGROUND_COLOR = "rgb(248,248,248)"
WEB_WIDTH = 1700
JUPYTER_WIDTH = 1500


class TreeVisualizer:
    def __init__(self, start_node: Node, tree: Tree, full_path_trail: List[int] = None):
        self.start_node = start_node
        self.tree = tree
        self.full_path_trail = full_path_trail if full_path_trail else []
        self.path_so_far = full_path_trail
        self.graph = Graph()
        self.frames = []
        self.jupyter = False

    def build_graph_from_tree(self, current_node: Node, parent_node_id: int = -1) -> int:
        """
        Recursively builds a graph representation of the tree structure.
        """
        node_id = self.graph.vcount()
        self.graph.add_vertex(
            name=f"• [Node #{current_node.index}]\n{current_node.text}",
            index=current_node.index,
            embeddings=current_node.embeddings,
        )

        if parent_node_id != -1:
            self.graph.add_edge(parent_node_id, node_id)

        for child_index in current_node.children:
            child_node = self.find_node_in_tree(child_index)
            self.build_graph_from_tree(child_node, node_id)

        return node_id

    def find_node_in_tree(self, node_index: int) -> Node:
        """
        Finds a node in the tree by its index.
        """
        for key in self.tree.all_nodes:
            node = self.tree.all_nodes[key]
            if node.index == node_index:
                return node

        raise Exception(f"Node with index {node_index} not found")

    def create_single_frame(self, frame_index: int) -> go.Frame:
        node_index_mapping = {i: vertex['index'] for i, vertex in enumerate(self.graph.vs)}
        edge_coords, node_coords, node_labels, edge_indices, special_edge_indices = (
            self._generate_plotly_coordinates(node_index_mapping))
        fig = self._create_visualization_figure(edge_coords, node_coords, node_labels, edge_indices,
                                                special_edge_indices)

        fig.update_layout(
            title=f"{FIGURE_TITLE} - Frame {frame_index}",
            font_size=FIGURE_FONT_SIZE,
            showlegend=False,
            xaxis=dict(
                showline=False, zeroline=False, showgrid=False, showticklabels=False
            ),
            yaxis=dict(
                showline=False, zeroline=False, showgrid=False, showticklabels=False
            ),
            margin=dict(l=FIGURE_MARGIN_LEFT, r=FIGURE_MARGIN_RIGHT, b=FIGURE_MARGIN_BOTTOM, t=FIGURE_MARGIN_TOP),
            hovermode="closest",
            plot_bgcolor=PLOT_BACKGROUND_COLOR,
            width=JUPYTER_WIDTH if self.jupyter else WEB_WIDTH,
        )
        return fig

    def plot_tree(self, jupyter: bool = False):
        self.build_graph_from_tree(self.start_node)
        paths = [[], [-1], [-1, 37], [-1, 37, 9]]
        frames = self.generate_all_frames(paths)
        fig = frames[0]

        add_sliders(fig, list(range(len(frames))))

        if not jupyter:
            fig.show()
            return

        import plotly.offline as py
        py.init_notebook_mode(connected=True)
        py.iplot(fig)

    def generate_all_frames(self, paths):
        frames = []
        for index, path in enumerate(paths):
            frame = self.create_single_frame(index)
            frames.append(frame)
        return frames

    def _generate_plotly_coordinates(self, node_index_mapping: dict) -> Tuple[list, list, list, list, list]:
        layout = self.graph.layout("rt", root=[0])
        positions = {i: layout[i] for i in range(self.graph.vcount())}
        heights = [layout[i][1] for i in range(self.graph.vcount())]
        max_height = max(heights)

        edge_tuples = [edge.tuple for edge in self.graph.es]
        num_positions = len(positions)
        node_x_coords = [positions[i][0] for i in range(num_positions)]
        node_y_coords = [2 * max_height - positions[i][1] for i in range(num_positions)]
        edge_x_coords = []
        edge_y_coords = []
        edge_indices = []
        special_edge_indices = []

        for edge in edge_tuples:
            edge_x_coords.extend([positions[edge[0]][0], positions[edge[1]][0], None])
            edge_y_coords.extend(
                [
                    2 * max_height - positions[edge[0]][1],
                    2 * max_height - positions[edge[1]][1],
                    None,
                ]
            )
            edge_indices.append(edge)
            origin_node = node_index_mapping[edge[0]]
            target_node = node_index_mapping[edge[1]]
            if origin_node in self.full_path_trail and target_node in self.full_path_trail:
                special_edge_indices.append(edge)

        node_labels = [vertex["name"] for vertex in self.graph.vs]
        edge_coords = [edge_x_coords, edge_y_coords]
        node_coords = [node_x_coords, node_y_coords]
        return edge_coords, node_coords, node_labels, edge_indices, special_edge_indices

    def _create_visualization_figure(self, edge_coords: List[List[float]], node_coords: List[List[float]],
                                     node_labels: List[str], edge_indices: List[Tuple[int, int]],
                                     special_edge_indices: List[Tuple[int, int]]) -> go.Figure:
        """
        Creates a Plotly figure for visualizing nodes and edges.
        """
        edge_x_coords, edge_y_coords = edge_coords
        node_x_coords, node_y_coords = node_coords
        fig = go.Figure()

        # Create a mapping of node positions to their indexes
        node_index_mapping = {i: vertex['index'] for i, vertex in enumerate(self.graph.vs)}

        edge_colors = []
        for edge in edge_indices:
            edge_colors.append(SPECIAL_EDGE_COLOR if edge in special_edge_indices else NORMAL_EDGE_COLOR)

        for i in range(len(edge_x_coords) // 3):
            fig.add_trace(go.Scatter(
                x=edge_x_coords[i * 3:i * 3 + 3], y=edge_y_coords[i * 3:i * 3 + 3], mode="lines",
                line=dict(color=edge_colors[i], width=NORMAL_EDGE_WIDTH),
                hoverinfo=FIGURE_HOVER_INFO
            ))

        if self.path_so_far:
            marker_colors = [SPECIAL_NODE_COLOR if node_index_mapping[i] in self.path_so_far else NODE_COLOR
                             for i in range(len(node_x_coords))]
        else:
            marker_colors = [NODE_COLOR] * len(node_x_coords)

        marker_dict = dict(
            symbol=NODE_SHAPE,
            size=NODE_SIZE,
            color=marker_colors,
            line=dict(color=NODE_OUTLINE_COLOR, width=NODE_OUTLINE_THICKNESS),
        )
        markers_scatter = go.Scatter(
            x=node_x_coords, y=node_y_coords, mode="markers+text", name="nodes", marker=marker_dict,
            hoverinfo="text", opacity=FIGURE_OPACITY,
            text=[str(node_index_mapping[i]) for i in range(len(node_x_coords))],
            hovertext=[format_text_for_plot(label) for label in node_labels],
            textposition="top center"
        )
        fig.add_trace(markers_scatter)

        return fig