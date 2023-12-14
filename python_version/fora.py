import mylib
import graph
import config
import algo 
import query
import build

import datetime
import sys
import random
import os
import json

def get_time_path():
    tm = datetime.datetime.now()
    if sys.platform == "win32":
        return "../../execution/" + tm.isoformat()
    else:
        return parent_folder + os.sep + "execution/" + tm.isoformat()

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", help="prefix")
    parser.add_argument("--epsilon", type=float, help="epsilon")
    parser.add_argument("--dataset", help="dataset")
    parser.add_argument("--query_size", type=int, help="queries count")
    parser.add_argument("--k", type=int, help="top k")
    parser.add_argument("--with_idx", action="store_true", help="with idx")
    parser.add_argument("--hub_space", type=int, help="hubppr oracle space-consumption")
    parser.add_argument("--exact_ppr_path", help="eaact-topk-pprs-path")
    parser.add_argument("--rw_ratio", type=float, help="rand-walk cost ratio")
    parser.add_argument("--result_dir", help="directory to place results")
    parser.add_argument("--rmax_scale", type=float, help="scale of rmax")
    parser.add_argument("--opt", action="store_true", help="opt")
    parser.add_argument("--balanced", action="store_true", help="balanced")
    parser.add_argument("--force-rebuild", action="store_true", help="force-rebuild")
    parser.add_argument("--version", help="version")
    parser.add_argument("--algo", help="algo")
    parser.add_argument("--multithread", action="store_true", help="multithread")
    parser.add_argument("--help", action="store_true", help="help")
    args = parser.parse_args()

    if args.help:
        help_str = """
        fora query --algo <algo> [options]
        fora topk  --algo <algo> [options]
        fora batch-topk --algo <algo> [options]
        fora build [options]
        fora generate-ss-query [options]
        fora gen-exact-topk [options]
        fora

        algo:
          bippr
          montecarlo
          fora
          hubppr
        options:
          --prefix <prefix>
          --epsilon <epsilon>
          --dataset <dataset>
          --query_size <queries count>
          --k <top k>
          --with_idx
          --hub_space <hubppr oracle space-consumption>
          --exact_ppr_path <eaact-topk-pprs-path>
          --rw_ratio <rand-walk cost ratio>
          --result_dir <directory to place results>
          --rmax_scale <scale of rmax>
        """
        print(help_str)
        sys.exit(0)

    config = {
        "prefix": args.prefix,
        "epsilon": args.epsilon,
        "dataset": args.dataset,
        "query_size": args.query_size,
        "k": args.k,
        "with_idx": args.with_idx,
        "hub_space": args.hub_space,
        "exact_ppr_path": args.exact_ppr_path,
        "rw_ratio": args.rw_ratio,
        "result_dir": args.result_dir,
        "rmax_scale": args.rmax_scale,
        "opt": args.opt,
        "balanced": args.balanced,
        "force_rebuild": args.force_rebuild,
        "version": args.version,
        "algo": args.algo,
        "multithread": args.multithread
    }

    print("action:", config["action"])

    if args.prefix:
        config["prefix"] = args.prefix
    if args.dataset:
        config["graph_alias"] = args.dataset

    possibleAlgo = ["bippr", "fora", "fwdpush", "montecarlo", "hubppr"]

    if args.algo not in possibleAlgo:
        print("Wrong algo param:", args.algo)
        sys.exit(1)

    print("action:", config["action"])

    if args.algo:
        config["algo"] = args.algo
    if args.epsilon:
        config["epsilon"] = args.epsilon
        print(config["epsilon"])
    if args.multithread:
        config["multithread"] = True
    if args.result_dir:
        config["exe_result_dir"] = args.result_dir
    if args.exact_ppr_path:
        config["exact_pprs_folder"] = args.exact_ppr_path
    if args.with_idx:
        config["with_rw_idx"] = True
    if args.rmax_scale:
        config["rmax_scale"] = args.rmax_scale
    if args.force_rebuild:
        config["force_rebuild"] = True
    if args.query_size:
        config["query_size"] = args.query_size
    if args.hub_space:
        config["hub_space_consum"] = args.hub_space
    if args.version:
        config["version"] = args.version
    if args.k:
        config["k"] = args.k
    if args.rw_ratio:
        config["rw_cost_ratio"] = args.rw_ratio

    print(config["version"])

    possibleAlgo = ["bippr", "fora", "fwdpush", "montecarlo", "hubppr"]

    if config["action"] == "query":
        if config["algo"] not in possibleAlgo:
            print("Wrong algo param:", config["algo"])
            sys.exit(1)

        config["graph_location"] = config.get_graph_folder()
        graph = Graph(config["graph_location"])
        print("load graph finish")
        init_parameter(config, graph)
        print("finished initing parameters")
        print(graph.n, graph.m)

        if config["with_rw_idx"]:
            deserialize_idx()

        query(graph)
        print("finished query")
    elif config["action"] == "gen_ss_query":
        config["graph_location"] = config.get_graph_folder()
        graph = Graph(config["graph_location"])
        print(graph.n, graph.m)
        generate_ss_query(graph.n)
    elif config["action"] == "topk":
        if config["algo"] not in possibleAlgo:
            print("Wrong algo param:", config["algo"])
            sys.exit(1)

        config["graph_location"] = config.get_graph_folder()
        graph = Graph(config["graph_location"])
        print("load graph finish")
        init_parameter(config, graph)
        if config["exact_pprs_folder"] == "" or not exists_test(config["exact_pprs_folder"]):
            config["exact_pprs_folder"] = config["graph_location"]
        print("finihsed initing parameters")
        print(graph.n, graph.m)

        if config["with_rw_idx"]:
            deserialize_idx()

        topk(graph)
    elif config["action"] == "batch_topk":
        if config["algo"] not in possibleAlgo:
            print("Wrong algo param:", config["algo"])
            sys.exit(1)

        config["graph_location"] = config.get_graph_folder()
        graph = Graph(config["graph_location"])
        print("load graph finish")
        init_parameter(config, graph)
        if config["exact_pprs_folder"] == "" or not exists_test(config["exact_pprs_folder"]):
            config["exact_pprs_folder"] = config["graph_location"]
        print("finihsed initing parameters")
        print(graph.n, graph.m)

        if config["with_rw_idx"]:
            deserialize_idx()

        batch_topk(graph)
    elif config["action"] == "gen_exact_topk":
        config["graph_location"] = config.get_graph_folder()
        graph = Graph(config["graph_location"])
        print("load graph finish")
        init_parameter(config, graph)
        if config["exact_pprs_folder"] == "" or not exists_test(config["exact_pprs_folder"]):
            config["exact_pprs_folder"] = config["graph_location"]
        print("finihsed initing parameters")
        print(graph.n, graph.m)
        gen_exact_topk(graph)
    elif config["action"] == "build":
        config["graph_location"] = config.get_graph_folder()
        graph = Graph(config["graph_location"])
        print("load graph finish")
        init_parameter(config, graph)
        print("finihsed initing parameters")
        print(graph.n, graph.m)
        with Timer(0):
            if config["multithread"]:
                multi_build(graph)
            else:
                build(graph)
    else:
        print("sub command not regoznized")
        sys.exit(1)

    Timer.show()
    if config["action"] == "query" or config["action"] == "topk":
        Counter.show()
        args = combine_args(sys.argv)
        Saver.save_json(config, result, args)
    else:
        program_stop()

if __name__ == "__main__":
    main()


