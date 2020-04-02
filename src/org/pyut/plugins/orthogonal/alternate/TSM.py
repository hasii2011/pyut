import collections as coll
import copy
import math as m

import networkx as nx

import DCEL

import matplotlib.pyplot as plt


def convert_pos_to_embdeding(G, pos):
    '''only straight line in G.
    '''
    emd = nx.PlanarEmbedding()
    for node in G:
        neigh_pos = {
            neigh: (pos[neigh][0]-pos[node][0], pos[neigh][1]-pos[node][1]) for neigh in G[node]
        }
        neighes_sorted = sorted(G.adj[node],
                                key=lambda v: m.atan2(
                                    neigh_pos[v][1], neigh_pos[v][0])
                                )  # counter clockwise
        last = None
        for neigh in neighes_sorted:
            emd.add_half_edge_ccw(node, neigh, last)
            last = neigh
    emd.check_structure()
    return emd


def number_of_cross(G, pos, print_it=False):
    '''
    not accurate, may be equal to actual number or double
    '''
    def is_cross(pa, pb, pc, pd):
        def xmul(v1, v2):
            return v1[0] * v2[1] - v1[1] * v2[0]

        def f(pa, pb, p):
            return (pa[1] - pb[1]) * (p[0] - pb[0]) - (p[1] - pb[1]) * (pa[0] - pb[0])

        ca = (pa[0] - pc[0], pa[1] - pc[1])
        cb = (pb[0] - pc[0], pb[1] - pc[1])
        cd = (pd[0] - pc[0], pd[1] - pc[1])
        return xmul(ca, cd) >= 0 and xmul(cd, cb) >= 0 and f(pa, pb, pc) * f(pa, pb, pd) < 0
    count = 0
    for a, b in G.edges:
        for c, d in G.edges:
            if a not in (c, d) and b not in (c, d):
                if is_cross(pos[a], pos[b], pos[c], pos[d]):
                    count += 1
                    if print_it:
                        print(a, b, c, d)
    return count


class Flow_net(nx.MultiDiGraph):
    def add_v2f(self, v, f, key):
        self.add_edge(v, f, key=key, lowerbound=1, capacity=4, weight=0)

    def add_f2f(self, f1, f2, key):
        # if not self.has_edge(f1, f2):
        self.add_edge(f1, f2, key=key, lowerbound=0, capacity=2**32, weight=1)

    def add_v(self, v):
        self.add_node(v, demand=-4) # the total degree around a node is 2pi

    def add_f(self, f, degree, is_external):
        # the degree of a face is the length of the cycle bounding the face.
        self.add_node(f, demand=(2 * degree + 4) if is_external else (2 * degree - 4))

    def min_cost_flow(self):
        def get_demand(flow_dict, node):
            in_flow = sum(flow_dict[u][v][key]
                          for u, v, key in self.in_edges(node, keys=True))
            out_flow = sum(flow_dict[u][v][key]
                           for u, v, key in self.out_edges(node, keys=True))
            return in_flow - out_flow

        def split(multi_flowG):
            base_dict = coll.defaultdict(lambda: coll.defaultdict(dict))
            new_mdg = nx.MultiDiGraph()

            for u, v, key in multi_flowG.edges:
                lowerbound = multi_flowG[u][v][key]['lowerbound']
                base_dict[u][v][key] = lowerbound
                new_mdg.add_edge(u, v, key,
                                          capacity=multi_flowG[u][v][key]['capacity'] - lowerbound,
                                          weight=multi_flowG[u][v][key]['weight'],
                                          )
            for node in multi_flowG:
                new_mdg.nodes[node]['demand'] =  \
                    multi_flowG.nodes[node]['demand'] - \
                    get_demand(base_dict, node)
            return base_dict, new_mdg

        base_dict, new_mdg = split(self)
        flow_dict = nx.min_cost_flow(new_mdg)
        for u, v, key in self.edges:
            flow_dict[u][v][key] += base_dict[u][v][key]

        self.cost = self.cost_of_flow(flow_dict)
        return flow_dict

    def cost_of_flow(self, flow_dict):
        cost = 0
        for u, v, key in self.edges:
            cost += flow_dict[u][v][key] * self[u][v][key]['weight']
        return cost


