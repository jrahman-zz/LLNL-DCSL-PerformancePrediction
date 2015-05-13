

import re

def parse(inp):

    regex = r"\[OVERALL\], RunTime\(ms\), (\d*\.\d*)\n\[OVERALL\], Throughput\(ops/sec\), (\d*\.\d*)\n.*\n\[OVERALL\], RunTime\(ms\), (\d*\.\d*)\n\[OVERALL\], Throughput\(ops/sec\), (\d*\.\d*)\n.*\n\[OVERALL\], RunTime\(ms\), (\d*\.\d*)\n\[OVERALL\], Throughput\(ops/sec\), (\d*\.\d*)"

    match = re.search(regex, inp, flags=re.DOTALL)
    if match is None:
        raise Exception('No match') 
    t1 = float(match.group(1))
    t2 = float(match.group(3))
    t3 = float(match.group(5))
    r1 = float(match.group(2))
    r2 = float(match.group(4))
    r3 = float(match.group(6))

    time = t1 + t2 + t3
    # Use the harmonic mean because we are dealing with rates
    mean_rate = 3 / (1/r1 + 1/r2 + 1/r3)
    features = {'time': time, 'throughput': mean_rate}
    return features

def main():
    data = """YCSB Client 0.1
Command line: -db com.yahoo.ycsb.db.MongoDbClient -P /home/jprahman/llnl/YCSB//workloads/workloadc -p "operationcount=10000" -t
Loading workload...
Starting test.
new database url = localhost:27017/ycsb
mongo connection created with localhost:27017/ycsb
[OVERALL], RunTime(ms), 1350.0
[OVERALL], Throughput(ops/sec), 740.7407407407408
[READ], Operations, 1000
[READ], AverageLatency(us), 922.095
[READ], MinLatency(us), 540
[READ], MaxLatency(us), 92604
[READ], 95thPercentileLatency(ms), 1
[READ], 99thPercentileLatency(ms), 1
YCSB Client 0.1
Command line: -db com.yahoo.ycsb.db.MongoDbClient -P /home/jprahman/llnl/YCSB//workloads/workloadc -p "operationcount=10000" -t
Loading workload...
Starting test.
new database url = localhost:27017/ycsb
mongo connection created with localhost:27017/ycsb
[OVERALL], RunTime(ms), 1350.0
[OVERALL], Throughput(ops/sec), 740.7407407407408
[READ], Operations, 1000
[READ], AverageLatency(us), 922.095
[READ], MinLatency(us), 540
[READ], MaxLatency(us), 92604
[READ], 95thPercentileLatency(ms), 1
[READ], 99thPercentileLatency(ms), 1
YCSB Client 0.1
Command line: -db com.yahoo.ycsb.db.MongoDbClient -P /home/jprahman/llnl/YCSB//workloads/workloadc -p "operationcount=10000" -t
Loading workload...
Starting test.
new database url = localhost:27017/ycsb
mongo connection created with localhost:27017/ycsb
[OVERALL], RunTime(ms), 1350.0
[OVERALL], Throughput(ops/sec), 740.7407407407408
[READ], Operations, 1000
[READ], AverageLatency(us), 922.095
[READ], MinLatency(us), 540
[READ], MaxLatency(us), 92604
[READ], 95thPercentileLatency(ms), 1
[READ], 99thPercentileLatency(ms), 1
    """

    try:
        features = parse(data)
        print features
        exit(0)
    except Exception as e:
        print e
        exit(1)
    exit(0)

if __name__ == "__main__":
    main()
