class CPU(object):
    def __init__(self, quantum):
        # Quantum del cpu
        self.quantum = quantum

        # Tiempo actual en el que se encuentra el cpu
        self.current_time = 0

        # Proceso que se encuentra en el cpu
        self.current_process = 0

        # Determina si el cpu esta en uso
        self.in_use = False

    # Asigna el proceso al cpu.
    def assing_process(self, process):
        self.current_process = process
        self.in_use = True

    # Limpia todas las variables del cpu
    def clear(self):
        self.in_user = False
        self.current_time = 0

    # Hace un paso del cpu, se mueve una unidad de tiempo.
    def step(self):
        self.current_time += 1

        if self.current_time >= self.current_process.cpu_time:
            clear()
            return