class Planarization:
    '''This step determines the topology of the drawing which is described by a planar embedding.
    '''

    def __init__(self, G, pos=None):
        assert nx.number_of_selfloops(G) == 0
        assert nx.is_connected(G)
        if pos is None:
            is_planar, self.embedding = nx.check_planarity(G)
            assert is_planar
            pos = nx.combinatorial_embedding_to_pos(self.embedding)
        else:
            assert number_of_cross(G, pos) == 0
            self.embedding = convert_pos_to_embdeding(G, pos)

        self.G = G.copy()
        self.pos = pos # is only used to find the ext_face now.
        self.dcel = DCEL.Dcel(G, self.embedding)
        self.ext_face = self.get_external_face()

    def copy(self):
        new_planar = self.__new__(self.__class__)
        new_planar.__init__(self.G, self.pos)
        return new_planar

    def get_external_face(self):
        def left_most(G, pos):
            corner_node = min(pos, key=lambda k: (pos[k][0], pos[k][1]))
            other = max(
                G.adj[corner_node], key=lambda node:
                (pos[node][1] - pos[corner_node][1]) /
                m.hypot(
                    pos[node][0] - pos[corner_node][0],
                    pos[node][1] - pos[corner_node][1]
                )
            )  # maximum cosine value
            return sorted([corner_node, other], key=lambda node:
                          (pos[node][1], pos[node][0]))

        if len(self.pos) < 2:
            return list(self.dcel.face_dict.values())[0]
        down, up = left_most(self.G, self.pos)
        return self.dcel.half_edge_dict[up, down].inc

    def dfs_face_order(self):  # dfs dual graph, starts at ext_face
        def dfs_face(face, marked):
            marked.add(face.id)
            yield face
            for neighbor_face in set(face.surround_faces()):
                if neighbor_face.id not in marked:
                    yield from dfs_face(neighbor_face, marked)
        yield from dfs_face(self.ext_face, set())


