from IPython.display import display
from langchain_core.runnables.graph import MermaidDrawMethod
from langgraph.graph.state import CompiledGraph


def save_graph_as_png(app: CompiledGraph, output_file_path="graph.png") -> None:
    png_image = app.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)
    with open(output_file_path, "wb") as f:
        f.write(png_image)


def display_graph(app: CompiledGraph) -> None:
    display(app.get_graph().draw_mermaid())
