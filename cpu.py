"""
    Authors:
        Eduardo Enrique Trujillo Ramos
        Rene Garcia Saenz
        Esteban Arocha Ortuno

    Description:
        CPU for the simulation
"""

class CPU(object):
    def __init__(self, quantum, context_switch):
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
        # Checar si el proceso actual es el mismo que se habia asignado
        # anteriomente, para determinar si hay cambio de contexto.
        if self.current_process != process:
            self.changed_context = False
        if self.in_use and self.current_process.cpu_time < process.cpu_time
            self.current_process = process
            return True
        elif not self.in_use:
            self.current_process = process
            self.in_use = True
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
        if self.current_time < self.context_switch and not changed_context:
            return
        changed_context = True
        if self.current_process:
            if self.current_process.cpu_time == self.current_process.time_processed:
                self.clear()
            elif self.current_process.time_processed in self.current_process.initial_io_time:
                p = self.current_process
                self.clear()
                p.initial_io_time.remove(p.time_processed)
                return self.current_process 
            else:
                self.current_process.time_processed += 1
        return None

    def change_context(self):
        # TODO(anyone): make it work with the context switch

