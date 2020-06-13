
from orthogonal.doublyConnectedEdgeList.GraphElement import GraphElement


class Vertex(GraphElement):
    def __init__(self, name):
        super().__init__(name)
        self.inc = None  # 'the first outgoing incident half-edge'
        self.x = None
        self.y = None

    def surround_faces(self):  # clockwise, duplicated
        for he in self.surround_half_edges():
            yield he.inc

    def surround_half_edges(self):  # clockwise
        yield self.inc
        he = self.inc.pred.twin
        while he is not self.inc:
            yield he
            he = he.pred.twin

