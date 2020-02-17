#!/usr/bin/env python3

import sys
import yaml
import pathlib
import subprocess

def read_yaml(file_path):
    f = open(file_path, "r+")
    dic = yaml.safe_load(f)
    f.close()
    return dic


def drop_false(dic):
    return {k: v for k, v in dic.items() if v != False}

def replace_source_path(dic, curr_dir):
    ret = dic
    if "source" in ret:
        ret["source"] = str(pathlib.PurePath(
                curr_dir,
                ret["source"]))
    
    return ret

def conv_dict_values(dic):
    return {k: ",".join([str(i) for i in v]) if type(v) == list
            else (
                ",".join(["{}={}".format(v_k, v_v) for v_k, v_v in v.items()]) if type(v) == dict
                else (
                    v
                )
            ) for k, v in dic.items()
        }

def create_cmd_array(name, dic, other_args):
    ret_origin = [["gcloud", "functions", "deploy", name]]
    ret_origin.extend([ ["--{}".format(k)] if v == True else ["--{}".format(k), v] for k, v in dic.items()])
    return sum(ret_origin, other_args, [])

args = sys.argv
args.pop(0)
conf_filepath = args.pop(-1)
conf_filedir = pathlib.Path(conf_filepath).resolve().parent
name = conf_filedir.name

cmd_array = create_cmd_array(name, conv_dict_values(replace_source_path(drop_false(read_yaml(conf_filepath)), conf_filepath)), other_args)

print("exec:", " ".join(cmd_array))
subprocess.call(cmd_array)

