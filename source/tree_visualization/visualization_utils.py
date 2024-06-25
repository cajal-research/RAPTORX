from typing import List

from igraph import Graph, Layout
from plotly.graph_objs import Figure

from source.raptor.tree_structures import Node, Tree

MAX_CHARS_PER_LINE = 80


def format_text_for_plot(text: str) -> str:
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


def add_sliders(fig: Figure, ticks: List):
    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Frame #",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.01,
        "y": 0,
        "steps": []
    }
    for i in ticks:
        slider_step = {
            "args": [
                [f"frame{i}"],
                {"frame": {"duration": 1000, "redraw": True}, "mode": "immediate", "transition": {"duration": 300}}
            ],
            "label": str(i),
            "method": "animate"
        }
        sliders_dict["steps"].append(slider_step)
    fig.update_layout(sliders=[sliders_dict])


def create_root_node(tree: Tree) -> Node:
    return Node(
        text="Root Node",
        index=-1,
        children=list(map(lambda x: x.index, tree.root_nodes.values())),
        embeddings=[]
    )
