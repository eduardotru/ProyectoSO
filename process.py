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

    def __cmp__(self, other):
        return cmp(self.cpu_time, other.cpu_time)