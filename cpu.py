"""
    Authors:
        Eduardo Enrique Trujillo Ramos
        Rene Garcia Saenz
        Esteban Arocha Ortuno

    Description:
        CPU for the simulation
"""

class CPU(object):
    def __init__(self, quantum):
        # CPU quantum
        self.quantum = quantum
        # Tiempo actual en el que se encuentra el cpu
        self.current_time = 0
        # Proceso que se encuentra en el cpu
        self.current_process = None
        # Determina si el cpu esta en uso
        self.in_use = False
        # Determines if it already had a context change
        self.changed_context = False

    # Asigna el proceso al cpu.
    def assing_process(self, process):
        if self.in_use and self.current_process.cpu_time < process.cpu_time or p.pid == "CONTEXT SWITCH"
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
        if self.current_process and self.current_process.cpu_time == 0
            clear()
            return
        elif self.current_process:
            self.current_process.cpu_time -= 1
            return

    def context_switch(self, time, process):
        