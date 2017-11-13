import random
import subprocess
import os
import time
import datetime

from ga import *

FNULL = open(os.devnull, 'w')


def ssh_process(hostname, script):
    gem5_path = "~/Documents/cs4202/p2/CS4202_gensched/gem5/"

    return ["ssh", hostname, "cd " + gem5_path + " && python3 " + script]

def get_cpu_time(file):
    f = subprocess.check_output(["tail", "--lines=2", file]).decode("utf-8")
    output = f.split("\t")

    return (output[output.index("Total_time=") + 1])


#hosts = ["pc3-0"+str(host_id)+"-l.cs.st-andrews.ac.uk" for host_id in range(10,70)]
hosts = ["pc2-0"+str(host_id)+"-l.cs.st-andrews.ac.uk" for host_id in range(10,99)]


# population 25:
# mutation per genes: random 0 - length/10
# crossover: random
# selection: tournament 5
# experiment_data = open("blackscholes1.data", "w")


# population 25:
# mutation per genes: random 0 - length/10
# crossover: random
# selection: tournament 5
experiment_data = open("bodytrack1.data", "w")

population = Population(25, 1000000)
for generation in range(30):
    experiment_data.write("Generation " + str(generation) + ": \n")
    print("Start generation " + str(generation) + " at " + str(datetime.datetime.now()))

    print("Pinging hosts...")
    activehosts = []
    for hostname in hosts:
        process = subprocess.run(["ping", "-c", "1", "-w", "1", hostname], stdout=FNULL)
        if process.returncode == 0:
            activehosts.append(hostname)
            
    print("Active hosts: " + str(len(activehosts)))

    random.shuffle(activehosts)

    
    processes = {}
    i = 0
    for chromosome in population.chromosomes:
        binRepf = open("binRep1.txt", "w")
        binRepf.write("".join(map(str, chromosome.genes)))

        # Write schedule to local storage
        subprocess.run(ssh_process(activehosts[i], "write.py"), stdout=FNULL)

        # Spawn simulator processes
        print("Spawn simulator for chromosome " + str(i) + " on " + activehosts[i])
        p = subprocess.Popen(ssh_process(activehosts[i], "script.py"), stdout=FNULL, stderr=FNULL)
        processes[(activehosts[i], chromosome)] = p

        i += 1

    # Wait for simulator processes to terminate
    for (k,v) in processes.items():
        processes[k] = v.wait()

    print("Simulations finished...")
    print("Time: " + str(datetime.datetime.now()))
    finished_hosts = 0
    for ((host, chromosome), v) in processes.items():

        # Simulation terminated without errors
        if v == 0:
            finished_hosts += 1

            # Copy sched_stats.txt output to networked storage
            subprocess.run(ssh_process(host, "copy.py"))

            time.sleep(1)

            # Update chromosome fitness
            experiment_data.write(get_cpu_time("sched_stats.txt") + ", ")
            print("Host: " + host + " time taken: " + get_cpu_time("sched_stats.txt"))
            experiment_data.write()
            chromosome.fitness = 1 / int(get_cpu_time("sched_stats.txt"))


    # Save best schedule 
    best_child = population.elites(1)[0]
    best_file = open("best-bodytrack.txt", "w")
    best_file.write("".join(map(str, best_child.genes)))

    
    print("generation " + str(generation) + " finished hosts: " + str(finished_hosts) + "/" + str(len(processes)) + " best time: " + str(population.elites(1)[0].fitness))
    print("---------------------------------------")

    num_elites = random.randint(1, int(population.size/2))
    print("Evolving with " + str(num_elites) + " elites.")
    population.evolve(num_elites)

    experiment_data.write("\n--------------------------\n")