class Orthogonalization:
    '''
    works on a planar embedding, changes shape of the graph.
    '''

    def __init__(self, planar):
        assert max(pair[1] for pair in planar.G.degree) <= 4
        assert planar.G.number_of_nodes() > 1

        self.planar = planar

        self.flow_network = self.face_determination()
        self.flow_dict = self.tamassia_orthogonalization()

    def face_determination(self):
        flow_network = Flow_net()

        for vertex in self.planar.dcel.vertex_dict.values():
            flow_network.add_v(vertex.id)

        for face in self.planar.dcel.face_dict.values():
            flow_network.add_f(face.id, len(face), face is self.planar.ext_face)

        for vertex in self.planar.dcel.vertex_dict.values():
            for he in vertex.surround_half_edges():
                flow_network.add_v2f(vertex.id, he.inc.id, he.id)

        for he in self.planar.dcel.half_edge_dict.values():
            flow_network.add_f2f(he.twin.inc.id, he.inc.id, he.id) # lf -> rf


        return flow_network

    def tamassia_orthogonalization(self):
        return self.flow_network.min_cost_flow()

    def lp_solve(self, weight_of_corner=1, weight_of_sym=0, sym_pairs=None,
                 # trans=lambda s: s if s[0] != '(' else eval(s.replace('_', ' ')),
                 ):
        '''alert: pulp will automatically transfer node's name into str and replace some special
        chars into '_', and will throw a error if there are variables' name duplicated.
        '''
        import pulp

        prob = pulp.LpProblem()  # minimize

        var_dict = coll.defaultdict(lambda: coll.defaultdict(dict))

        for u, v, he_id in self.flow_network.edges:
            var_dict[u][v][he_id] = pulp.LpVariable(
                f'{u}%{v}%{he_id}',
                self.flow_network[u][v][he_id]['lowerbound'],
                self.flow_network[u][v][he_id]['capacity'],
                pulp.LpInteger
            )

        objs = []
        for he in self.planar.dcel.half_edge_dict.values():
            lf, rf = he.twin.inc.id, he.inc.id
            objs.append(
                self.flow_network[lf][rf][he.id]['weight'] *
                var_dict[lf][rf][he.id]
            )

        # bend points' cost
        if weight_of_corner != 0:
            for v in self.planar.G:
                if self.planar.G.degree(v) == 2:
                    (f1, he1_id), (f2, he2_id) = [(f, key)
                                                  for f, keys in self.flow_network.adj[v].items()
                                                  for key in keys]
                    x = var_dict[v][f1][he1_id]
                    y = var_dict[v][f2][he2_id]
                    p = pulp.LpVariable(
                        x.name + "%temp", None, None, pulp.LpInteger)
                    prob.addConstraint(x - y <= p)
                    prob.addConstraint(y - x <= p)
                    objs.append(weight_of_corner * p)

        # non symmetrics cost
        if weight_of_sym != 0:
            if sym_pairs:
                for u, v in sym_pairs:
                    if u != v:
                        faces1 = {
                            face.id for face in self.planar.dcel.vertex_dict[u].surround_faces()}
                        faces2 = {
                            face.id for face in self.planar.dcel.vertex_dict[v].surround_faces()}
                        for f in faces1 & faces2:
                            nodes_id = self.planar.dcel.face_dict[f].nodes_id
                            n = len(nodes_id)
                            u_succ = nodes_id[(nodes_id.index(u) + 1) % n]
                            v_succ = nodes_id[(nodes_id.index(v) + 1) % n]
                            he_u = self.planar.dcel.half_edge_dict[u, u_succ]
                            he_v = self.planar.dcel.half_edge_dict[v, v_succ]

                            x, y = var_dict[u][f][he_u.id], var_dict[v][f][he_v.id]
                            p = pulp.LpVariable(
                                x.name + y.name + "%temp", None, None, pulp.LpInteger)
                            prob.addConstraint(x - y <= p)
                            prob.addConstraint(y - x <= p)
                            objs.append(weight_of_sym * p)

            for v in self.planar.G:
                if self.planar.G.degree(v) == 3:
                    for f, keys in self.flow_network.adj[v].items():
                        if len(keys) == 2:
                            he1_id, he2_id = list(keys)
                            x = var_dict[v][f][he1_id]
                            y = var_dict[v][f][he2_id]
                            p = pulp.LpVariable(
                                x.name + y.name + "%temp", None, None, pulp.LpInteger)
                            prob.addConstraint(x - y <= p)
                            prob.addConstraint(y - x <= p)
                            objs.append(weight_of_sym * p)
        prob += pulp.lpSum(objs), "number of bends in graph"

        for f in self.planar.dcel.face_dict:
            prob += self.flow_network.nodes[f]['demand'] == pulp.lpSum(
                [var_dict[v][f][he_id] for v, _, he_id in self.flow_network.in_edges(f, keys=True)])
        for v in self.planar.G:
            prob += -self.flow_network.nodes[v]['demand'] == pulp.lpSum(
                [var_dict[v][f][he_id] for _, f, he_id in
                 self.flow_network.out_edges(v, keys=True)]
            )

        state = prob.solve()
        if state == 1:  # update flow_dict
            # code here works only when nodes are represented by str, likes '(1, 2)'
            for var in prob.variables():
                if 'temp' not in var.name:
                    l = var.name.split('%')
                    if len(l) == 3:
                        # u, v, he_id = map(trans, l) # change str to tuple !!!!!!!!!
                        u, v, he_id = [item.replace('_', ' ') for item in l]
                        he_id = eval(he_id)
                        self.flow_dict[u][v][he_id] = int(var.varValue)
            return pulp.value(prob.objective)
        else:
            return 2**32

    def number_of_corners(self):
        count_right_angle = 0
        for node in self.planar.G:
            if self.planar.G.degree(node) == 2:
                for f, he_id in [(f, key) for f, keys in self.flow_network.adj[node].items()
                                 for key in keys]:
                    if self.flow_dict[node][f][he_id] == 1:
                        count_right_angle += 1
        return count_right_angle + self.flow_network.cost


