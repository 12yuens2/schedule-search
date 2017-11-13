import subprocess
import os
#import ga

FNULL = open(os.devnull, 'w')

hostname = "pc3-012-l.cs.st-andrews.ac.uk"

hosts = ["pc3-0"+str(host_id)+"-l.cs.st-andrews.ac.uk" for host_id in range(10,70)]
#hosts += ["pc2-0"+str(host_id)+"-l.cs.st-andrews.ac.uk" for host_id in range(10,99)]

activehosts = []

for hostname in hosts:
    process = subprocess.run(["ping", "-c", "1", "-w", "1", hostname], stdout=FNULL)
    if process.returncode == 0:
        activehosts.append(hostname)

gem5_path = "~/Documents/cs4202/p2/CS4202_gensched/gem5/"

simulation_process = ["build/ARM/gem5.opt", "-d", "./exps/rng/", "configs/sched-ferret_In.py", "--machine-type=VExpress_EMM64"]

def ssh_process(hostname):
    return ["ssh", hostname, "cd " + gem5_path + " && python3 script.py"]

processes = {}
for i in range(10):
    p = subprocess.Popen(ssh_process(activehosts[i]), stdout=FNULL)
    processes[activehosts[i]] = p

for (k,v) in processes.items():
   processes[k] = v.wait() 

finished_hosts = 0
for (k,v) in processes.items():
    if v == 0:
        finished_hosts += 1
        print(k)
        subprocess.run(["ssh", k, "cd /tmp/exps/result/ && wc -m binRep2.txt"])
        print("----------------")

print("end start processes " + str(finished_hosts) + "/" + str(len(processes)))
