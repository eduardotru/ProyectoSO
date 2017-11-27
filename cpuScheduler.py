"""
    Authors:
        Eduardo Enrique Trujillo Ramos
        Rene Garcia Saenz
        Esteban Arocha Ortuno

    Description:
        CPUScheduler simulator.
"""
import sys
# from cpu import *
import Queue
# from process import *

timer = 0

timeSRT = []
timeSJF = []

arrayInput = []

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
        # Copy of list of processes
        self.processes_copy = []
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
        timer = 0
        print("=============================================================================================================================================")
        print("Input")
        for arr in arrayInput[0]:
            print(arr)
        arrayInput.pop(0)
        self.outputHeader()
        self.createCPUs()

        for proc in self.processes:
            self.processes_copy.append(proc)
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
            timer += 1
            if self.timer > 1000:
                break
        print("---------------------------------------------------------------------------------------------------------------------------------------------")
        print ("Estadisitcas: ")
        turnaround_prom = 0
        tiempo_espera_prom = 0
        count = 0
        for process in self.processes_copy:
            print("Process ID: %s" %(process.pid))
            print("Turaround time: %s" % (process.time_to_finish))
            print("Tiempo de espera: %s" % (process.time_to_finish - process.cpu_time))
            turnaround_prom +=  process.time_to_finish
            tiempo_espera_prom += process.time_to_finish - process.cpu_time
            count += 1
        tiempo_espera_prom = tiempo_espera_prom /count
        turnaround_prom = turnaround_prom/count
        print("Turaround promedio: %s" %turnaround_prom)
        print("Tiempo de espera promedio: %s" %tiempo_espera_prom)
        if self.algorithm == "SJF":
            timeSJF.append(tuple((turnaround_prom, tiempo_espera_prom)))
        elif self.algorithm == "SRT":
            timeSRT.append(tuple((turnaround_prom, tiempo_espera_prom)))
    
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
                self.blocked_list.append(blocked) #CPU listos y bloquedados
            for process in self.processes_copy:
                if cpu.current_process and process.pid == cpu.current_process.pid and not cpu.current_process.blocked and cpu.in_use:
                    process.time_to_finish += 1
        for process_block in self.blocked_list:
            for process_copy in self.processes_copy:
                if self.blocked_list and process_block.pid == process_copy.pid:
                    process_copy.time_to_finish += 1
        for process_ready in self.ready_list.queue:
            for process_copy in self.processes_copy:
                if self.ready_list and process_ready.pid == process_copy.pid:
                    process_copy.time_to_finish += 1


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
                if isinstance(assigned, process):
                    self.ready_list.put(assigned)
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


class CPU(object):
    def __init__(self, num, quantum, context_switch):
        # CPU id number
        self.num = num
        # CPU quantum
        self.quantum = quantum
        # Time the cpu is on
        self.current_time = 0
        # Process currently inside the CPU
        self.current_process = None
        # Determines if the CPU is being used or not
        self.in_use = False
        # Determines if it already had a context change
        self.changed_context = False
        # Time that it takes to change a process
        self.context_switch = context_switch

    # Asigns the process to the CPU
    def assign_process(self, process, scheduler = None):
        if not self.changed_context:
            return False
        if self.in_use and (self.current_process.cpu_time - self.current_process.time_processed) >= (process.cpu_time - process.time_processed):
            p = self.current_process
            self.change_context(process)
            self.current_process = process
            self.current_time = 0
            return p
        elif not self.in_use:
            self.change_context(process)
            self.current_process = process
            self.in_use = True
            self.current_time = 0
            return True
        else:
            return False

    # Limpia todas las variables del cpu
    def clear(self):
        self.in_use = False
        self.current_time = 0

    # Hace un paso del cpu, se mueve una unidad de tiempo.
    def step(self):
        self.current_time += 1
        # No ejecutara el proceso y hara return hasta que no hayan pasado
        # la cantidad de steps necesario para llegar a un cambio de contexto
        # en caso de que sea un proceso que anteriormente ya estaba en el CPU
        # la segunda parte la condicion lo dejara pasar
        if self.current_process and self.current_time == self.context_switch and self.context_switch != 0 and not self.changed_context:
            self.current_process.time_processed -= 1
        if self.current_time >= self.context_switch:
            self.changed_context = True
        if not self.changed_context:
            return None
        if self.current_process:
            if self.current_process.cpu_time - 1 == self.current_process.time_processed:
                self.clear()
            elif self.current_process.time_processed in self.current_process.initial_io_time:
                p = self.current_process
                self.clear()
                p.initial_io_time.remove(p.time_processed)
                return self.current_process
            elif not self.current_process.blocked:
                self.current_process.time_processed += 1
        return None

    def change_context(self, process):
        if self.current_process and self.current_process.pid != process.pid and self.context_switch != 0:
            self.changed_context = False

    def __repr__(self):
        return str(self)

    def __str__(self):
        process = ""
        context = ""
        if self.in_use:
            process = str(self.current_process)
        else:
            process = "EMPTY "
        if not self.changed_context:
            context = "Context Switch "
        return "CPU " + str(self.num) + ": " + context + process


