import subprocess

def get_cpu_time():
    f = subprocess.check_output(["tail", "--lines=2", "/tmp/exps/result/sched_stats.txt"]).decode("utf-8")
    output = f.split("\t")

    return (output[output.index("Total_time=") + 1])


print(get_cpu_time())
