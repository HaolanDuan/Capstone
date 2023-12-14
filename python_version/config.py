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




import boost.progress
import boost.property_tree.ptree
import boost.property_tree.json_parser
import boost.property_tree.ptree
import boost.property_tree.json_parser
import boost.date_time.posix_time.posix_time
import boost.algorithm.string.predicate
import boost.filesystem.operations
import boost.filesystem.path
import boost.filesystem
import unordered_map
import list

ALPHA_DEFAULT = 0.2
ALPHA_DENOMINATOR = 5
ALPHA_NUMERATOR = 1
NUM_OF_QUERY = 20
QUERY = "query"
GEN_SS_QUERY = "generate-ss-query"
TOPK = "topk"
BUILD = "build"
GEN_EXACT_TOPK = "gen-exact-topk"

BATCH_TOPK = "batch-topk"
BIPPR = "bippr"
FORA = "fora"
FWDPUSH = "fwdpush"
MC = "montecarlo"
HUBPPR = "hubppr"
MC_QUERY = 1
BIPPR_QUERY = 2
FORA_QUERY = 3
HUBPPR_QUERY = 4
FWD_LU = 5
RONDOM_WALK = 6
SOURCE_DIST = 7
SORT_MAP = 8
BWD_LU = 9
PI_QUERY = 10
STOP_CHECK=11
DEG_NORM = 7
RG_COST = 1

SG_RW_COST = 8.0

parent_folder = "../../" if WIN32 else "./"

class Config:
    def __init__(self):
        self.graph_alias = ""
        self.graph_location = ""
        self.action = ""
        self.prefix = "/Users/haolan/Desktop/capstone/data"
        self.version = "vector"
        self.exe_result_dir = parent_folder
        self.multithread = False
        self.with_rw_idx = False
        self.opt = False
        self.remap = False
        self.force_rebuild = False
        self.balanced = False
        self.omega = 0
        self.rmax = 0
        self.query_size = 1000
        self.max_iter_num = 100
        self.pfail = 0
        self.dbar = 0
        self.epsilon = 0
        self.delta = 0
        self.k = 500
        self.ppr_decay_alpha = 0.77
        self.rw_cost_ratio = 8.0
        self.rmax_scale = 1
        self.multithread_param = 1.0
        self.algo = ""
        self.alpha = ALPHA_DEFAULT
        self.alpha_numerator = 1
        self.alpha_denominator = 5
        self.exact_pprs_folder = ""
        self.hub_space_consum = 1
    
    def get_graph_folder(self):
        return self.prefix + self.graph_alias + FILESEP
    
    def get_data(self):
        data = boost.property_tree.ptree()
        data.put("graph_alias", self.graph_alias)
        data.put("action", self.action)
        data.put("alpha", self.alpha)
        data.put("pfail", self.pfail)
        data.put("epsilon", self.epsilon)
        data.put("delta", self.delta)
        data.put("idx", self.with_rw_idx)
        data.put("k", self.k)
        data.put("rand-walk & push cost ratio", self.rw_cost_ratio)
        data.put("query-size", self.query_size)
        data.put("algo", self.algo)
        data.put("rmax", self.rmax)
        data.put("rmax-scale", self.rmax_scale)
        data.put("omega", self.omega)
        data.put("result-dir", self.exe_result_dir)
        return data

