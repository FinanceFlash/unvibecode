import json


def render_map(tmp_path):
    from unvibecode_graph.render import (
        _write_html,
    )  # a package now, not a script to exec

    class Graph:
        def generate_html(self, notebook=False):
            return '<html><head></head><body><div id="mynetwork"></div></body></html>'

    path = tmp_path / "map.html"
    _write_html(Graph(), path, context_store_filename="context.js")
    return path.read_text(encoding="utf-8")


class Network:
    last = None

    def __init__(self, **kwargs):
        self.nodes = []
        self.edges = []
        Network.last = self

    def set_options(self, s):
        self.options = json.loads(s)

    def add_node(self, id, **kwargs):
        self.nodes.append(dict(id=id, **kwargs))

    def add_edge(self, source, target, **kwargs):
        self.edges.append(dict(from_=source, to=target, **kwargs))

    def generate_html(self, **kwargs):
        return '<html><head></head><body><div id="mynetwork"></div></body></html>'