class Compaction:
    '''
    Assign minimum lengths to the segments of the edges of the orthogonal representation.
    Never reverse ortho in this class.
    '''

    def __init__(self, ortho):
        self.ortho = ortho
        if ortho.flow_network.cost == 0:
            self.planar = ortho.planar
            self.flow_dict = ortho.flow_dict
        else:
            self.planar = ortho.planar.copy()
            self.flow_dict = copy.deepcopy(ortho.flow_dict)

        self.bend_point_processor()
        self.edge_side = self.face_side_processor()
        self.tidy_rectangle_compaction()
        self.pos = self.layout()

    def bend_point_processor(self):
            '''Create dummy nodes for bends.
            '''
            bends = {}  # left to right
            for he in self.planar.dcel.half_edge_dict.values():
                lf, rf = he.twin.inc, he.inc
                flow = self.flow_dict[lf.id][rf.id][he.id]
                if flow > 0:
                    bends[he.id] = flow

            idx = 0
            for he_id, n_bends in bends.items():
                # Q: what if there are bends on both (u, v) and (v, u)?
                # A: Impossible, not a min cost
                he = self.planar.dcel.half_edge_dict[he_id]
                u, v = he.get_points()
                lf_id, rf_id = he.twin.inc.id, he.inc.id

                self.planar.G.remove_edge(u, v)
                self.flow_dict[u][rf_id][u, f'b{idx}'] = self.flow_dict[u][rf_id].pop((u, v))



                for i in range(n_bends):
                    cur_node = f'b{idx}'
                    pre_node = f'b{idx-1}' if i > 0 else u
                    nxt_node = f'b{idx+1}' if i < n_bends - 1 else v
                    self.planar.G.add_edge(pre_node, cur_node)
                    self.planar.dcel.add_node_between(
                        pre_node, v, cur_node
                    )
                    self.flow_dict.setdefault(cur_node, {}).setdefault(lf_id, {})[cur_node, pre_node] = 1
                    self.flow_dict.setdefault(cur_node, {}).setdefault(rf_id, {})[cur_node, nxt_node] = 3
                    idx += 1

                self.flow_dict[v][lf_id][v, f'b{idx-1}'] = self.flow_dict[v][lf_id].pop((v, u))
                self.planar.G.add_edge(f'b{idx-1}', v)

    def face_side_processor(self):
        '''
        Associating edges with face sides.
        '''

        def update_face_edge(edge_side, face, base):
            for he in face.surround_half_edges():
                edge_side[he.id] = (edge_side[he.id] + base) % 4

        edge_side = {}
        for face in self.planar.dcel.face_dict.values():
            # set edges' side in internal faces independently at first
            side = 0
            for he in face.surround_half_edges():
                edge_side[he.id] = side
                end_angle = self.flow_dict[he.succ.ori.id][face.id][he.succ.id]
                if end_angle == 1:
                    # turn right in internal face or turn left in external face
                    side = (side + 1) % 4
                elif end_angle == 3:
                    side = (side + 3) % 4
                elif end_angle == 4:  # a single edge
                    side = (side + 2) % 4

        # update other face's edge side based on ext_face's edge side
        faces_dfs = list(self.planar.dfs_face_order())

        # all faces in dfs order
        has_updated = {faces_dfs[0].id}
        for face in faces_dfs[1:]:
            # at least one twin edge has been set
            for he in face.surround_half_edges():
                lf_id = he.twin.inc.id
                if lf_id in has_updated:  # neighbor face has been updated
                    # the edge that has been updated
                    l_side = edge_side[he.twin.id]
                    r_side = edge_side[he.id]  # side of u, v in face
                    update_face_edge(
                        edge_side, face, (l_side + 2) % 4 - r_side)
                    has_updated.add(face.id)
                    break
        return edge_side

    def tidy_rectangle_compaction(self):
        '''
        Doing the compaction of TSM algorithm.
        Compute every edge's length, and store them in self.planar.G.edges[u, v]['len']
        '''
        def build_flow(target_side):
            hv_flow = Flow_net()
            for he_id, side in self.edge_side.items():
                if side == target_side:
                    he = self.planar.dcel.half_edge_dict[he_id]
                    lf, rf = he.twin.inc, he.inc
                    lf_id = lf.id
                    rf_id = rf.id if rf.id != self.planar.ext_face.id else 'end'
                    hv_flow.add_edge(lf_id, rf_id, he_id)
            return hv_flow

        def solve(hv_flow, source, sink):
            if not hv_flow:
                return {}
            for node in hv_flow:
                hv_flow.nodes[node]['demand'] = 0
            hv_flow.nodes[source]['demand'] = -2**32
            hv_flow.nodes[sink]['demand'] = 2**32
            for lf_id, rf_id, he_id in hv_flow.edges:
                # what if selfloop?
                hv_flow.edges[lf_id, rf_id, he_id]['weight'] = 1
                hv_flow.edges[lf_id, rf_id, he_id]['lowerbound'] = 1
                hv_flow.edges[lf_id, rf_id, he_id]['capacity'] = 2**32
            hv_flow.add_edge(source, sink, 'extend_edge',
                             weight=0, lowerbound=0, capacity=2**32)

            # selfloop，avoid inner edge longer than border
            # for u, _ in hv_flow.selfloop_edges():
            #     in_nodes = [v for v, _ in hv_flow.in_edges(u)]
            #     assert in_nodes
            #     delta = sum(hv_flow[v][u]['lowerbound'] for v in in_nodes) - hv_flow[u][u]['count']
            #     if delta < 0:
            #         hv_flow.edges[in_nodes[0]][u]['lowerbound'] += -delta
            return hv_flow.min_cost_flow()

        hor_flow = build_flow(1)  # up -> bottom
        ver_flow = build_flow(0)  # left -> right

        hor_flow_dict = solve(hor_flow, self.planar.ext_face.id, 'end')
        ver_flow_dict = solve(ver_flow, self.planar.ext_face.id, 'end')

        for he in self.planar.dcel.half_edge_dict.values():
            if self.edge_side[he.id] in (0, 1):
                side = self.edge_side[he.id]

                rf = he.inc
                rf_id = 'end' if rf.id == self.planar.ext_face.id else rf.id
                lf_id = he.twin.inc.id

                if side == 0:
                    hv_flow_dict = ver_flow_dict
                elif side == 1:
                    hv_flow_dict = hor_flow_dict

                length = hv_flow_dict[lf_id][rf_id][he.id]
                self.planar.G.edges[he.id]['len'] = length

    def layout(self):
        pos = {}
        for face in self.planar.dfs_face_order():
            for i, u in enumerate(face.nodes_id):
                if not pos:
                    pos[u] = (0, 0) # initial point
                if u in pos:  # has found a start point
                    new_loop = face.nodes_id[i:] + face.nodes_id[:i]
                    for u, v in zip(new_loop, new_loop[1:]):
                        if v not in pos:
                            side = self.edge_side[u, v]
                            length = self.planar.G.edges[u, v]['len']
                            if side == 1:
                                pos[v] = (pos[u][0] + length, pos[u][1])
                            elif side == 3:
                                pos[v] = (pos[u][0] - length, pos[u][1])
                            elif side == 0:
                                pos[v] = (pos[u][0], pos[u][1] + length)
                            else:  # side == 2
                                pos[v] = (pos[u][0], pos[u][1] - length)
                    break
        return pos

    def check(self):
        for u, v in self.planar.G.edges:
            assert self.pos[u][0] == self.pos[v][0] or self.pos[u][1] == self.pos[v][1]

    def draw(self, **kwds):
        nx.draw(self.planar.G, self.pos, **kwds)
