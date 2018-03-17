
import heapq

class _Subset:
    def __init__(self, parent, identifier, rank):
        self.parent = parent
        self.identifier = identifier
        self.rank = rank

class _Edge:
    def __init__(self, edge):
        self.origin = edge['origin']
        self.destiny = edge['destiny']
        self.weight = edge['weight']

    def __lt__(self, other):
        return self.weight < other.weight

class MST:
    'This class returns the mst of any graph jn json format'
    def __init__(self, json_graph):
        self.graph = json_graph
        self.num_vertex = len(self.graph['vertex'])
        self.index_result = 0
        self.result = []
        self.subsets = []
        self.heap = []

    def get_mst(self):
        'Returns the mst of the graph'
        self.__build_heap()
        self.__build_subsets()

        while self.index_result < self.num_vertex - 1:
            edge = heapq.heappop(self.heap)
            origin = self.__find(edge.origin)['parent']
            destiny = self.__find(edge.destiny)['parent']

            if origin != destiny:
                self.result.append(edge)
                self.__union(origin, destiny)
                self.index_result += 1

        return self.__to_json_graph()

    def __build_heap(self):
        for edge in self.graph['edges']:
            heapq.heappush(self.heap, _Edge(edge))

    def __build_subsets(self):
        for i in range(self.num_vertex):
            parent = identifier = self.graph['vertex'][i]
            rank = 0
            self.subsets.append(_Subset(parent, identifier, rank))

    def __find(self, vertex_name):
        subset = 0

        while subset < len(self.subsets):
            if self.subsets[subset].identifier == vertex_name:
                break
            subset += 1

        if self.subsets[subset].parent != vertex_name:
            bundle = self.__find(self.subsets[subset].parent)
            self.subsets[subset].parent = bundle['parent']
            subset = bundle['set']

        return {'parent': self.subsets[subset].parent, 'set': subset}

    def __union(self, origin, destiny):
        bundle_origin = self.__find(origin)
        bundle_destiny = self.__find(destiny)
        set_origin = bundle_origin['set']
        set_destiny = bundle_destiny['set']

        if self.subsets[set_origin].rank < self.subsets[set_destiny].rank:
            self.subsets[set_origin].parent = bundle_destiny['parent']

        elif self.subsets[set_origin].rank > self.subsets[set_destiny].rank:
            self.subsets[set_destiny].parent = bundle_origin['parent']

        else:
            self.subsets[set_destiny].parent = bundle_origin['parent']
            self.subsets[set_origin].rank += 1

    def __to_json_graph(self):
        graph = []

        for edge in self.result:
            json = {}
            json['origin'] = edge.origin
            json['destiny'] = edge.destiny
            json['weight'] = edge.weight
            graph.append(json)

        return graph
