"""
    Author:
        Eduardo Enrique Trujillo Ramos
        Rene Garcia Saenz
        Esteban Arocha Ortuno

    Description:
        Input parser that generates the different structures used.
"""
import sys
from cpuScheduler import *
from process import *

def parser():
    # Data read from STDIN stripped from spaces, tabs, and newlines.
    data = [line.split("//")[0].strip() for line in sys.stdin]
    simulation = [CPUScheduler(), CPUScheduler()]
    numScheduler = 0
    for line in data:
        if line == "FIN":
            numScheduler+=1
        elif line == "SJF":
            simulation[numScheduler].algorithm = "SJF"
        elif line == "SRT":
            simulation[numScheduler].algorithm = "SRT"
        else:
            words = line.split(" ")
            if len(words) == 0 or words[0] == "":
                continue
            elif words[0] == "QUANTUM":
                simulation[numScheduler].quantum = float(words[1])
            elif words[0] == "CONTEXT":
                simulation[numScheduler].context_switches = float(words[2])
            elif words[0] == "CPUS":
                simulation[numScheduler].num_cpus = float(words[1])
            elif len(words >= 3) and len(words <= 6):
                p = process()
                p.pid = words[0]
                p.arrival_time = float(words[1])
                p.cpu_time = float(words[2])
                if len(words) > 3 and words[3] == "I/O":
                    p.initial_io_time = float(words[4])
                    p.io_duration = float(words[5])
                simulation[numScheduler].processes.append(p)
            else:
                print("Error: Entrada de datos incorrecta.")
    return simulation[0], simulation[1]