import subprocess
import time

def get_cpu_time(file):
    f = subprocess.check_output(["tail", "--lines=2", file]).decode("utf-8")
    output = f.split("\t")

    return (output[output.index("Total_time=") + 1])


subprocess.run(["build/ARM/gem5.opt", "-d", "/tmp/exps/result", "configs/sched-blackscholes_gen.py", "--machine-type=VExpress_EMM64"])


#time.sleep(2)
