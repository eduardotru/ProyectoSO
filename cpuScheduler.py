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
        # CPUs that are going to be used
        self.cpus = {}
    
    def createCPUs(self):
        for i in range(1, num_cpus):
            self.cpus.append(CPU(self.quantum))
    
    # TODO(anyone): Hacer que este programa pare.
    def start(self):
        self.createCPUs()
        while True:
            for process in processes:
                if process.arrival_time == self.timer:
                    self.ready_list.put(process)
            if self.algorithm == "SJF": 
                for cpu in cpus:
                    if not cpu.in_use and len(self.ready_list) > 0:
                        cpu.assign_process(self.ready_list.get())
                # TODO(anyone): Terminar esto
            elif self.algorithm == "SRT":
                # TODO(anyone): Terminar esto tambien
            else:
                print("Incorrect schedulling algorithm, cannot start CPUScheduler.")
                return
            self.output()
            self.timer += 1

    # TODO(anyone): Hacer que se imprima bien el output
    def output(self):
        print("Implementame esta")

cpuSchedule1, cpuSchedule2 = parser()