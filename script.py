import subprocess
import time
import sys

def get_cpu_time():
    f = subprocess.check_output(["tail", "--lines=2", "/tmp/exps/result/sched_stats.txt"]).decode("utf-8")
    output = f.split("\t")

    return (output[output.index("Total_time=") + 1])

subprocess.run(["build/ARM/gem5.opt", "-d", "/tmp/exps/result", "configs/sched-blackscholes_gen.py", "--machine-type=VExpress_EMM64"])


