"""
    Authors:
        Eduardo Enrique Trujillo Ramos
        Rene Garcia Saenz
        Esteban Arocha Ortuno

    Description:
        CPU for the simulation
"""

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
    def assign_process(self, process):
        if not self.changed_context:
            return False
        if self.in_use and self.current_process.cpu_time < process.cpu_time:
            self.change_context(process)
            self.current_process = process
            self.current_time = 0
            return True
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