class Result:
    def __init__(self):
        self.n = 0
        self.m = 0
        self.avg_query_time = 0
        self.total_mem_usage = 0
        self.total_time_usage = 0
        self.num_randwalk = 0
        self.num_rw_idx_use = 0
        self.hit_idx_ratio = 0
        self.randwalk_time = 0
        self.randwalk_time_ratio = 0
        self.propagation_time = 0
        self.propagation_time_ratio = 0
        self.source_dist_time = 0
        self.source_dist_time_ratio = 0
        self.topk_sort_time = 0
        self.topk_sort_time_ratio = 0
        self.topk_max_abs_err = 0
        self.topk_avg_abs_err = 0
        self.topk_max_relative_err = 0
        self.topk_avg_relative_err = 0
        self.topk_precision = 0
        self.topk_recall = 0
        self.real_topk_source_count = 0
    
    def get_data(self):
        data = boost.property_tree.ptree()
        data.put("n", self.n)
        data.put("m", self.m)
        data.put("avg query time(s/q)", self.avg_query_time)
        data.put("total memory usage(MB)", self.total_mem_usage)
        data.put("total time usage(s)", self.total_time_usage)
        data.put("total time on rand-walks(s)", self.randwalk_time)
        data.put("total time on propagation(s)", self.propagation_time)
        data.put("total time on sorting top-k ppr(s)", self.topk_sort_time)
        data.put("total time ratio on rand-walks(%)", self.randwalk_time_ratio)
        data.put("total time ratio on propagation(%)", self.propagation_time_ratio)
        data.put("total number of rand-walks", self.num_randwalk)
        data.put("total number of rand-walk idx used", self.num_rw_idx_use)
        data.put("total usage ratio of rand-walk idx", self.hit_idx_ratio)
        data.put("topk max absolute error", self.topk_max_abs_err/self.real_topk_source_count)
        data.put("topk avg absolute error", self.topk_avg_abs_err/self.real_topk_source_count)
        data.put("topk max relative error", self.topk_max_relative_err/self.real_topk_source_count)
        data.put("topk avg relative error", self.topk_avg_relative_err/self.real_topk_source_count)
        data.put("topk precision", self.topk_precision/self.real_topk_source_count)
        data.put("topk recall", self.topk_recall/self.real_topk_source_count)
        return data

config = Config()
result = Result()

def exists_test(name):
    return boost.filesystem.exists(name)

def assert_file_exist(desc, name):
    assert exists_test(name)

class Saver:
    @staticmethod
    def get_current_time_str():
        rawtime = boost.date_time.posix_time.posix_time()
        timeinfo = boost.date_time.localtime(rawtime)
        buffer = boost.date_time.strftime(timeinfo, "%Y-%m-%d %H:%M:%S")
        return buffer
    
    @staticmethod
    def get_time_path():
        if not boost.algorithm.ends_with(config.exe_result_dir, FILESEP):
            config.exe_result_dir += FILESEP
        config.exe_result_dir += "execution/"
        if not boost.filesystem.exists(config.exe_result_dir):
            dir = boost.filesystem.path(config.exe_result_dir)
            boost.filesystem.create_directories(dir)
        filename = config.graph_alias+"."+config.action+"."+config.algo
        if config.algo == "assppr":
            filename = filename + "." + str(int(config.rw_cost_ratio))
        idx_flag = "with_idx" if config.with_rw_idx else "without_idx"
        filename = filename+"."+idx_flag+"."
        filename += "k-"+str(config.k)+"."
        filename += "rmax-"+str(config.rmax_scale)
        return config.exe_result_dir + filename
    
    @staticmethod
    def init():
        Saver.combine = boost.property_tree.ptree()
        Saver.combine.put("start_time", Saver.get_current_time_str())
    
    @staticmethod
    def save_json(config, result, args):
        fout = open(Saver.get_time_path() + ".json", "w")
        command_line = ""
        for i in range(1, len(args)):
            command_line += " " + args[i]
        Saver.combine.put("end_time", Saver.get_current_time_str())
        Saver.combine.put("command_line", command_line)
        Saver.combine.put_child("config", config.get_data())
        Saver.combine.put_child("result", result.get_data())
        timer = boost.property_tree.ptree()
        for i in range(len(Timer.timeUsed)):
            if Timer.timeUsed[i] > 0:
                timer.put(str(i), Timer.timeUsed[i] / TIMES_PER_SEC)
        Saver.combine.put_child("timer", timer)
        boost.property_tree.json_parser.write_json(fout, Saver.combine, True)


