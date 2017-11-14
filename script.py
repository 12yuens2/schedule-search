import subprocess

subprocess.run(["build/ARM/gem5.opt", "-d", "/tmp/sy35/exps/result", "configs/sched-blackscholes_gen.py", "--machine-type=VExpress_EMM64"])
