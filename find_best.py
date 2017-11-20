import statistics

def get_stdev(lines):
    stddevs = []
    i = 1
    for line in lines:
        if "," in line:
            times = [int(x) for x in line.split(", ") if x.isdigit()]
            times = [x for x in times if x > 0]
            stddevs.append((i, statistics.stdev(times[:250])))

            i += 1

    print("Standard deviation: " + str(stddevs))


def get_mean(lines):
    means = []
    i = 1
    for line in lines:
        if "," in line:
            times = [int(x) for x in line.split(", ") if x.isdigit()]
            times = [x for x in times if x > 0]
            means.append((i, statistics.mean(times[:250])))
            i += 1
    print("Mean: " + str(means))

def get_median(lines):
    medians = []
    i = 1
    for line in lines:
        if "," in line:
            times = [int(x) for x in line.split(", ") if x.isdigit()]
            times = [x for x in times if x > 0]
            medians.append((i, statistics.median(times[:250])))
            i += 1

    print("Median: " + str(medians))

def get_best(lines):
    best_times = []
    i = 1
    for line in lines:
        if "," in line:
            times = line.split(", ")
            best_time = 999999
            for t in times[:250]:
                try:
                    if int(t) < best_time and int(t) > 0:
                        best_time = int(t)
                except ValueError:
                    x = 0
            best_times.append((i, best_time))
            i += 1


    print("Best time")
    print(best_times)   


print("blackscholes 1")
f = open("blackscholes1.data", "r")
lines = f.read().splitlines()
get_best(lines)

   
print("blackscholes 2")
f = open("blackscholes2.data", "r")
lines = f.read().splitlines()
get_best(lines)



print("bodytrack 1")
f = open("bodytrack1.data", "r")
lines = f.read().splitlines()
get_best(lines)

   
print("bodytrack 2")
f = open("bodytrack2.data", "r")
lines = f.read().splitlines()
get_best(lines)
