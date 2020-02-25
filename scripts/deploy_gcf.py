#!/usr/bin/env python3
"""
Usage:
    deploy_gcf.py -c <config_file> -p <policy_file> [<args>...]

Options:
    -c <config_file>, --config-file <config_file>   configファイルを設定します。
    -p <policy_file>, --policy-file <policy_file>   iam-policyファイルを設定します。
"""

import os
import pathlib
import subprocess
import sys
import tempfile
import yaml
from docopt import docopt
import google.auth

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

def create_deploy_cmd_array(name, dic, other_args):
    ret_origin = [["gcloud", "functions", "deploy", name]]
    ret_origin.extend([ ["--{}".format(k)] if v == True else ["--{}".format(k), v] for k, v in dic.items()])
    ret_origin.extend(other_args)
    return sum(ret_origin, [])

args = docopt(__doc__)

conf_filepath = args["--config-file"]
conf_filedir = pathlib.Path(conf_filepath).resolve().parent
name = conf_filedir.name
other_args = args["<args>"]

config_params = read_yaml(conf_filepath)
deploy_cmd_array = create_deploy_cmd_array(name, conv_dict_values(replace_source_path(drop_false(config_params), conf_filedir)), other_args)

print("exec:", " ".join(deploy_cmd_array))
ret = subprocess.call(deploy_cmd_array)

if ret != 0:
    exit(ret)

def format_file(src, formatter, dst=None):
    wf = open(dst, mode="w+") if dst else tempfile.NamedTemporaryFile(mode='w+', delete=False)
    with open(policy_filepath) as rf:
        wf.write(rf.read().format(**formatter))
    filename = dst if dst else wf.name
    wf.close()
    return filename

policy_filepath = args["--policy-file"]
_, project_id = google.auth.default()

temp_policy_filename = format_file(policy_filepath, {"PROJECT_ID": project_id})

set_iam_policy_cmd_array = ["gcloud", "functions", "set-iam-policy", name, "--region", config_params["region"], temp_policy_filename]

print("exec:", " ".join(set_iam_policy_cmd_array))
ret = subprocess.call(set_iam_policy_cmd_array)
os.remove(temp_policy_filename)

exit(ret)
