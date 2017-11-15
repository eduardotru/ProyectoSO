"""
    Authors:
        Eduardo Enrique Trujillo Ramos
        Rene Garcia Saenz
        Esteban Arocha Ortuno

    Description:
        CPUScheduler simulator.
"""

class CPUScheduler:
    def __init__(self):
        self.algorithm = ""
        self.num_cpus = 0
        self.quantum = 0
        self.context_switches = 0
        self.processes = []
