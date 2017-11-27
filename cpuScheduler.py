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
        self.quantum = -1
        # Time that it takes to change context
        self.context_switches = -1
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
            new_cpu = CPU(i+1, self.quantum, self.context_switches)
            # If context switch takes 0, then the CPU is already done with
            # context switch
            if self.context_switches == 0:
                new_cpu.changed_context = True
            self.cpus.append(new_cpu)

    
    # Returns True if all cpus are not in use
    def cpusEmpty(self):
        empty = True
        for cpu in self.cpus:
            empty = empty and not cpu.in_use
        return empty

    # TODO(anyone): Hacer que este programa pare.
    def start(self):
        self.outputHeader()
        self.createCPUs()
        while len(self.processes) > 0 or len(self.ready_list.queue) > 0 or len(self.blocked_list) > 0 or not self.cpusEmpty():
            # Check to see if there is a Process that just arrived
            self.checkProcesses()
            # Check if a process can be unblocked
            self.checkBlockedList()
            
            if self.algorithm == "SJF":
                self.stepCPUs()
                self.SJF()
            elif self.algorithm == "SRT":
                self.stepCPUs()
                self.SRT()
            else:
                print("Incorrect schedulling algorithm, cannot start CPUScheduler.")
                return
            self.output()
            self.timer += 1
            if self.timer > 100:
                break
        print("=============================================================================================================================================")

    # Check if there is a process that just arrived and add it to the ready list.
    def checkProcesses(self):
        aux = list(self.processes)
        for process in aux:
            if process.arrival_time == self.timer:
                self.ready_list.put(process)
                self.processes.remove(process)

    # Check the process that are blocked if they can be unblocked
    def checkBlockedList(self):
        aux = list(self.blocked_list)
        for blocked_p in aux:
            if blocked_p.io_duration[0] == 1:
                blocked_p.blocked = False
                self.blocked_list.remove(blocked_p)
                blocked_p.io_duration.remove(1)
                self.ready_list.put(blocked_p)
            else:
                blocked_p.io_duration[0] -= 1

    # Make a step in each CPU
    def stepCPUs(self):
        for cpu in self.cpus:
            blocked = cpu.step()
            if blocked:
                blocked.blocked = True
                self.blocked_list.append(blocked)

    # SJF is a non preemptive algorithm so first check if the cpu is not in use.
    def SJF(self):
        for cpu in self.cpus:
            if not cpu.in_use and len(self.ready_list.queue) > 0:
                p = self.ready_list.get()
                assigned = cpu.assign_process(p)
                if not assigned:
                    self.ready_list.put(p)


    # SRT is a preemptive algorithm, assign only if the time is shorter.
    def SRT(self):
        for cpu in self.cpus:
            if len(self.ready_list.queue) > 0:
                p = self.ready_list.get()
                assigned = cpu.assign_process(p)
                if not assigned:
                    self.ready_list.put(p)

    # Output the Header of the table
    def outputHeader(self):
        print("=============================================================================================================================================")
        print("|| Tiempo   || Cola de Listos                    || CPUs                                                         || Bloqueados             ||")
        print("---------------------------------------------------------------------------------------------------------------------------------------------")

    # Outputs a row of the table according to the information in the CPUScheduller
    def output(self):
        print("|| {0:8} || {1:33} || {2:60} || {3:22} ||".format(
            self.timer, self.ready_list.queue, self.cpus, self.blocked_list))
        print("---------------------------------------------------------------------------------------------------------------------------------------------")


# Parses the incoming data to create the two CPUSchedulers
def parse():
    # Data read from STDIN stripped from spaces, tabs, and newlines.
    data = [line.split("//")[0].strip() for line in sys.stdin]
    simulations = []
    simulation = CPUScheduler()
    numScheduler = 0
    for line in data:
        print line
        if line == "FIN":
            if simulation.context_switches == 0:
                simulation.changed_context = True
            if simulation.quantum != -1 and simulation.context_switches != -1 and simulation.algorithm != "" and len(simulation.processes) > 0:
                simulations.append(simulation)
            simulation = CPUScheduler()
            numScheduler+=1
        elif line == "SJF":
            simulation.algorithm = "SJF"
        elif line == "SRT":
            simulation.algorithm = "SRT"
        else:
            words = line.split(" ")
            if len(words) == 0 or words[0] == "":
                continue
            elif words[0] == "QUANTUM":
                simulation.quantum = int(words[1])
            elif words[0] == "CONTEXT":
                simulation.context_switches = int(words[2])
            elif words[0] == "CPUS":
                simulation.num_cpus = int(words[1])
            elif len(words) >= 3 and words[0].isdigit() and words[1].isdigit() and words[2].isdigit():
                p = process()
                p.pid = int(words[0])
                p.arrival_time = int(words[1])
                p.cpu_time = int(words[2])
                if len(words) > 3 and words[3] == "I/O":
                    is_start = True
                    words.pop(0)
                    words.pop(0)
                    words.pop(0)
                    words.pop(0)
                    zipped = zip(words[0::2], words[1::2])
                    for pair in zipped:
                        p.initial_io_time.append(int(pair[0]))
                        p.io_duration.append(int(pair[1]))
                simulation.processes.append(p)
            else:
                print("Error: Entrada de datos incorrecta.")
    return simulations

simulations = parse()

for simulation in simulations:
    simulation.start()
