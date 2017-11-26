"""
    Authors:
        Eduardo Enrique Trujillo Ramos
        Rene Garcia Saenz
        Esteban Arocha Ortuno

    Description:
        CPUScheduler simulator.
"""
import sys
from cpu import *
import Queue
from process import *

class CPUScheduler:
    def __init__(self):
        # The timer expresses the actual time
        self.timer = 0
        # The algorithm being used, either SJF or SRT
        self.algorithm = ""
        # The number of CPUs of the scheduler
        self.num_cpus = 0
        # Unused since SJF nor SRT use quantum
        self.quantum = 0
        # Time that it takes to change context
        self.context_switches = 0
        # List of processes
        self.processes = []
        # Priority Queue for the ready processes since they are ordered by cpu time
        self.ready_list = Queue.PriorityQueue()
        # Process which get blocked because an IO go in here.
        self.blocked_list = []
        # CPUs that are going to be used
        self.cpus = []
    
    # Creates CPU objects
    def createCPUs(self):
        for i in range(self.num_cpus):
            self.cpus.append(CPU(i+1, self.quantum, self.context_switches))
    
    # Returns True if all cpus are not in use
    def cpusEmpty(self):
        empty = True
        for cpu in self.cpus:
            empty = empty and not cpu.in_use
        return empty

    # TODO(anyone): Hacer que este programa pare.
    def start(self):
        print("CPUScheduler started ===============================")
        self.createCPUs()
        while len(self.processes) > 0 or len(self.ready_list.queue) > 0 or len(self.blocked_list) > 0 or not self.cpusEmpty():
            # Check if there is a process that just arrived and add it to the ready list.
            aux = list(self.processes)
            for process in aux:
                if process.arrival_time == self.timer:
                    self.ready_list.put(process)
                    self.processes.remove(process)
            # Check the process that are blocked if they can be unblocked
            aux = list(self.blocked_list)
            for blocked_p in aux:
                if blocked_p.io_duration[0] == 0:
                    self.blocked_list.remove(blocked_p)
                    blocked_p.io_duration.remove(0)
                    self.ready_list.put(blocked_p)
                else:
                    blocked_p.io_duration[0] -= 1
            # SJF is a non preemptive algorithm so first check if the cpu is not in use.
            if self.algorithm == "SJF":
                for cpu in self.cpus:
                    blocked = cpu.step()
                    if blocked:
                        self.blocked_list.append(blocked)
                    if not cpu.in_use and len(self.ready_list.queue) > 0:
                        p = self.ready_list.get()
                        cpu.assign_process(p)
            # SRT is a preemptive algorithm, assign only if the time is shorter.
            elif self.algorithm == "SRT":
                for cpu in self.cpus:
                    blocked = cpu.step()
                    if blocked:
                        self.blocked_list.append(blocked)
                    if len(self.ready_list.queue) > 0:
                        p = self.ready_list.get()
                        assigned = cpu.assign_process(p)
                        if not assigned:
                            self.ready_list.put(p)
            else:
                print("Incorrect schedulling algorithm, cannot start CPUScheduler.")
                return
            self.output()
            self.timer += 1

    def output(self):
        print("|| Tiempo: {0:5} || Listos: {1:25} || {2:20} || Bloqueados: {3:10} ||".format(
            self.timer, self.ready_list.queue, self.cpus, self.blocked_list))
        '''
        print("Procesos bloqueados: ")
        for blocked in self.blocked_list:
            if (blocked.io_duration[0] == 1):
                print(blocked.pid + "(1) -- termina su I/O")
            else:
                print(blocked.pid + "(" + str(blocked.io_duration[0]) + ")")'''
        print("================================================================================================================")

def parse():
    # Data read from STDIN stripped from spaces, tabs, and newlines.
    data = [line.split("//")[0].strip() for line in sys.stdin]
    simulation = [CPUScheduler(), CPUScheduler()]
    numScheduler = 0
    for line in data:
        if line == "FIN":
            numScheduler+=1
        elif line == "SJF":
            simulation[numScheduler].algorithm = "SJF"
        elif line == "SRT":
            simulation[numScheduler].algorithm = "SRT"
        else:
            words = line.split(" ")
            if len(words) == 0 or words[0] == "":
                continue
            elif words[0] == "QUANTUM":
                simulation[numScheduler].quantum = int(words[1])
            elif words[0] == "CONTEXT":
                simulation[numScheduler].context_switches = int(words[2])
            elif words[0] == "CPUS":
                simulation[numScheduler].num_cpus = int(words[1])
            elif len(words) >= 3 and len(words) <= 6:
                p = process()
                p.pid = words[0]
                p.arrival_time = int(words[1])
                p.cpu_time = int(words[2])
                if len(words) > 3 and words[3] == "I/O":
                    p.initial_io_time.append(int(words[4]))
                    p.io_duration.append(int(words[5]))
                simulation[numScheduler].processes.append(p)
            else:
                print("Error: Entrada de datos incorrecta.")
    return simulation[0], simulation[1]

cpuSchedule1, cpuSchedule2 = parse()
cpuSchedule1.start()
cpuSchedule2.start()
