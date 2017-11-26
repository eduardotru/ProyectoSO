"""
    Authors:
        Eduardo Enrique Trujillo Ramos
        Rene Garcia Saenz
        Esteban Arocha Ortuno

    Description:
        CPUScheduler simulator.
"""
import parser
from cpu import *
import Queue

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
        # List of finished processes
        self.finished = []
        # Priority Queue for the ready processes since they are ordered by cpu time
        self.ready_list = Queue.PriorityQueue()
        # Process which get blocked because an IO go in here.
        self.blocked_list = []
        # CPUs that are going to be used
        self.cpus = {}
    
    # Creates CPU objects
    def createCPUs(self):
        for i in range(1, num_cpus):
            self.cpus.append(CPU(self.quantum, self.context_switches))
    
    # Returns True if all cpus are not in use
    def cpusEmpty(self):
        empty = True
        for cpu in self.cpus:
            empty = empty and not cpu.in_use
        return empty

    # TODO(anyone): Hacer que este programa pare.
    def start(self):
        self.createCPUs()
        while len(self.processes) > 0 and len(self.ready_list) > 0 and len(self.blocked_list) > 0 and not self.cpusEmpty():
            # Check if there is a process that just arrived and add it to the ready list.
            for process in self.processes:
                if process.arrival_time == self.timer:
                    self.ready_list.put(process)
                    self.processes.remove(process)
            # Check the process that are blocked if they can be unblocked
            for blocked_p in blocked_list:
                if blocked_p.io_duration[0] == 0:
                    blocked_list.remove(blocked_p)
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
                    if not cpu.in_use and len(self.ready_list) > 0:
                        p = self.ready_list.get()
                        cpu.assign_process(p)
            # SRT is a preemptive algorithm, assign only if the time is shorter.
            elif self.algorithm == "SRT":
                for cpu in self.cpus:
                    cpu.step()
                    if len(self.ready_list) > 0:
                        p = self.ready_list.get()
                        assigned = cpu.assign_process(p)
                        if not assigned:
                            self.ready_list.put(p)
            else:
                print("Incorrect schedulling algorithm, cannot start CPUScheduler.")
                return
            self.output()
            self.timer += 1

    # TODO(anyone): Hacer que se imprima bien el output
    def output(self):
        print("Implementame esta")

cpuSchedule1, cpuSchedule2 = parser()