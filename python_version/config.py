import os
import mylib
import config

config = config.Config()
result = config.Result()

def exists_test(name):
    if os.path.isfile(name):
        return True
    else:
        return False

def assert_file_exist(desc, name):
    if not exists_test(name):
        print(desc + " " + name + "not found")
        exit(1)


alpha_default = 0.2
alpha_denominator = 5
alpha_numerator = 1

num_of_query = 20
query = "query"
gen_ss_query = "generate-ss-query"
topk = "topk"
build = "build"
gen_exact_topk = "gen-exact-topk"
batch_topk = "batch-topk"

bippr = "bippr"
fora = 'fora'
fwdpush = "fwdpush"
mc = "montecarlo"
hubppr = "hubppr"

mc_query = 1
bippr_query = 2
fora_query = 3
hubppr_query = 4
fwd_lu = 5
random_walk = 6
source_dist = 7
sort_map = 8
bwd_lu = 9
pi_query = 10
stop_check = 11

deg_norm = 7
rg_cost = 1.0

sg_rw_cost = 8.0

class Config:
    def __init__(self, graph_alias, graph_location, action, prefix,version,exe_result_dir,
    multithread,with_rw_idx,opt,remap,force_rebuild,balance):
        self.graph_alias = ""
        self.graph_location = ""
        self.action = ""
        self.prefix = "/Users/haolan/Desktop/capstone/data/"
        self.version = "vector"
        self.exe_result_dir = "" or self.parent_folder()
        self.multithread = False
        self.with_rw_idx = False
        self.opt = False
        self.remap = False
        self.force_rebuild = False
        self.balance = False
    
    def get_graph_folder(self):
        return os.path.join(self.prefix, self.graph_alias)

    def parent_folder(self):
        pass