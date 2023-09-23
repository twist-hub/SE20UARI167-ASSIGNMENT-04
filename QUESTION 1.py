from collections import deque
import time
import datetime

class Process:
    def __init__(self, process_id, arrival_time, burst_time, priority):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.waiting_time = 0
        self.turnaround_time = 0

def FCFS(processes):
    total_waiting_time_FCFS = 0
    total_turnaround_time_FCFS = 0
    current_time = 0
    for process in processes:
        process.waiting_time = current_time - process.arrival_time
        process.turnaround_time = process.waiting_time + process.burst_time
        current_time += process.burst_time
        total_waiting_time_FCFS += process.waiting_time
        total_turnaround_time_FCFS += process.turnaround_time

    print("total waiting time for FCFS:",total_waiting_time_FCFS)
    print("total turnaround time time for FCFS:",total_turnaround_time_FCFS)
    average_waiting_time = total_waiting_time_FCFS / len(processes)
    average_turnaround_time = total_turnaround_time_FCFS / len(processes)

    print("Average waiting time for FCFS:", average_waiting_time)
    print("Average turnaround time for FCFS:", average_turnaround_time)

    return total_waiting_time_FCFS, total_turnaround_time_FCFS 

def SJF(processes):
    total_waiting_time_SJF = 0
    total_turnaround_time_SJF = 0
    current_time = 0
    
    sorted_processes = processes.copy()

    while sorted_processes:
        arrived_processes = [process for process in sorted_processes if process.arrival_time <= current_time]
        if not arrived_processes:
            current_time += 1
        else:
            arrived_processes.sort(key=lambda process: process.burst_time)
            shortest_job = arrived_processes[0]
            shortest_job.waiting_time = current_time - shortest_job.arrival_time
            shortest_job.turnaround_time = shortest_job.waiting_time + shortest_job.burst_time
            current_time += shortest_job.burst_time
            total_waiting_time_SJF += shortest_job.waiting_time
            total_turnaround_time_SJF += shortest_job.turnaround_time
            sorted_processes.remove(shortest_job)

    print("\ntotal waiting time for SJF:",total_waiting_time_SJF)
    print("total turnaround time time for SJF:",total_turnaround_time_SJF)
    average_waiting_time = total_waiting_time_SJF / len(processes)  
    average_turnaround_time = total_turnaround_time_SJF / len(processes) 

    print("Average waiting time for SJF:", average_waiting_time)
    print("Average turnaround time for SJF:", average_turnaround_time)

    return total_waiting_time_SJF, total_turnaround_time_SJF 

def PS(processes):

    total_waiting_time = 0
    total_turnaround_time = 0
    current_time = 0
    
    sorted_processes = processes.copy()

    while sorted_processes:
        arrived_processes = [process for process in sorted_processes if process.arrival_time <= current_time]
        if not arrived_processes:
            current_time += 1
        else:
            sorted_processes.sort(key=lambda process: process.priority)
            highest_priority_job = arrived_processes[0]
            highest_priority_job.waiting_time = current_time - highest_priority_job.arrival_time
            highest_priority_job.turnaround_time = highest_priority_job.waiting_time + highest_priority_job.burst_time
            current_time += highest_priority_job.burst_time
            total_waiting_time += highest_priority_job.waiting_time
            total_turnaround_time += highest_priority_job.turnaround_time
            sorted_processes.remove(highest_priority_job)

    print("\ntotal waiting time for PS:", total_waiting_time)
    print("total turnaround time time for PS:", total_turnaround_time)
    average_waiting_time = total_waiting_time / len(processes)
    average_turnaround_time = total_turnaround_time / len(processes)

    print("Average waiting time for PS:", average_waiting_time)
    print("Average turnaround time for PS:", average_turnaround_time)

    return total_waiting_time, total_turnaround_time

def RR(processes, time_quantum):
    n = len(processes)
    timer, maxProcessIndex = 0, 0
    avg_waiting_time=0 
    avg_turnaround_time = 0
    total_waiting_time=0
    total_turnaround_time=0
    queue = deque()
    temp_burst = [process.burst_time for process in processes]
    complete = [False] * n

    while timer < processes[0].arrival_time:
        timer += 1

    queue.append(processes[0])

    while True:
        flag = True
        for i in range(n):
            if temp_burst[i] != 0:
                flag = False
                break

        if flag:
            break

        current_process = queue.popleft()
        ctr = 0
        while ctr < time_quantum and temp_burst[current_process.process_id - 1] > 0:
            temp_burst[current_process.process_id - 1] -= 1
            timer += 1
            ctr += 1

            for process in processes:
                if (
                    process.arrival_time <= timer
                    and not complete[process.process_id - 1]
                    and process.process_id != current_process.process_id
                ):
                    queue.append(process)

            if temp_burst[current_process.process_id - 1] == 0 and not complete[current_process.process_id - 1]:
                current_process.turnaround_time = timer
                complete[current_process.process_id - 1] = True

        if not queue:
            timer += 1

    for process in processes:
        process.turnaround_time -= process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        total_waiting_time += process.waiting_time
        total_turnaround_time += process.turnaround_time


    avg_waiting_time = total_waiting_time/4
    avg_turnaround_time = total_turnaround_time/4
    print("\ntotal waiting time for RR", total_waiting_time)
    print("total turnaround time for RR", total_turnaround_time)
    print("Average waiting time for RR:", avg_waiting_time)
    print("Average turnaround time for RR:", avg_turnaround_time)

    return total_waiting_time, total_turnaround_time

def main():
    processes = [
        Process(1, 0, 24, 3),
        Process(2, 4, 3, 1),
        Process(3, 5, 3, 4),
        Process(4, 6, 12, 2)
    ]

    total_waiting_time_FCFS, total_turnaround_time_FCFS = FCFS(processes)
    total_waiting_time_SJF, total_turnaround_time_SJF = SJF(processes)
    total_waiting_time_PS, total_turnaround_time_PS = PS(processes)
    total_waiting_time_RR, total_turnaround_time_RR = RR(processes, 4)

    avg_waiting_times = [
        total_waiting_time_FCFS / len(processes),
        total_waiting_time_SJF / len(processes),
        total_waiting_time_PS / len(processes),
        total_waiting_time_RR / len(processes)
    ]

    avg_turnaround_times=[
        total_turnaround_time_FCFS / len(processes),
        total_turnaround_time_SJF / len(processes),
        total_turnaround_time_PS / len(processes),
        total_turnaround_time_RR / len(processes)]

    lowest_waiting_time_index = avg_waiting_times.index(min(avg_waiting_times))
    lowest_turnaround_time_index = avg_turnaround_times.index(min(avg_turnaround_times))

    print("\nComparison Results:")
    print("Lowest Average Waiting Time Algorithm:", end=" ")
    if lowest_waiting_time_index == 0:
        print("FCFS")
    elif lowest_waiting_time_index == 1:
        print("SJF")
    elif lowest_waiting_time_index == 2:
        print("PS")
    else:
        print("RR")

    print("Lowest Average Turnaround Time Algorithm:", end=" ")
    if lowest_turnaround_time_index == 0:
        print("FCFS")
    elif lowest_turnaround_time_index == 1:
        print("SJF")
    elif lowest_turnaround_time_index == 2:
        print("PS")
    else:
        print("RR")

if __name__ == "__main__":
    main()
