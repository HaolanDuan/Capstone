import mylib
import config

class Graph:
    def __init__(self, data_folder):
        self.g = []
        self.gr = []
        self.data_folder = data_folder
        if config.action != GEN_SS_QUERY:
            self.init_graph()
        else:
            self.init_nm()
        print("init graph n:", self.n, "m:", self.m)
    
    @staticmethod
    def cmp(t1, t2):
        return t1[1] > t2[1]
    
    def init_nm(self):
        attribute_file = self.data_folder + FILESEP + "attribute.txt"
        assert_file_exist("attribute file", attribute_file)
        attr = open(attribute_file, 'r')
        line1, line2 = '', ''
        c = ''
        while True:
            c = attr.read(1)
            if c == '=':
                break
        self.n = int(attr.readline())
        while True:
            c = attr.read(1)
            if c == '=':
                break
        self.m = int(attr.readline())
    
    def init_nm_convert(self):
        attribute_file = self.data_folder + FILESEP + "attribute.txt"
        assert_file_exist("attribute file", attribute_file)
        attr = open(attribute_file, 'r')
        line1, line2 = '', ''
        c = ''
        while True:
            c = attr.read(1)
            if c == '=':
                break
        self.n = int(attr.readline())
        while True:
            c = attr.read(1)
            if c == '=':
                break
        self.m = int(attr.readline())
        while True:
            c = attr.read(1)
            if c == '=':
                break
        self.maxid = int(attr.readline())
    
    def init_graph(self):
        if config.remap:
            self.init_nm_convert()
        else:
            self.init_nm()
        self.g = [[] for _ in range(self.n)]
        self.gr = [[] for _ in range(self.n)]
        graph_file = self.data_folder + FILESEP + "graph.txt"
        assert_file_exist("graph file", graph_file)
        if config.remap:
            idmap = [-1] * self.maxid
            degree = [0] * self.n
            startid = 0
            with open(graph_file, 'r') as fin:
                for line in fin:
                    t1, t2 = map(int, line.split())
                    if idmap[t1] < 0:
                        idmap[t1] = startid
                        degree[startid] += 1
                        startid += 1
                    else:
                        degree[idmap[t1]] += 1
                    if idmap[t2] < 0:
                        idmap[t2] = startid
                        startid += 1
                    if t1 == t2:
                        continue
            for i in range(self.n):
                self.g[i] = [0] * degree[i]
            with open(graph_file, 'r') as fin2:
                for line in fin2:
                    t1, t2 = map(int, line.split())
                    assert idmap[t1] < self.n and idmap[t1] >= 0
                    assert idmap[t2] < self.n and idmap[t2] >= 0
                    if t1 == t2:
                        continue
                    self.g[idmap[t1]].append(idmap[t2])
        else:
            with open(graph_file, 'r') as fin:
                for line in fin:
                    t1, t2 = map(int, line.split())
                    assert t1 < self.n
                    assert t2 < self.n
                    if t1 == t2:
                        continue
                    self.g[t1].append(t2)
                    self.gr[t2].append(t1)
    
    def get_avg_degree(self):
        return float(self.m) / float(self.n)

def init_parameter(config, graph):
    print("init parameters", graph.n)
    config.delta = 1.0 / graph.n
    config.pfail = 1.0 / graph.n
    config.dbar = float(graph.m) / float(graph.n)

