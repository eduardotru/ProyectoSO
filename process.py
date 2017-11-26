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
        # Duration of the IO operation
        self.io_duration = []
        # True if the process is blocked in an IO operation
        self.blocked = False

    def __cmp__(self, other):
        return cmp(self.cpu_time, other.cpu_time)

    def __str__(self):
        process_string = self.pid + "("
        if self.blocked:
            process_string += str(self.io_duration[0]) + ")"
            if self.io_duration[0] == 1:
                process_string += " -- termina IO"
        else:
            process_string += str(self.cpu_time - self.time_processed) + ")"
        return process_string

    def __repr__(self):
        return str(self)