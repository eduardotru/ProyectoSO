class process:

    def __init__(self):
        #Identificador unico del proceso
        self.pid = 0
        #Tiempo de CPU en milisegundos que utiliza el proceso
        self.cpu_time = 0
        #Tiempo en el que llega el proceso en milisegundos
        self.arrival_time = 0
        #Prioridad del proceso de 1 a 10 donde 1 es la mayor prioridad
        self.priority = 0
        #Tiempo en el que el proceso pide una operacion de input/output
        self.initial_io_time = 0
        #Duracion de la intervencion de Input/Output
        self.io_duration = 0

    def __cmp__(self, other):
        return cmp(self.cpu_time, other.cpu_time)