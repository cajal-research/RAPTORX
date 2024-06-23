"""
    Takes a tree : Tree as an input and creates a tree in real sense to see.
    See more : https://plotly.com/python/tree-plots/
    Usage : visualize_tree_structure(start_node : Node, tree : Tree)
"""
from typing import Tuple, List

from source.raptor.tree_structures import Node, Tree

try:
    import plotly.graph_objects as go
except ImportError as e:
    raise ImportError("`plotly` not installed. Please install using `pip install plotly`")

try:
    from igraph import Graph, EdgeSeq
except ImportError as e:
    raise ImportError("`igraph` not installed. Please install using `pip install igraph`.")

# Configuration Constants
MAX_CHARS_PER_LINE = 80

NODE_SHAPE = "circle-dot"
NODE_SIZE = 35
NODE_COLOR = "#6175c1"
NODE_OUTLINE_COLOR = "#000000"
NODE_OUTLINE_THICKNESS = 2

FIGURE_LINE_COLOR = "rgb(210,210,210)"
FIGURE_LINE_WIDTH = 2
FIGURE_HOVER_INFO = "none"
FIGURE_OPACITY = 0.8
FIGURE_TITLE = "Tree Visualization"
FIGURE_FONT_SIZE = 12
FIGURE_MARGIN_LEFT = 40
FIGURE_MARGIN_RIGHT = 40
FIGURE_MARGIN_BOTTOM = 85
FIGURE_MARGIN_TOP = 100
PLOT_BACKGROUND_COLOR = "rgb(248,248,248)"


def build_graph_from_tree(graph: Graph, current_node: Node, tree: Tree, parent_node_id: int = -1) -> int:
    """
    Recursively builds a graph representation of the tree structure.
    """
    node_id = graph.vcount()
    graph.add_vertex(
        name=f"Node Index: {current_node.index}, Node Text: {current_node.text}",
        index=current_node.index,
        embeddings=current_node.embeddings,
    )

    if parent_node_id != -1:
        graph.add_edge(parent_node_id, node_id)

    for child_index in current_node.children:
        child_node = find_node_in_tree(child_index, tree)
        build_graph_from_tree(graph, child_node, tree, node_id)

    return node_id


def find_node_in_tree(node_index: int, tree: Tree) -> Node:
    """
    Finds a node in the tree by its index.
    """
    for key in tree.all_nodes:
        node = tree.all_nodes[key]
        if node.index == node_index:
            return node

    raise Exception(f"Node with index {node_index} not found")


def visualize_tree_structure(start_node: Node, tree: Tree, jupyter: bool = False, special_nodes: list[int] = None):
    """
    Visualizes the tree structure using iGraph and Plotly.
    """
    graph = Graph()
    build_graph_from_tree(graph, start_node, tree)

    node_index_mapping = {i: vertex['index'] for i, vertex in enumerate(graph.vs)}
    edge_coords, node_coords, node_labels, edge_indices, special_edge_indices = (
        _generate_plotly_coordinates(graph, special_nodes, node_index_mapping))
    fig = _create_visualization_figure(edge_coords, node_coords, node_labels, special_nodes, graph, edge_indices,
                                       special_edge_indices)

    fig.update_layout(
        title=FIGURE_TITLE,
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
        width=1500 if jupyter else 1000,
    )

    if not jupyter:
        fig.show()
        return

    import plotly.offline as py
    py.init_notebook_mode(connected=True)
    py.iplot(fig)


def _generate_plotly_coordinates(input_graph: Graph, special_nodes: List[int], node_index_mapping: dict) -> Tuple[
    list, list, list, list, list]:
    layout = input_graph.layout("rt", root=[0])
    positions = {i: layout[i] for i in range(input_graph.vcount())}
    heights = [layout[i][1] for i in range(input_graph.vcount())]
    max_height = max(heights)

    edge_tuples = [edge.tuple for edge in input_graph.es]
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
        if origin_node in special_nodes and target_node in special_nodes:
            special_edge_indices.append(edge)

    node_labels = [vertex["name"] for vertex in input_graph.vs]
    edge_coords = [edge_x_coords, edge_y_coords]
    node_coords = [node_x_coords, node_y_coords]
    return edge_coords, node_coords, node_labels, edge_indices, special_edge_indices


def _create_visualization_figure(edge_coords: List[List[float]], node_coords: List[List[float]], node_labels: List[str],
                                 special_nodes: List[int], graph: Graph, edge_indices: List[Tuple[int, int]],
                                 special_edge_indices: List[Tuple[int, int]]) -> go.Figure:
    """
    Creates a Plotly figure for visualizing nodes and edges.
    """
    edge_x_coords, edge_y_coords = edge_coords
    node_x_coords, node_y_coords = node_coords
    fig = go.Figure()

    special_edges_color = "red"
    normal_edges_color = FIGURE_LINE_COLOR

    # Create a mapping of node positions to their indexes
    node_index_mapping = {i: vertex['index'] for i, vertex in enumerate(graph.vs)}

    edge_colors = []
    for edge in edge_indices:
        if edge in special_edge_indices:
            edge_colors.append(special_edges_color)
        else:
            edge_colors.append(normal_edges_color)

    for i in range(len(edge_x_coords) // 3):
        fig.add_trace(go.Scatter(
            x=edge_x_coords[i * 3:i * 3 + 3], y=edge_y_coords[i * 3:i * 3 + 3], mode="lines",
            line=dict(color=edge_colors[i], width=FIGURE_LINE_WIDTH),
            hoverinfo=FIGURE_HOVER_INFO
        ))

    special_nodes_color = "red"

    # Check if the node index is in special_nodes
    marker_colors = [
        NODE_COLOR if node_index_mapping[i] not in special_nodes else special_nodes_color
        for i in range(len(node_x_coords))
    ] if special_nodes else [NODE_COLOR] * len(node_x_coords)

    marker_dict = dict(
        symbol=NODE_SHAPE,
        size=NODE_SIZE,
        color=marker_colors,
        line=dict(color=NODE_OUTLINE_COLOR, width=NODE_OUTLINE_THICKNESS),
    )
    markers_scatter = go.Scatter(
        x=node_x_coords, y=node_y_coords, mode="markers", name="nodes", marker=marker_dict,
        hoverinfo="text", opacity=FIGURE_OPACITY,
        text=[_format_text_for_plot(label) for label in node_labels],
    )
    fig.add_trace(markers_scatter)

    return fig


def _format_text_for_plot(text: str) -> str:
    """
    Formats text for plotting by splitting long lines into shorter ones.
    """
    lines = text.split("\n")
    formatted_lines = []
    for line in lines:
        while len(line) > MAX_CHARS_PER_LINE:
            formatted_lines.append(line[:MAX_CHARS_PER_LINE])
            line = line[MAX_CHARS_PER_LINE:]
        formatted_lines.append(line)

    return "<br>".join(formatted_lines)