class process:

    def __init__(self):
        # Process ID
        self.pid = 0
        # Time in miliseconds that the process is in the cpu
        self.cpu_time = 0
        # Time that has been processed
        self.time_processed = 0
        # Arrival time of the process to the CPU Scheduler
        self.arrival_time = 0
        # Unused. Priority of the process
        self.priority = 0
        # Time relative to its cpu time in which it orders an IO operation.
        self.initial_io_time = []
        # Number of io operations
        self.number_of_io = 0
        # Duration of the IO operation
        self.io_duration = []
        # True if the process is blocked in an IO operation
        self.blocked = False
        #Time from start to end of the process
        self.time_to_finish = 0

    def __cmp__(self, other):
        return cmp(self.cpu_time, other.cpu_time)

    def __str__(self):
        process_string = str(self.pid) + "("
        if self.blocked:
            process_string += str(self.io_duration[0]) + ")"
            if self.io_duration[0] == 1:
                process_string += " -- termina IO"
        else:
            process_string += str(self.cpu_time - self.time_processed) + ")"
        return process_string

    def __repr__(self):
        return str(self)


# Parses the incoming data to create the two CPUSchedulers
def parse():
    # Data read from STDIN stripped from spaces, tabs, and newlines.
    data = [line.split("//")[0].strip() for line in sys.stdin]
    simulations = []
    simulation = CPUScheduler()
    numScheduler = 0
    new_input = []
    for line in data:
        #print line
        if line == "FIN":
            if simulation.context_switches == 0:
                simulation.changed_context = True
            if simulation.quantum != -1 and simulation.context_switches != -1 and simulation.algorithm != "" and len(simulation.processes) > 0:
                arrayInput.append(new_input)
                simulations.append(simulation)
            simulation = CPUScheduler()
            new_input = []
            numScheduler+=1
        elif line == "SJF":
            new_input.append(line)
            simulation.algorithm = "SJF"
        elif line == "SRT":
            new_input.append(line)
            simulation.algorithm = "SRT"
        else:
            new_input.append(line)
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
                    p.number_of_io = len(zipped)
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
print ("")
print("=============================================================================================================================================")
print("Resumen de tiempos promedios")
print("SRT:")
for srt in timeSRT:
    print("Turnaround promedio: %s" %srt[0])
    print("Tiempo de espera promedio: %s" %srt[1])

print(" ")
print("SRT:")
for sjf in timeSJF:
    print("Turnaround promedio: %s" %sjf[0])
    print("Tiempo de espera promedio: %s" %sjf[1])

print ("")
print("=============================================================================================================================================")
print("Comparacion de algoritmos")
for x in range(0, len(timeSRT)):
    print("Algoritmo: %s" %(x + 1))
    if timeSJF[x][0] < timeSRT[x][0]:
        print("Para el conjunto de procesos %s es mejor usar SJF. " %(x + 1))
    else:
        print("Para el conjunto de procesos %s es mejor usar SRT. " %(x + 1))
