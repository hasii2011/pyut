
import networkx as nx


class GraphElement:
    def __init__(self, name):
        self.id = name

    def __hash__(self):
        return hash(self.id)


class Hedge(GraphElement):
    def __init__(self, name):
        super().__init__(name)
        self.inc  = None    # the incident face'
        self.twin = None
        self.ori  = None
        self.pred = None
        self.succ = None

    def get_points(self):
        return self.ori.id, self.twin.ori.id

    def set_all(self, twin, ori, pred, succ, inc):
        self.twin = twin
        self.ori = ori
        self.pred = pred
        self.succ = succ
        self.inc = inc


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


class Face(GraphElement):
    def __init__(self, name):
        super().__init__(name)
        self.inc = None  # the first half-edge incident to the face from left
        self.nodes_id = []

    def __len__(self):
        return len(self.nodes_id)

    def __repr__(self):
        return f'FaceView{repr(self.nodes_id)}'

    def update_nodes(self):
        self.nodes_id = [vertex.id for vertex in self.surround_vertices()]

    def surround_faces(self):   # clockwise, duplicated!!
        for he in self.surround_half_edges():
            yield he.twin.inc

    def surround_half_edges(self):  # clockwise
        yield self.inc
        he = self.inc.succ
        while he is not self.inc:
            yield he
            he = he.succ

    def surround_vertices(self):
        for he in self.surround_half_edges():
            yield he.ori


class Dcel:
    def __init__(self, G, embedding):

        assert nx.check_planarity(G)[0]

        self.vertex_dict = {}
        for node in G.nodes:
            self.vertex_dict[node] = Vertex(node)

        self.half_edge_dict = {}
        for u, v in G.edges:
            he1, he2 = Hedge((u, v)), Hedge((v, u))
            self.half_edge_dict[he1.id] = he1
            self.half_edge_dict[he2.id] = he2
            he1.twin = he2
            he1.ori = self.vertex_dict[u]
            self.vertex_dict[u].inc = he1

            he2.twin = he1
            he2.ori = self.vertex_dict[v]
            self.vertex_dict[v].inc = he2

        for he in self.half_edge_dict.values():
            u, v = he.get_points()
            he.succ = self.half_edge_dict[embedding.next_face_half_edge(u, v)]
            he.succ.pred = he

        self.face_dict = {}
        for he in self.half_edge_dict.values():
            if not he.inc:
                face_id = f'f{len(self.face_dict)}'
                face = Face(face_id)
                face.inc = he
                self.face_dict[face_id] = face

                face.nodes_id = embedding.traverse_face(*he.get_points())
                for v1_id, v2_id in zip(face.nodes_id, face.nodes_id[1:]+face.nodes_id[:1]):
                    other = self.half_edge_dict[v1_id, v2_id]
                    assert not other.inc
                    other.inc = face

        if not self.face_dict:
            self.face_dict['f0'] = Face('f0')

    def add_node_between(self, u: 'id', v: 'id', node_name):
        def insert_node(u, v, mid_vertice):
            he = self.half_edge_dict.pop((u, v))
            he1 = Hedge((u, mid_vertice.id))
            he2 = Hedge((mid_vertice.id, v))
            # update half_edge_dict
            self.half_edge_dict[u, mid_vertice.id] = he1
            self.half_edge_dict[mid_vertice.id, v] = he2
            he1.set_all(None, he.ori, he.pred, he2, he.inc)
            he2.set_all(None, mid_vertice, he1, he.succ, he.inc)
            he1.pred.succ = he1
            he2.succ.pred = he2
            # update face
            if he.inc.inc is he:
                he.inc.inc = he1
            he.inc.update_nodes() # not efficient

        # update vertex_dict
        mid_vertice = Vertex(node_name)
        self.vertex_dict[node_name] = mid_vertice
        # insert
        insert_node(u, v, mid_vertice)
        insert_node(v, u, mid_vertice)
        for v1, v2 in ((u, mid_vertice.id), (mid_vertice.id, v)):
            self.half_edge_dict[v1, v2].twin = self.half_edge_dict[v2, v1]
            self.half_edge_dict[v2, v1].twin = self.half_edge_dict[v1, v2]
